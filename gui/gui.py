import wx
import appIcons as icn
from welcomeScreen import WelcomeScreen


def osdriaApp():
    """Run GUI"""
    osdria = wx.App()
    icn.init()  # load icons from files
    screen = WelcomeScreen()
    screen.Show()
    osdria.MainLoop()


if __name__ == '__main__':
    osdriaApp()
