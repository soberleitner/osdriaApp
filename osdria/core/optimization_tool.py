import re

from pyomo.environ import *
import pyomo.core.kernel.set_types as var_types

from models.constants import DatasetResolution, PyomoVarType
from models.property import PropertyValueTimeSeries
from models.data_structure import List, Dict

SOLVER = 'gurobi'


class Optimizer:
    """incorporates the optimization code of Pyomo"""
    def __init__(self, process_list, commodity_list):
        self._processes = process_list
        self._commodities = commodity_list
        self._model = ConcreteModel(name="OSDRIA optimization model")
        self._commodity_list = {}
        self._variables = {}
        self._objective_expressions = []

    def translate(self):
        """translate processes in pyomo code"""
        # perform process specific translation
        for process in self._processes:
            process_code_name = process.name.lower().replace(" ", "_")
            obj = process.core.objective_function
            const = process.core.constraints
            [obj, const] = self.translate_variables(process_code_name, process.core.variables, obj, const)
            [obj, const] = self.translate_data(process.core.data, obj, const)
            [obj, const] = self.translate_properties(process_code_name, process.properties[1:], obj, const)
            [obj, const] = self.translate_commodities(process_code_name, process.name, process.inputs, obj, const)
            [obj, const] = self.translate_commodities(process_code_name, process.name, process.outputs, obj, const, False)
            self.translate_constraints(process_code_name, const)
            self.translate_objective(process_code_name, obj)

        # add commodity constraints
        for commodity, content in self._commodity_list.items():
            # create Constraint
            commodity_code_name = "commodity_" + commodity.lower().replace(" ", "_")
            res_index = "[_" + str(content['resolution'])[0].lower() + "_]"
            # set commodity sum to overflow variable
            pos_overflow = commodity_code_name + "_overflow_pos"
            neg_overflow = commodity_code_name + "_overflow_neg"
            commodity_const = content['com_sum'] + "==" + pos_overflow + res_index + " - " + neg_overflow + res_index
            commodity_range = range(content['resolution'].value)

            self._model.add_component(pos_overflow, Var(commodity_range, within=NonNegativeReals))
            self._variables[pos_overflow] = self._model.component(pos_overflow)
            self._model.add_component(neg_overflow, Var(commodity_range, within=NonNegativeReals))
            self._variables[neg_overflow] = self._model.component(neg_overflow)

            self.translate_constraints(commodity_code_name, commodity_const)

            commodity_objective = "(" + pos_overflow + res_index + " + " + neg_overflow + res_index + ") * 10000"
            self.translate_objective(commodity_code_name, commodity_objective)

        # add objective function
        self._model.objective = Objective(expr=sum(self._objective_expressions))

    def solve(self):
        opt = SolverFactory(SOLVER)
        results = opt.solve(self._model)
        print(results)

    def get_model(self):
        """return model expressions"""
        print("Variables")
        model_expr = "Variables:\n"
        for variable in self._model.component_data_objects(Var):
            model_expr += str(variable) + " ... " + str(variable.domain) + "\n"
        model_expr += "Parameters:\n"
        for parameter in self._model.component_data_objects(Param):
            model_expr += str(parameter) + "\n"
        print("Constraints")
        model_expr += "Constraints:\n"
        for constraint in self._model.component_data_objects(Constraint):
            model_expr += str(constraint.expr) + "\n"
        print("Objective")
        model_expr += "Objective:\n"
        for objective in self._model.component_data_objects(Objective):
            model_expr += str(objective.expr) + "\n"
        print("Done")

        return model_expr

    def set_results(self):
        """set optimization results in processes and commodities"""
        for process in self._processes:
            process.optimization_output = Dict({})
            process_code_name = process.name.lower().replace(" ", "_")
            for variable in process.core.variables:
                variable_code_name = variable.name.lower().replace(" ", "_")
                unique_name = process_code_name + "__" + variable_code_name
                process.optimization_output[variable.name] = List([result for result in
                                                         self._model.component(unique_name).get_values().values()])

        # set commodity flow results
        for commodity in self._commodities:
            commodity.optimization_output = Dict({"input_processes": Dict({}), "output_processes": Dict({})})
            commodity_code_name = commodity.name.lower().replace(" ", "_")
            for process_direction in ["input_processes", "output_processes"]:
                for process_name in self._commodity_list[commodity.name][process_direction]:
                    process_code_name = process_name.lower().replace(" ", "_")
                    commodity_process_name = commodity_code_name + "__" + process_code_name
                    commodity.optimization_output[process_direction][process_name] = \
                        List([result for result in self._model.component(commodity_process_name).get_values().values()])
                # add balance to commodity flows
                if process_direction == "input_processes":
                    commodity_process_name = "commodity_" + commodity_code_name + "_overflow_pos"
                    process_name = "Positive Balance"
                else:
                    commodity_process_name = "commodity_" + commodity_code_name + "_overflow_neg"
                    process_name = "Negative Balance"

                commodity.optimization_output[process_direction][process_name] = \
                    List([result for result in self._model.component(commodity_process_name).get_values().values()])


    def cancel(self):
        pass

    def translate_variables(self, process_code_name, variables, obj, const):
        # converts variables into pyomo variables and adds them to list
        for variable in variables:
            variable_code_name = variable.name.lower().replace(" ", "_")
            unique_name = process_code_name + "__" + variable_code_name
            replace_name = unique_name

            # add variable to declaration as pyomo Var
            pyomo_type = variable.pyomo_type
            if pyomo_type.name in [res.name for res in list(DatasetResolution)]:
                # set boundaries for index variables
                resolution = DatasetResolution[pyomo_type.name]
                pyomo_type = PyomoVarType.NON_NEGATIVE_INTEGERS
                self._model.add_component(unique_name, Var(within=getattr(var_types, pyomo_type.value),
                                                           bounds=(0, resolution.value - 1)))

            else:
                self._model.add_component(unique_name, Var(range(variable.resolution.value),
                                                           within=getattr(var_types, pyomo_type.value)))
                # replace indexed variable name
                [obj, const] = self.translate_indexed_terms([obj, const],
                                                            variable_code_name, unique_name,
                                                            variable.resolution)
                replace_name += "[_" + str(variable.resolution)[0].lower() + "_]"

            # replace variable name without indexing
            re_pattern = re.compile(r"\b(" + re.escape(variable_code_name) + r")(\b[^\[]|$)", flags=re.MULTILINE)
            [obj, const] = [re.sub(re_pattern, replace_name + r"\g<2>", s) for s in [obj, const]]

            self._variables[unique_name] = self._model.component(unique_name)

        return [obj, const]

    @staticmethod
    def translate_data(data, obj, const):
        # replaces data names with number
        for datum in data:
            datum_name = datum.name.lower().replace(" ", "_")
            [obj, const] = [s.replace(datum_name, datum.value) for s in [obj, const]]

        return [obj, const]

    def translate_properties(self, process_code_name, properties, obj, const):
        # replaces property names with number or create pyomo Param for time series
        for prop in properties:
            prop_code_name = prop.name.lower().replace(" ", "_")
            if isinstance(prop.value, PropertyValueTimeSeries):
                unique_name = process_code_name + "__" + prop_code_name
                init_dict = {i: float(v) for i, v in enumerate(prop.value.value)}
                resolution = DatasetResolution(len(prop.value.value))
                # add property to declaration as pyomo Param
                self._model.add_component(unique_name, Param(range(resolution.value), initialize=init_dict))
                self._variables[unique_name] = self._model.component(unique_name)
                # replace indexed variable name
                [obj, const] = self.translate_indexed_terms([obj, const], prop_code_name, unique_name, resolution)

                unique_name += "[_" + str(resolution)[0].lower() + "_]"
            else:
                unique_name = str(prop.value)

            re_pattern = re.compile(r"\b(" + re.escape(prop_code_name) + r")(\b[^\[]|$)", flags=re.MULTILINE)
            [obj, const] = [re.sub(re_pattern, unique_name + r"\g<2>", s) for s in [obj, const]]

        return [obj, const]

    def translate_commodities(self, process_code_name, process_name, commodities, obj, const, input_com=True):
        # converts commodities into pyomo variables and adds them to list respecting the direction
        for commodity in commodities:
            commodity_code_name = commodity.name.lower().replace(" ", "_")
            unique_name = commodity_code_name + "__" + process_code_name
            if commodity.name not in self._commodity_list:
                self._commodity_list[commodity.name] = {'resolution': commodity.resolution, 'com_sum': "",
                                                        'input_processes': [], 'output_processes': []}

            # add variable to declaration as pyomo Var
            self._model.add_component(unique_name, Var(range(commodity.resolution.value), within=NonNegativeReals))
            self._variables[unique_name] = self._model.component(unique_name)

            # replace indexed variable name
            [obj, const] = self.translate_indexed_terms([obj, const], commodity_code_name, unique_name,
                                                        commodity.resolution)
            # replace commodity name without indexing
            resolution_index = "[_" + str(commodity.resolution)[0].lower() + "_]"
            re_pattern = re.compile(r"\b(" + re.escape(commodity_code_name) + r")(\b[^\[]|$)", flags=re.MULTILINE)
            [obj, const] = [re.sub(re_pattern, unique_name + resolution_index + r"\g<2>", s) for s in [obj, const]]

            # and commodity with -/+ as input/output to commodity sum
            commodity_direction = '-' if input_com else '+'
            self._commodity_list[commodity.name]['com_sum'] += commodity_direction + unique_name + resolution_index

            process_direction = 'input_processes' if input_com else 'output_processes'
            self._commodity_list[commodity.name][process_direction].append(process_name)

        return [obj, const]

    def translate_constraints(self, process_code_name, const):
        for index, constraint in enumerate(const.split("\n")):
            unique_name = process_code_name + "__const_" + str(index)
            constraint = constraint.replace("[_y_]", "[0]")

            for resolution in list(DatasetResolution):
                resolution_letter = "_" + str(resolution)[0].lower() + "_"
                if resolution_letter in constraint:
                    constraint = self.translate_piecewise_constraint(constraint, unique_name, resolution)
                    self._model.add_component(unique_name,
                                              Constraint(range(resolution.value),
                                                         rule=lambda model, i: eval(constraint,
                                                                                    self._variables,
                                                                                    {resolution_letter: i})))
                    break

    def translate_piecewise_constraint(self, constraint, unique_name, resolution):
        resolution_value = resolution.value
        res_index = "_" + str(resolution)[0].lower() + "_"
        piecewise_function_name = unique_name + "_piecewise_function"
        piecewise_output_name = unique_name + "_piecewise_output"
        piecewise_input_name = unique_name + "_piecewise_input"
        re_pattern = re.compile(r"\bPiecewise\(\s*(.*?)\s*,\s*({.*?\})\s*\)", flags=re.MULTILINE)

        piecewise_counter = 0
        # search for multiply Piecewise expressions in constraint line
        while True:
            match = re.search(re_pattern, constraint)
            if not match:
                break

            piecewise_counter += 1
            output_name = piecewise_output_name + "_" + str(piecewise_counter)
            function_name = piecewise_function_name + "_" + str(piecewise_counter)
            input_name = piecewise_input_name + "_" + str(piecewise_counter)

            constraint = re.sub(match.re, output_name + "[" + res_index + "]", constraint, 1)
            input_expression = match[1]
            data_dict = eval(match[2])
            indizes = list(data_dict.keys())

            # add input and output variables
            self._model.add_component(input_name, Var(range(resolution_value),
                                                      within=Reals,
                                                      bounds=(min(indizes), max(indizes))))
            self._model.add_component(output_name, Var(range(resolution_value), within=NonNegativeReals))
            self._variables[output_name] = self._model.component(output_name)

            # add constraint for relationship between input expression of Piecewise function
            # and actual input in piecewise function
            def input_constraint(model, i):
                return model.component(input_name)[i] == eval(input_expression, self._variables, {res_index: i})

            self._model.add_component(input_name + "_const", Constraint(range(resolution_value), rule=input_constraint))

            # add piecewise function with data_dict
            self._model.add_component(function_name, Piecewise(range(resolution_value),
                                                               self._model.component(output_name),
                                                               self._model.component(input_name),
                                                               pw_pts=indizes, pw_constr_type="EQ",
                                                               f_rule=list(data_dict.values())))

        return constraint

    def translate_objective(self, process_code_name, obj):
        if obj == "":
            return

        for index, objective_term in enumerate(obj.split("++")):
            unique_name = process_code_name + "__objective_term_" + str(index)
            term = objective_term.strip()
            term = term.replace("[_y_]", "[0]")
            single_resolution = True

            for resolution in list(DatasetResolution):
                resolution_letter = "_" + str(resolution)[0].lower() + "_"
                if resolution_letter in term:
                    self._model.add_component(unique_name,
                                              Expression(expr=sum(eval(term, self._variables, {resolution_letter: i})
                                                                  for i in range(resolution.value))))
                    single_resolution = False
                    break

            if single_resolution:
                self._model.add_component(unique_name, Expression(expr=eval(term, self._variables)))

            self._objective_expressions.append(self._model.component(unique_name))

    def translate_indexed_terms(self, string_list, code_name, unique_name, resolution):
        # pattern without +/- in index
        re_pattern_single_indexed = re.compile(r"\b" + re.escape(code_name) + r"\[([^+-].*?)\]", flags=re.MULTILINE)
        # pattern with +/- in index
        re_pattern_index_shift = re.compile(r"\b" + re.escape(code_name) + r"\[([+-].*?)\]", flags=re.MULTILINE)

        for index, string in enumerate(string_list):
            match_single_indexed = re.search(re_pattern_single_indexed, string)
            match_index_shift = re.search(re_pattern_index_shift, string)

            # check which pattern applies and execute corresponding translation
            if match_single_indexed:
                string_list[index] = self.translate_single_indexed_term(string, match_single_indexed, unique_name)
            elif match_index_shift:
                string_list[index] = self.translate_index_shift_term(string, match_index_shift, unique_name, resolution)
            else:
                # jump to next for loop iteration
                continue

        return string_list

    def translate_single_indexed_term(self, string, match, unique_name):
        index_variable = match[1]
        # no replacement for numbers as index
        if index_variable.isdigit():
            return string

        piecewise_function_name = unique_name + "_function"
        piecewise_output_name = unique_name + "_output"
        # replace index parameter with list output variable
        string = re.sub(match.re, piecewise_output_name, string)
        # add list output variable
        self._model.add_component(piecewise_output_name, Var())
        self._variables[piecewise_output_name] = self._model.component(piecewise_output_name)
        # add piecewise function
        self._model.add_component(piecewise_function_name,
                                  Piecewise(self._model.component(piecewise_output_name),
                                            self._model.component(index_variable),
                                            pw_pts=list(self._model.component(unique_name).keys()),
                                            pw_constr_type="EQ",
                                            f_rule=list(self._model.component(unique_name).values())))

        return string

    def translate_index_shift_term(self, string, match, unique_name, resolution):
        # todo create translation for index shifts
        return string