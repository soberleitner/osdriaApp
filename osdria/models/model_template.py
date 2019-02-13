from models.property import *
from models.constants import PropType
from models.data_structure import List
from models.scenario import Scenario


class ModelTemplate(object):
    """initialising values for model"""

    @staticmethod
    def overview_properties():
        project_name = PropertyLineEdit(
            "Project Name",
            "Name")
        project_longitude = PropertyValue("0.0", "")
        project_latitude = PropertyValue("0.0", "")
        project_location = PropertyDialog(
            "Project Location",
            {"Longitude": project_longitude, "Latitude": project_latitude})
        project_area = PropertyLineEdit(
            "Project Area",
            "0.0",
            "ha")
        property_list = [project_name, project_location, project_area]

        return property_list

    @staticmethod
    def scenarios():
        scenario = Scenario("Base scenario", List())
        scenario_list = List([scenario])

        return scenario_list
