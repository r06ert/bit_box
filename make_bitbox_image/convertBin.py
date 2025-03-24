# @author: Robert Zdunek
# @project: make bit box image
# @date: 16.03.2025

import numpy as np
import sys 
import getopt 

BASIC_START_ADDRESS = 0x0801    #default start address of BASIC applicantion
ROM_START_ADDRESS = 0x8000      #default start address of cartridge area
ROM_BANK_SIZE = 0x2000          #default cartridge bank size (valid 8192 or 16384 bytes)
DUMMY_BYTE = 0xFF               #dummy byte, used to fill binary image

class binaryData(object):

    # @brief binary object constructor
    # @param none
    # @return none
    def __init__(self):
        self.aBinaryData = bytearray([])
        self.sFileName = "new"
    
    # @brief Open binary file
    # @param sFile[in] patch and file name
    # @return none
    def OpenFile(self, sFile):
        f = open(sFile, 'rb')
        try:
            binFile = f.read()
            self.aBinaryData = bytearray(binFile)
            self.sFileName = sFile
            print("file: " + sFile + " has been opened")
            print("file: " + self.sFileName + " is " +  str(len(self.aBinaryData)) + " bytes long")
        finally:
            f.close()
    
    # @brief Save binary data to binary file
    # @param sFile[in] patch and file name
    # @return none  
    def SaveFile(self, sFile):
        print("file: " + self.sFileName + " is " +  str(len(self.aBinaryData)) + " bytes long")
        print("file: " + self.sFileName + " has been saved to a file: " + sFile)
        aBinaryData = np.array(self.aBinaryData)
        binaryData = aBinaryData.tofile(sFile)
    
    # @brief Find end of BASIC program and remove data after
    # @param none
    # @return none      
    def FindProgramEnd(self):
        i = 0
        zeroOcurrence = 0
        while (len (self.aBinaryData)):
            #fine end of the BASIC program 
            if (zeroOcurrence == 3):
                #found three zeros in a row - end of BASIC program
                print("file: " + self.sFileName + ", last " + str(len(self.aBinaryData) - (i+1)) + " bytes have been removed")
                print("file: " + self.sFileName + " is " +  str(i+1) + " bytes long")
                self.aBinaryData = self.aBinaryData[:i+1]
                break
            elif (self.aBinaryData[i] == 0):
                #count zeros in binary image
                zeroOcurrence = zeroOcurrence + 1
            else:
                #clear zeros counter 
                zeroOcurrence = 0
                
            # byte counter
            i = i+1

    # @brief Set new offset address of BASIC program
    # @param newOffset[in] new offset value (address)
    # @return none 
    def SetProgramOffset(self, iNewOffset):
        iCurrentOffset = BASIC_START_ADDRESS
        iNewOffset = iNewOffset
        iCurrentAddressVal = 0
        iNextAddressVal = 0
        
        print("file: " + self.sFileName + " offset has been changed")
        while (True):

            # find next line-link address in a binary file
            iNextAddressVal = ((self.aBinaryData[iCurrentAddressVal+1] * 256) + self.aBinaryData[iCurrentAddressVal]) - iCurrentOffset
            
            print("\t two byte word at address " + hex(iCurrentAddressVal) + " has been changed: " + hex((self.aBinaryData[iCurrentAddressVal+1] * 256) + self.aBinaryData[iCurrentAddressVal]) + "->", end="" )
            
            # set next line-link address in a binary file as current
            self.aBinaryData[iCurrentAddressVal+1] = int((iNextAddressVal + iNewOffset) / 256)
            self.aBinaryData[iCurrentAddressVal] = int((iNextAddressVal + iNewOffset) % 256)
            
            print(hex((self.aBinaryData[iCurrentAddressVal+1] * 256) + self.aBinaryData[iCurrentAddressVal]))
            
            # go to current line-link address in a binary file
            iCurrentAddressVal = iNextAddressVal
            
            #check if line-link value = 0, then this is the end of BASIC program
            if(((self.aBinaryData[iCurrentAddressVal+1] * 256) + self.aBinaryData[iCurrentAddressVal]) == 0):
                break
                
    # @brief Add binary data to already existing
    # @param file[in] - binary data which will be added
    # @return none  
    def AddData(self, sFile):
        self.aBinaryData = self.aBinaryData + sFile.aBinaryData
        print("file: " + self.sFileName + ", file " + sFile.sFileName + " has been added")
    
    # @brief Aligne binary image size and fill new bytes by a given value
    # @param size[in] - size to which the binary data will be aligned
    # @param byte[in] - binary data with which the file will be filled 
    # @return none 
    def AlignData(self, iSize, iByte):
        for i in range(len(self.aBinaryData), iSize):
            self.aBinaryData.append(iByte)
        print("file: " + self.sFileName + ", data has been aligned to: " + str(len(self.aBinaryData)) + " bytes" )
    
    # @brief Get binary data size 
    # @param none
    # @return size ofthe binary data in bytes
    def GetDataLenght(self):
        return len(self.aBinaryData)

# @brief Get parameter from command line
# @param sOption[in] parameter name
# @return parameter value of a given parameter name
def GetOptions(sOption):
    try: 
        opts, args = getopt.getopt(sys.argv[1:], "b:a:c:") 
    except getopt.GetoptError as err: 
        print(f"Error: {err}") 
        sys.exit(1) 
        
    for opt, arg in opts: 
        if (opt in ("-b", "--bootmanager")) and (sOption == "bootmanager"): 
            return str(arg)
        elif (opt in ("-a", "--application")) and (sOption == "application"):
            return str(arg)
        elif (opt in ("-c", "--cartridge")) and (sOption == "cartridge"): 
            return str(arg)
            
if __name__ == "__main__":
    
    bootmanagerFile = ""
    applicationFile = ""
    cartridgeFile = ""
    
    #get patch and file names
    bootmanagerFile = GetOptions("bootmanager")
    applicationFile = GetOptions("application")
    cartridgeFile = GetOptions("cartridge")
    
    #process bootmanager binary data
    bootmanager = binaryData()
    bootmanager.OpenFile(bootmanagerFile)
    
    #process application binary data
    application = binaryData()
    application.OpenFile(applicationFile)
    application.FindProgramEnd()
    application.SetProgramOffset(ROM_START_ADDRESS + bootmanager.GetDataLenght())
    
    #process cartridge binary data
    cartridge = binaryData()
    cartridge.AddData(bootmanager)
    cartridge.AddData(application)
    cartridge.AlignData(ROM_BANK_SIZE, DUMMY_BYTE)
    cartridge.SaveFile(cartridgeFile)