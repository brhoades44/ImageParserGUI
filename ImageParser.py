
###########################################################################################
# Bruce Rhoades - Image Parser application  
#
# Application built with the wxPython GUI module which is a wrapper around the C++ library
# called wxWidgets. 
#
# wxPython's primary difference from other Python GUI toolkits is that it uses the actual 
# widgets on native platforms whenever possible, making applications look native to the
# operating system it is running on. PyQt and Tkinter draw their widgets themselves which
# is why they do not always match native widgets although PyQt is very close
#
# wxPython does support custom widgets and operates on an event loop which runs infinitely
#
# This application uses Absolute positioning of widgets. Dynamic sizing is preferred for 
# larger applications where managing sizing, alignment and such is accomplished through
# layout components:
#       wx.BoxSizer (to orient widgets horizontally or vertically)
#       wx.StaticBoxSizer - derived from BoxSizer but adds a static box around the sizer
#       wx.GridSizer (to orient widgets in two-dimensional table - width of each field is
#                     the width of the widest child, height is that of the tallest child)
#       wx.FlexGridSizer (to orient widgets in a two-dimensional table - all fields in one
#                       row having the same height and all fields in one column having the 
#                       same width but all rows and columns are not necessarily the same
#                       height or width as in wx.GridSizer)
#       wx.GridBagSizer - lays out items in a virtual grid like FlexGridSizer, but here
#                       explicit positioning of the items is allowed using GBPosition
#                       and items can span more than one row/column using GBSpan
#
#   Inheritance: wx.Object -> wx.EvtHandler -> wx.Window -> wx.Control -> wx.Button
#
#  app = wx.App() - To instantiate the application object
#  frame = ImageFrame() - To create the top-level parent widget for other widgets. It has 
#       no parent. Actually it can contain any window that is not a frame or dialog. 
#       wx.Frame consists of a title bar, borders and a central container area. The title bar 
#       and borders are optional.
#  app.MainLoop() -  To enter the mainloop. The mainloop is an endless cycle. It catches and 
#                    dispatches all events that exist during the life of our application.
###########################################################################################

import wx
import ImagePanel as ip

###########################################################################################
# Top level frame to host the application. It hosts the ImagePanel which is a container
# for many of the widgets in the application as well as the frame's menu. The frame is then 
# centered on the screen
###########################################################################################
class ImageFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None,
                         title='Image Parser',
                         size=(740,700))
        self.panel = ip.ImagePanel(self)
        self.createMenu()
        self.Show()
        self.Centre()

    ###########################################################################################
    # Method to create a menu bar to host a file menu 
    ###########################################################################################
    def createMenu(self):
        # Create a menu bar with a File Menu item to open a folder
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()

        # append an Open Folder menu item to the file menu with the help string
        # can also be a separator, checkbox or radio ('kind' parameter at the end)
        openFolderMenuItem = fileMenu.Append(
            wx.ID_ANY, 'Open Folder', 
            'Open a folder with JPEGs'
        )

        # append fileMenu with a caption to the menu bar
        # bind EVT_MENU to openFolderMenuItem method
        menuBar.Append(fileMenu, '&File')
        self.Bind(
            event=wx.EVT_MENU, 
            handler=self.onOpenFolder,
            source=openFolderMenuItem,
        )

        # Attach and show the menu on the frame
        self.SetMenuBar(menuBar)

    ###########################################################################################
    # Open Folder menu item handler to display a directory selection dialog box
    ###########################################################################################
    def onOpenFolder(self, event):
        title = "Choose a directory:"
        dlg = wx.DirDialog(self, title, 
                           style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            # update file location chosen by user on the Image Panel
            path = dlg.GetPath()
            self.panel.updateFileLocation(path)
            self.panel.updateImageListing(path)
            self.panel.clearLabels()
            self.panel.hideImage()
        dlg.Destroy()

if __name__ == '__main__':
    app = wx.App(False)
    frame = ImageFrame()
    app.MainLoop()