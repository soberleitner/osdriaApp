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
        project_longitude = PropertyLineEdit("Longitude", "0.0", "")
        project_latitude = PropertyLineEdit("Latitude", "0.0", "")
        project_location = PropertyDialog(
            "Project Location",
            List([project_longitude, project_latitude]))
        project_area = PropertyLineEdit(
            "Project Area",
            "0.0",
            "ha")
        property_list = List([project_name, project_location, project_area])

        return property_list

    @staticmethod
    def project_elements():
        commodity_list = []
        process_list = []

        return Elements(commodity_list, process_list)

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

    @staticmethod
    def time_series():
        return List([])

    @staticmethod
    def commodities():
        return List([])
