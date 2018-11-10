# TouchSelfie
Open Source Photobooth forked and improved from [laurentalacoque/TouchSelfie-extended](https://github.com/laurentalacoque/TouchSelfie-extended)

For hardware construction, see [Make Magazine article](https://makezine.com/projects/raspberry-pi-photo-booth/)

## Take a shortcut:
- [What's new?](#changes)
- [Installation](#install)


## <a id="changes"></a>Changes from [laurentalacoque/TouchSelfie-extended](https://github.com/laurentalacoque/TouchSelfie-extended)

### Hardware Buttons 
- If a hardware button is available, the software buttons are not displayed. 

### Functionality
-The Snap Mode directly prints the photo taken.

### MP3 Script
Added a script that plays an MP3 from a directory when printing a hardware button. The directory must be configured in Configurations.json. Press the button again to play the next song.



## <a id="install"></a>Installing (extracted and adapted from [Make Magazine](https://makezine.com/projects/raspberry-pi-photo-booth/))

### Get the necessary packages

```
# update system
sudo apt-get update

# Install ImageTk, Image from PIL
sudo apt-get install python-imaging
sudo apt-get install python-imaging-tk

# Install google data api and upgrade it
sudo apt-get install python-gdata
sudo pip install --upgrade google-api-python-client
sudo pip install --upgrade oauth2client

# Install ImageMagick for the 'Animation' mode
sudo apt-get install imagemagick

# Install CUPS for the Printing function(optional)
sudo apt-get install cups
sudo apt-get install python-cups

# Setting up  CUPS/printer(optional)
https://www.techradar.com/how-to/computing/how-to-turn-the-raspberry-pi-into-a-wireless-printer-server-1312717
Test device:
Canon Selphy CP1300 with the Canon SELPHY CP900 - CUPS+Gutenprint v5.2.11  driver over USB

```

If google chrome is not on your system, the following might be necessary:

```
sudo apt-get install luakit
sudo update-alternatives --config x-www-browser
```

### Configure the program

1. run `setup.sh` script, this will:
  - guide you through the feature selection (email feature, upload feature)
  - Google credentials retrieval and installation
  - Google Photos album selection
  - and will create a `photobooth.sh` launcher

2. `setup.sh` creates a configuration file `scripts/configuration.json`, you can edit this file to change configuration parameters, such as:
  - the logo file to put on your pictures
  - email subject and body
  - wether or not to archive snapshots locally
  - where to store pictures locally

3. Optionally you can change lower-level configuration options in the file `scripts/constants.py` such as:
  - captured image sizes
  - hardware dependent things




