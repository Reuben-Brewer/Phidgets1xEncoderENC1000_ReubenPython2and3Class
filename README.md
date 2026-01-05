########################

Phidgets1xEncoderENC1000_ReubenPython2and3Class

Wrapper (including ability to hook to Tkinter GUI) to control Quadrature Encoder Phidget ENC1000 (VINT).

From Phidgets' website:
"The Quadrature Encoder Phidget interfaces with any 5V quadrature encoder. 
A quadrature encoder is the most commonly used feedback device for a DC or stepper motor. 
With an encoder, you can keep track of how far your motor has turned, 
which then allows you to control the position and velocity in your code. 
This Phidget connects to your computer through a VINT Hub."

Quadrature Encoder Phidget

ID: ENC1000_0

https://www.phidgets.com/?tier=3&catid=4&pcid=2&prodid=959

Reuben Brewer, Ph.D.

reuben.brewer@gmail.com

www.reubotics.com

Apache 2 License

Software Revision J, 12/31/2025

Verified working on:

Python 3.12/13.

Windows 10/11 64-bit

Raspberry Pi Bookworm

(no Mac testing yet)

*NOTE THAT YOU MUST INSTALL BOTH THE Phidget22 LIBRARY AS WELL AS THE PYTHON MODULE.*

########################  

########################### Python module installation instructions, all OS's

Phidgets1xEncoderENC1000_ReubenPython2and3Class, ListOfModuleDependencies: ['LowPassFilter_ReubenPython2and3Class', 'Phidget22', 'ReubenGithubCodeModulePaths']

Phidgets1xEncoderENC1000_ReubenPython2and3Class, ListOfModuleDependencies_TestProgram: ['MyPrint_ReubenPython2and3Class', 'ReubenGithubCodeModulePaths']

Phidgets1xEncoderENC1000_ReubenPython2and3Class, ListOfModuleDependencies_NestedLayers: ['numpy']

Phidgets1xEncoderENC1000_ReubenPython2and3Class, ListOfModuleDependencies_All:['LowPassFilter_ReubenPython2and3Class', 'MyPrint_ReubenPython2and3Class', 'numpy', 'Phidget22', 'ReubenGithubCodeModulePaths']

https://pypi.org/project/Phidget22/#files

To install the Python module using pip:

pip install Phidget22       (with "sudo" if on Linux/Raspberry Pi)

To install the Python module from the downloaded .tar.gz file, enter downloaded folder and type "python setup.py install"

###########################

########################### Library/driver installation instructions, Windows

https://www.phidgets.com/docs/OS_-_Windows

###########################

########################### Library/driver installation instructions, Linux (other than Raspberry Pi)

https://www.phidgets.com/docs/OS_-_Linux#Quick_Downloads

###########################

########################### Library/driver installation instructions, Raspberry Pi (models 2 and above)

https://www.phidgets.com/education/learn/getting-started-kit-tutorial/install-libraries/

curl -fsSL https://www.phidgets.com/downloads/setup_linux | sudo -E bash -

sudo apt-get install -y libphidget22
 
###########################
