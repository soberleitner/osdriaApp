from models.property import *
from models.data_structure import List
from models.scenario import Scenario
from models.elements import Elements
from models.element import *
from models.constants import *


class ModelTemplate(object):
    """initialising values for model"""

    @staticmethod
    def overview_properties():
        project_name = PropertyLineEdit(
            "Project Name",
            "Name")
        project_longitude = PropertyValue("Longitude", "0.0", "")
        project_latitude = PropertyValue("Latitude", "0.0", "")
        project_location = PropertyDialog(
            "Project Location",
            List([project_longitude, project_latitude]))
        project_area = PropertyLineEdit(
            "Project Area",
            "0.0",
            "ha")
        timeline_values_1 = List(["3", "5", "10"])
        timeline_values_2 = List(["30", "50", "100"])
        timeline_values_3 = List(["300", "500", "1000"])
        timeline_1 = PropertyValueTimeSeries("Timeline 1", timeline_values_1, "kW")
        timeline_2 = PropertyValueTimeSeries("Timeline 2", timeline_values_2, "kW")
        timeline_3 = PropertyValueTimeSeries("Timeline 3", timeline_values_3, "kW")
        project_timeline = PropertyPopupMenu("Project Timeline",
                                             List([timeline_1, timeline_2, timeline_3]))
        property_list = Dict({'name': project_name,
                              'location': project_location,
                              'area': project_area,
                              'timeline': project_timeline})

        return property_list

    @staticmethod
    def project_elements():
        sub_com_1 = SubCommodity("General Electricity")
        sub_com_2 = SubCommodity("Irrigation Water")
        sub_com_3 = SubCommodity("Domestic Water")
        commodity_1 = Commodity("Electricity", "", List([sub_com_1]))
        commodity_2 = Commodity("Water", "", List([sub_com_2, sub_com_3]))
        core_1 = ProcessCore()
        core_1.category = ProcessCategory.SUPPLY
        core_1.section = OverviewSelection.ENERGY
        core_1.properties = List([])
        core_2 = ProcessCore()
        process_1 = Process("Photovoltaic system 1", QPoint(0, 0), core_1)
        process_2 = Process("Water Pump 1", QPoint(50, 0), core_2)
        commodity_list = List([commodity_1, commodity_2])
        process_list = List([process_1, process_2])
        elements_list = Elements(commodity_list, process_list)

        return elements_list

    @staticmethod
    def scenarios():
        scenario_1 = Scenario("Base scenario", List())
        scenario_2 = Scenario("Extra long scenario name requiring a lot of space", List())
        scenario_3 = Scenario("Another scenario", List())
        scenario_4 = Scenario("Yet, another one", List())
        scenario_list = PropertyPopupMenu("Scenarios", List([scenario_1,
                                                             scenario_2,
                                                             scenario_3,
                                                             scenario_4]))

        return scenario_list

    @staticmethod
    def process_cores():
        return List([])
