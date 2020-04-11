# Automatic beam light system using Raspberry Pi
This is a project realized for the **embedded microcomputer systems programming** course at my school. It is an automatic beam light system for a car, using **OpenCV** for light detection and **Raspberry Pi** for GPIO control.
## Table of contents
* [Automatic beam light system using Raspberry Pi](#automatic-beam-light-system-using-raspberry-pi)
    * [Table of contents](#table-of-contents)
    * [Hardware requirements](#hardware-requirements)
    * [Software dependencies](#software-dependencies)
    * [Downloading and running the application](#downloading-and-running-the-application)
        * [Command-line arguments](#command-line-arguments)


## Hardware requirements
This project requires you to have a Raspberry Pi (3 Model B was used for the realization, but any Pi should work) and a camera, connected to the SBC's CSI interface.

## Software dependencies
The following dependencies must be installed in order to be able to run this system:
* argparse
* imutils
* OpenCV
* picamera
* skimage

## Downloading and running the application
Since the program is written in Python, it doesn't require any build procedures. Ensure the above-mentioned dependencies are installed and run the following commands in the Pi's terminal:
```console
$ git clone https://github.com/TheRandomTroll/emcsp-project
$ cd emcsp-project
$ python main.py --left-relay {LEFT_RELAY_PIN} --right-relay {RIGHT_RELAY_PIN}
```
### Command-line arguments
As seen in the command snippet above, the `main.py` file has arguments, which are as follows:
* Mandatory arguments:
	* `-lr, --left-relay` --  left relay GPIO pin
    * `-rr, --right-relay` -- right relay GPIO pin
* Optional arguments:
	* `-s, --sensitivity` -- number of pixels required to be considered a **bright spot**
	* `-t, --threshold` -- how bright a pixel has to be to be considered **bright**
