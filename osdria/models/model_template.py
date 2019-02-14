from models.property import *
from models.data_structure import List
from models.scenario import Scenario


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
        property_list = [project_name, project_location, project_area, project_timeline]

        return property_list

    @staticmethod
    def scenarios():
        scenario = Scenario("Base scenario", List())
        scenario_list = List([scenario])

        return scenario_list
