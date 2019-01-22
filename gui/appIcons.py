"""definition of all icons used in the app"""
import wx


ICON_DIRECTORY = "/Users/stefan/Dropbox/Uni/Master/Semester_04/01_master_thesis/05_OSDRIA/01_GUI/gui_icons/"

ICON_BUTTON_LIST = ["add", "back", "export", "graph",
                    "minus", "run", "scenarios", "trash"]
ICON_BUTTON_TYPES = ["normal", "select"]

ICON_TOGGLE_LIST = ["connect", "cursor", "draft", "sidebar",
                    "zoom-in", "zoom-out", "zoom-range"]
ICON_TOGGLE_TYPE = ["normal", "select_orange"]  # options: select, select_blue

ICON_IMAGE_LIST = ["new", "open", "logo"]


def init():
    """Initialise icons as class variable with both states as dictionary"""
    for button in ICON_BUTTON_LIST:
        globals()[button] = {}
        for type in ICON_BUTTON_TYPES:
            globals()[button][type] = ICON_DIRECTORY + button + "_" + type + ".png"

    for toggle in ICON_TOGGLE_LIST:
        globals()[toggle] = {}
        for type in ICON_TOGGLE_TYPE:
            globals()[toggle][type] = ICON_DIRECTORY + toggle + "_" + type + ".png"

    for image in ICON_IMAGE_LIST:
        globals()[image] = ICON_DIRECTORY + image + "@2x.png"
