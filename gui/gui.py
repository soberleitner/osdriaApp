import wx
from welcomeScreen import WelcomeScreen


def osdriaApp():
    """Run GUI"""
    osdria = wx.App()
    screen = WelcomeScreen()
    screen.Show()
    osdria.MainLoop()


if __name__ == '__main__':
    osdriaApp()
