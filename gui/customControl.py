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

        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_ENTER_WINDOW, self.on_enter_window)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave_window)

    def DoGetBestSize(self):
        return self.normal.GetSize()

    def Enable(self, *args, **kwargs):
        super(Button, self).Enable(*args, **kwargs)
        self.Refresh()

    def Disable(self, *args, **kwargs):
        super(Button, self).Disable(*args, **kwargs)
        self.Refresh()

    def post_event(self):
        event = wx.CommandEvent()
        event.SetEventObject(self)
        event.SetEventType(wx.EVT_BUTTON.typeId)
        wx.PostEvent(self, event)

    def on_size(self, event):
        event.Skip()
        self.Refresh()

    def on_paint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        dc.SetBackground(wx.Brush(self.GetParent().GetBackgroundColour()))
        dc.Clear()

        bitmap = self.normal
        if (self.selected ^ self._hover):
            bitmap = self.select or bitmap
        dc.DrawBitmap(bitmap, 0, 0, True)

    def set_selected(self, selected):
        if self._toggle:
            if selected is not self._selected:
                self._selected = selected
                self.Refresh()

    def get_selected(self):
        return self._selected

    selected = property(get_selected, set_selected)

    def on_left_down(self, event):
        x, y = event.GetPosition()
        if self.region.Contains(x, y):
            self.selected = not self.selected
            self._hover = not self._hover

    def on_left_dclick(self, event):
        self.on_left_down(event)

    def on_left_up(self, event):
        x, y = event.GetPosition()
        if self.region.Contains(x, y):
            self.post_event()

    def on_enter_window(self, event):
        self._hover = True
        self.Refresh()

    def on_leave_window(self, event):
        self._hover = False
        self.Refresh()
