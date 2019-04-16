import re

from pyomo.environ import *
import pyomo.core.kernel.set_types as var_types

from models.constants import DatasetResolution
from models.property import PropertyValueTimeSeries

SOLVER = 'glpk'


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
            # set commodity sum to zero
            code = content['com_sum'] + "==0"
            # create Constraint
            commodity_code_name = "commodity_" + commodity.lower().replace(" ", "_")
            self.translate_constraints(commodity_code_name, code)

        # add objective function
        self._model.objective = Objective(expr=sum(self._objective_expressions))

    def solve(self):
        opt = SolverFactory(SOLVER)
        results = opt.solve(self._model)
        print(results)

    def set_results(self):
        """set optimization results in processes and commodities"""
        for process in self._processes:
            process_code_name = process.name.lower().replace(" ", "_")
            for variable in process.core.variables:
                variable_code_name = variable.name.lower().replace(" ", "_")
                unique_name = process_code_name + "__" + variable_code_name
                process.optimization_output[variable] = [result for result in
                                                         self._model.component(unique_name).get_values().values()]

        # set commodity flow results
        for commodity in self._commodities:
            commodity_code_name = commodity.name.lower().replace(" ", "_")
            for process_direction in ["input_processes", "output_processes"]:
                for process_name in self._commodity_list[commodity.name][process_direction]:
                    process_code_name = process_name.lower().replace(" ", "_")
                    commodity_process_name = commodity_code_name + "__" + process_code_name
                    commodity.optimization_output[process_direction][process_name] = \
                        [result for result in self._model.component(commodity_process_name).get_values().values()]


    def cancel(self):
        pass

    def translate_variables(self, process_code_name, variables, obj, const):
        # converts variables into pyomo variables and adds them to list
        for variable in variables:
            variable_code_name = variable.name.lower().replace(" ", "_")
            unique_name = process_code_name + "__" + variable_code_name

            # add variable to declaration as pyomo Var
            self._model.add_component(unique_name, Var(range(variable.resolution.value),
                                                       within=getattr(var_types, variable.pyomo_type.value)))
            self._variables[unique_name] = self._model.component(unique_name)

            resolution_index = "[" + str(variable.resolution)[0].lower() + "]"
            re_pattern = re.compile(r"\b" + re.escape(variable_code_name) + r"\b", flags=re.MULTILINE)
            [obj, const] = [re.sub(re_pattern, unique_name + resolution_index, s) for s in [obj, const]]

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
                resolution_index = "[" + str(resolution)[0].lower() + "]"
                unique_name += resolution_index
            else:
                unique_name = str(prop.value)

            re_pattern = re.compile(r"\b" + re.escape(prop_code_name) + r"\b", flags=re.MULTILINE)
            [obj, const] = [re.sub(re_pattern, unique_name, s) for s in [obj, const]]

        return [obj, const]

    def translate_commodities(self, process_code_name, process_name, commodities, obj, const, input_com=True):
        # converts commodities into pyomo variables and adds them to list respecting the direction
        for commodity in commodities:
            commodity_code_name = commodity.name.lower().replace(" ", "_")
            unique_name = commodity_code_name + "__" + process_code_name
            if commodity.name not in self._commodity_list:
                self._commodity_list[commodity.name] = {'com_sum': "", 'input_processes': [], 'output_processes': []}

            # add variable to declaration as pyomo Var
            self._model.add_component(unique_name, Var(range(commodity.resolution.value), within=NonNegativeReals))
            self._variables[unique_name] = self._model.component(unique_name)

            resolution_index = "[" + str(commodity.resolution)[0].lower() + "]"
            re_pattern = re.compile(r"\b"+re.escape(commodity_code_name)+r"\b", flags=re.MULTILINE)
            [obj, const] = [re.sub(re_pattern, unique_name + resolution_index, s) for s in [obj, const]]

            # and commodity with -/+ as input/output to commodity sum
            commodity_direction = '-' if input_com else '+'
            self._commodity_list[commodity.name]['com_sum'] += commodity_direction + unique_name + resolution_index

            process_direction = 'input_processes' if input_com else 'output_processes'
            self._commodity_list[commodity.name][process_direction].append(process_name)

        return [obj, const]

    def translate_constraints(self, process_code_name, const):
        for index, constraint in enumerate(const.split("\n")):
            unique_name = process_code_name + "__const_" + str(index)
            constraint = constraint.replace("[y]", "[0]")

            for resolution in list(DatasetResolution):
                resolution_letter = str(resolution)[0].lower()
                if "[" + resolution_letter + "]" in constraint:
                    self._model.add_component(unique_name,
                                              Constraint(range(resolution.value),
                                                         rule=lambda model, i: eval(constraint,
                                                                                    self._variables,
                                                                                    {resolution_letter: i})))
                    break

    def translate_objective(self, process_code_name, obj):
        if obj == "":
            return obj

        for index, objective_term in enumerate(obj.split("+")):
            unique_name = process_code_name + "__objective_term_" + str(index)
            term = objective_term.strip()
            term = term.replace("[y]", "[0]")
            single_resolution = True

            for resolution in list(DatasetResolution):
                resolution_letter = str(resolution)[0].lower()
                if "[" + resolution_letter + "]" in term:
                    self._model.add_component(unique_name,
                                              Expression(expr=sum(eval(term, self._variables, {resolution_letter: i})
                                                                  for i in range(resolution.value))))
                    single_resolution = False
                    break

            if single_resolution:
                self._model.add_component(unique_name, Expression(expr=eval(term, self._variables)))

            self._objective_expressions.append(self._model.component(unique_name))
