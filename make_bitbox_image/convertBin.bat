@ECHO OFF

ECHO Processing files and creating a new binary image 
python convertBin.py -b "bootmanager.bin" -a "application.bin" -c "myCartridgeImage.bin"
PAUSE
