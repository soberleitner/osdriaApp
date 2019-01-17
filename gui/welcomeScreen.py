import wx
import appColors as col

WELCOME_SCREEN_HEIGHT_RATIO = 2


class WelcomeScreen(wx.Frame):
    """Creation of the Welcome Screen
    includes interaction for creating new file
    as well as opening existing file
    """
    def __init__(self):
        super(WelcomeScreen, self).__init__(parent=None, style=wx.CLOSE_BOX)
        self.initUI()

    def initUI(self):
        # define frame design
        _screenHeight = wx.DisplaySize()[1] / WELCOME_SCREEN_HEIGHT_RATIO
        self.SetSize(_screenHeight, _screenHeight)
        self.Centre()

        # define panel design
        panel = wx.Panel(self)
        panel.SetBackgroundColour(col.WHITE)

        # define content structure
        #verticalSizer = wx.BoxSizer(wx.VERTICAL)

        #verticalSizer.Add()
