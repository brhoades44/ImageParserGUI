###########################################################################################
# Bruce Rhoades
#
# Image Manager class to parse .jpg files and find make and model encoded within the .jpg
# file. No third party library used. Older jpg specification - not guaranteed to work on 
# newer ones. 
###########################################################################################

class ImageManager:
    __endian = ''
    __cameraMake = ''
    __cameraModel = ''
    __app1Offset = 12
    __cameraMakeTagID = 271
    __cameraModelTagID = 272

    
    ###########################################################################################
    # Initialize with a fully quantified fileName or one in current working directory
    ###########################################################################################
    def __init__(self, fileName):
        self.__fileName = fileName
 
    @property
    def fileName(self):
        return self.__fileName    

    @fileName.setter
    def fileName(self, fileName):
        self.__fileName = fileName
    
    @property
    def endian(self):
        return self.__endian    

    @property
    def cameraMake(self):
        return self.__cameraMake 

    @property
    def cameraModel(self):
        return self.__cameraModel    

    
    ###########################################################################################
    # Method to parse the image sent with constructor to find the make and model of jpg
    ###########################################################################################
    def parseImage(self):
        print("\nParsing: ", self.__fileName)
        try:
            with open(self.__fileName, mode='rb+') as imageFile:
                self.setEndian(imageFile)
                imageFile.seek(self.__app1Offset + 4)
                zeroethIFDOffset = int.from_bytes(imageFile.read(4), self.__endian)
                zeroIFD = True
                if(zeroethIFDOffset > 0):
                    self.__readIFD(imageFile, zeroethIFDOffset, zeroIFD)

        except OSError as osErr:
            print("OS error in ImageManager::loadImage(): {0}".format(osErr))
            raise
        except Exception as err:
            print("Unknown error in ImageManager::loadImage(): {0}".format(err))
            raise

    
    ###########################################################################################
    # Method to set the endian value of the inputted jpeg file content
    ############################################################################################
    def setEndian(self, imageFile):
        try:
            imageFile.seek(self.__app1Offset)
            endianBytes = imageFile.read(2)
            if(endianBytes == b"II"):
                self.__endian = 'little'
            else:
                self.__endian = 'big'

        except Exception as err:
            print("Unknown error in ImageManager::setEndian(): {0}".format(err))
            raise

    
    ###########################################################################################
    # Method to read an IFD sector given jpg image contents and an offset
    ############################################################################################
    def __readIFD(self, imageFile, offset, zeroIFD):
        dataTagCt = 0
        dataTagID = 0
        dataCount = 0
        dataOffset = 0
        nextIFDOffset = 0
        oldArrayPos = 0
        totalMetaTags = 0

        try:    
            # set position to start of IFD section and iterate over data tags
            imageFile.seek(self.__app1Offset + offset)
            dataTagCt = int.from_bytes(imageFile.read(2), self.__endian)
            totalMetaTags += dataTagCt
            for i in range(dataTagCt):
                # get data tags
                dataTagID = int.from_bytes(imageFile.read(2), self.__endian)
                imageFile.seek(2, 1)
                dataCount = int.from_bytes(imageFile.read(4), self.__endian)
                dataOffset = int.from_bytes(imageFile.read(4), self.__endian)
                # see if any data tags are camera make, model
                self.__readData(imageFile, dataTagID, dataCount, dataOffset)

            # last item in Zeroeth IFD is ExifIFD Pointer
            if(zeroIFD == True):
                zeroIFD = False
                oldArrayPos = imageFile.tell()
                if(dataOffset > 0):
                    self.__readIFD(imageFile, dataOffset, zeroIFD)
            
                imageFile.seek(oldArrayPos)
            
            # get next IFD Chunk
            nextIFDOffset = int.from_bytes(imageFile.read(2), self.__endian)
            if(nextIFDOffset > 0):
                self.__readIFD(imageFile, nextIFDOffset, zeroIFD)

        except Exception as err:
            print("Unknown error in ImageManager::__readIFD(): {0}".format(err))
            raise


    ###########################################################################################
    # Check data tag to see if it matches the camera make/model tag ID and set data members
    # accordingly
    ###########################################################################################
    def __readData(self, imageFile, tagID, count, offset):
        try:
            oldArrayPos = imageFile.tell()
            imageFile.seek(self.__app1Offset + offset)
            if(tagID == self.__cameraMakeTagID):
                self.__cameraMake = imageFile.read(count).decode('ascii')
            
            if(tagID == self.__cameraModelTagID):
                self.__cameraModel = imageFile.read(count).decode('ascii')
                
            imageFile.seek(oldArrayPos)

        except Exception as err:
            print("Unknown error in ImageManager::__readData(): {0}".format(err))
            raise

    ###########################################################################################
    # Given an Exception object, print its error information
    ###########################################################################################
    @staticmethod
    def printMoreErrInfo(err):
        print("Exception Type : {0}".format(type(err)))
        print("Exception Args : {0}".format(err.args))
        print("Exception: {0}".format(err))


