@ECHO OFF
ECHO Convert binary image to catridge file type 
..\GTK3VICE-3.9-win64\bin\cartconv.exe -t normal -i myCartridgeImage.bin -o myCartridgeImage.crt -n "r06ert" -p
PAUSE