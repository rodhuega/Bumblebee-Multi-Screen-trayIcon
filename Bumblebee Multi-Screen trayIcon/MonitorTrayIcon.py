import wx
import os
import threading

TRAY_TOOLTIP = 'Extra Display'
TRAY_ICON_OFF = 'monitorOFF.png'
TRAY_ICON_ON = 'monitorON.png'

isOff = True


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item

def encenderMonitor():
         os.system('intel-virtual-output') 

class TaskBarIcon(wx.TaskBarIcon):
    
    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON_OFF)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        global isOff
        if isOff:
            create_menu_item(menu, 'Turn On', self.on_TurnOn)
        else:    
            create_menu_item(menu, 'Turn Off', self.on_TurnOff)

        isOff=not isOff    
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):
        x=0

    def on_TurnOn(self, event):
        self.set_icon(TRAY_ICON_ON)
        t1= threading.Thread(target=encenderMonitor,args=())
        t1.start()
        #os.system('intel-virtual-output -f')
    
    def on_TurnOff(self, event):
        self.set_icon(TRAY_ICON_OFF)
        os.system('killall intel-virtual-output')

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()

    

class App(wx.App):
    def OnInit(self):
        frame=wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)
        return True

def main():
    app = App(False)
    app.MainLoop()


if __name__ == '__main__':
    main()