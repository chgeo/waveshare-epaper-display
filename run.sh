
. env.sh

figlet Weather info
sudo -E python3 screen-weather-get.py

figlet Calendar info
sudo -E python3 screen-calendar-get.py

figlet Stock info
sudo -E python3 screen-stocks-get.py

figlet Export
# Inkscape can't export to BMP, so let's export to PNG first. 
inkscape  screen-output-weather.svg --without-gui -e screen-output.png -w880 -h528 --export-dpi=150

# Convert to a black and white, 1 bit bitmap
convert -colors 2 +dither -type Bilevel -monochrome screen-output.png screen-output.bmp

SHOULD_REFRESH=0
current_hour=`date +"%H"`
current_minute=`date +"%M"`

figlet Display
sudo python3 display.py screen-output.bmp 
