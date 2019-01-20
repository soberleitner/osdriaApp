"""CLasses of custom controls"""

import wx


class Button(wx.Control):
    """Custom Button:
    @param bitmaps: dict with normal and select state bitmaps
    @param toogle:  defines toggle button (default: False)
    """
    def __init__(self, parent, bitmaps, toggle=False):
        super(Button, self).__init__(parent, -1, style=wx.BORDER_NONE)

        self.normal = bitmaps['normal']
        self.select = bitmaps['select']
        self._toggle = toggle

        self.region = wx.Region(wx.Rect(self.normal.GetSize()))

        self._selected = False
        self._hover = False

        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)

        self.Bind(wx.EVT_SIZE, self.onSize)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.onLeftUp)
        self.Bind(wx.EVT_ENTER_WINDOW, self.onEnterWindow)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.onLeaveWindow)

    def DoGetBestSize(self):
        return self.normal.GetSize()

    def Enable(self, *args, **kwargs):
        super(Button, self).Enable(*args, **kwargs)
        self.Refresh()

    def Disable(self, *args, **kwargs):
        super(Button, self).Disable(*args, **kwargs)
        self.Refresh()

    def postEvent(self):
        event = wx.CommandEvent()
        event.SetEventObject(self)
        event.SetEventType(wx.EVT_BUTTON.typeId)
        wx.PostEvent(self, event)

    def onSize(self, event):
        event.Skip()
        self.Refresh()

    def onPaint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        dc.SetBackground(wx.Brush(self.GetParent().GetBackgroundColour()))
        dc.Clear()

        bitmap = self.normal
        if (self.selected ^ self._hover):
            bitmap = self.select or bitmap
        dc.DrawBitmap(bitmap, 0, 0, True)

    def setSelected(self, selected):
        if self._toggle:
            if selected is not self._selected:
                self._selected = selected
                self.Refresh()

    def getSelected(self):
        return self._selected

    selected = property(getSelected, setSelected)

    def onLeftDown(self, event):
        x, y = event.GetPosition()
        if self.region.Contains(x, y):
            self.selected = not self.selected
            self._hover = not self._hover

    def onLeftUp(self, event):
        x, y = event.GetPosition()
        if self.region.Contains(x, y):
            self.postEvent()

    def onEnterWindow(self, event):
        self._hover = True
        self.Refresh()

    def onLeaveWindow(self, event):
        self._hover = False
        self.Refresh()
