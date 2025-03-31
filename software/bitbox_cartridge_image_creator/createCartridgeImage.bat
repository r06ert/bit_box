@ECHO OFF

ECHO Processing files and creating a new binary image 
python createCartridgeImage.py -b "bootmanager.bin" -a "application.bin" -c "cartridge.bin"
PAUSE
