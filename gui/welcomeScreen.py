import wx
import appColors as col
import appTexts as txt
import appIcons as icn


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

        # create content
        logo = wx.StaticBitmap(panel, bitmap=icn.logo)
        welcomeText = wx.StaticText(panel, label=txt.WELCOME)
        createButton = ProjectButton(panel, icn.new, txt.CREATE_PROJECT)
        openButton = ProjectButton(panel, icn.open, txt.OPEN_PROJECT)

        # define content structure
        verticalSizer = wx.BoxSizer(wx.VERTICAL)
        verticalSizer.Add(0, 10, 0)
        verticalSizer.Add(logo, 0, wx.SHAPED | wx.ALIGN_CENTER)
        verticalSizer.Add(welcomeText, 0, wx.SHAPED | wx.ALIGN_CENTER)
        verticalSizer.Add(createButton, 0, wx.ALIGN_LEFT)
        verticalSizer.Add(openButton, 0, wx.ALIGN_LEFT)

        horizontalSizer = wx.BoxSizer()
        horizontalSizer.AddStretchSpacer()
        horizontalSizer.Add(verticalSizer, 0, wx.ALIGN_CENTER)
        horizontalSizer.AddStretchSpacer()
        panel.SetSizer(horizontalSizer)


class ProjectButton(wx.Panel):
    """Entry level project buttons
    including icon, title and subtext"""
    def __init__(self, parent, icon, text):
        super(ProjectButton, self).__init__(parent)
        self.icon = wx.StaticBitmap(self, bitmap=icon)
        self.title = wx.StaticText(self, label=text['main'])
        self.sub = wx.StaticText(self, label=text['sub'])

        # vertical sizer for title and subtext
        verticalSizer = wx.BoxSizer(wx.VERTICAL)
        verticalSizer.Add(self.title, 0, wx.ALIGN_LEFT)
        verticalSizer.Add(self.sub, 0, wx.ALIGN_LEFT)

        # horizontal sizer for icon and text
        horizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        horizontalSizer.Add(self.icon, 0, wx.ALIGN_CENTER)
        horizontalSizer.Add(verticalSizer, 0, wx.ALIGN_LEFT)
        self.SetSizer(horizontalSizer)

        # change cursor type when entering the window
        self.Bind(wx.EVT_ENTER_WINDOW, self.onEnterWindow)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.onLeaveWindow)

    def onEnterWindow(self, event):
        handCursor = wx.Cursor(wx.CURSOR_HAND)
        self.GetParent().SetCursor(handCursor)

    def onLeaveWindow(self, event):
        arrowCursor = wx.Cursor(wx.CURSOR_ARROW)
        self.SetCursor(arrowCursor)
