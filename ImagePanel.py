###########################################################################################
# Bruce Rhoades - Image Panel Class to Display Widgets relative to selection, display
# and parsing of jpeg files for their camera make and model
###########################################################################################

import os
import wx
import wx.adv

import ImageManager as im

class ImagePanel(wx.Panel): 
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        # file list to store absolute paths to jpeg files
        self.fileList = []

        # Button to parse the jpeg files for the camera make/model info
        parseBtn = wx.Button(self, wx.ID_ANY, 'Parse', (340, 53))
        parseBtn.Bind(wx.EVT_BUTTON, self.onParseBtnPress)

        # static text widgets to store the instructions/directory selection, make and model camera info of parse jpeg
        self.dirTxt = wx.StaticText(self, -1, 'Please Select a JPG File Location Using the File Menu Above', (10, 20), (500, 20))
        self.makeTxt = wx.StaticText(self, -1, '', (440, 50), (100, 20))
        self.modelTxt = wx.StaticText(self, -1, '', (440, 70), (300, 20))

        # bitmap combo box dro down to store the jpegs store in nested folders within selected one
        self.imageFileCb = wx.adv.BitmapComboBox(self, pos=(15,55), size=(300,-1), style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.imageFileCb)

        # to hold the selected image of the jpeg file
        self.bitmap = wx.StaticBitmap()

    ###########################################################################################
    # File listing combo box handler. 
    ###########################################################################################
    def EvtComboBox(self, evt):
        cb = evt.GetEventObject()

        # clear the camera make/model labels, save the selected jpg file path and hide the image
        self.clearLabels()
        self.fullPath = self.fileList[cb.GetSelection()]
        self.bitmap.Hide()

        # construct a new image and show it 
        jpg = wx.Image(self.fullPath, wx.BITMAP_TYPE_JPEG)
        self.bitmap = wx.StaticBitmap(self, wx.ID_ANY, jpg.ConvertToBitmap(), (15,100), (640,480))
        self.bitmap.Show()

    ###########################################################################################
    # Method to clear out the camera make and model fields
    ###########################################################################################    
    def clearLabels(self):
        self.makeTxt.SetLabel("")
        self.modelTxt.SetLabel("")

    ###########################################################################################
    # Mehthod to hide the selected image
    ###########################################################################################
    def hideImage(self):
        self.bitmap.Hide()
    
    ###########################################################################################
    # Update the directory field with the selected folder chosen by the user
    ###########################################################################################
    def updateFileLocation(self, fileLocation):
        self.dirTxt.SetLabel("JPG File Location: " + fileLocation)
    
    ###########################################################################################
    # Handler to Parse the selected jpeg file and display the camera make/model
    ###########################################################################################
    def onParseBtnPress(self, event):
        if(self.bitmap.IsShown() == True):
            parsedImage = im.ImageManager(self.fullPath)
            parsedImage.parseImage()
            self.makeTxt.SetLabel("Camera Make: " + parsedImage.cameraMake)
            self.modelTxt.SetLabel("Camera Model: " + parsedImage.cameraModel)
    
    ###########################################################################################
    # Method to accept a folder path and recursively traverse its folder structure and 
    # collect all jpg files adding them and scaled down image to combo box
    ###########################################################################################
    def updateImageListing(self, folder_path):
        self.imageFileCb.Clear()
        self.fileList.clear()
        # iterate through all folders in path
        for root, _, files in os.walk(folder_path):
            for file in files:
                if(file.find(".jpg") > -1):
                    # add full path to list and show scaled down image and filename in 
                    # list portion of combo box
                    fullPath = os.path.join(root, file)
                    self.fileList.append(fullPath)
                    jpg = wx.Image(fullPath, wx.BITMAP_TYPE_JPEG)
                    jpg.Rescale(20,20)
                    bmp = jpg.ConvertToBitmap()
                    self.imageFileCb.Append(file, bmp)
