# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision F, 05/22/2022

Verified working on: Python 2.7, 3.8 for Windows 8.1, 10 64-bit and Raspberry Pi Buster (no Mac testing yet).
'''

__author__ = 'reuben.brewer'

import os, sys, time, datetime
import shutil #For copying file
import traceback

########################################
import distutils #For CopyEntireDirectoryWithContents(). Both imports are needed to avoid errors in 'distutils.dir_util.copy_tree("./foo", "./bar")'
from distutils import dir_util #For CopyEntireDirectoryWithContents(). Both imports are needed to avoid errors in 'distutils.dir_util.copy_tree("./foo", "./bar")'
########################################

#######################################################################################################################
def CreateNewDirectory(directory):
    try:
        #print("CreateNewDirectory, directory: " + directory)
        if os.path.isdir(directory) == 0: #No directory with this name exists
            os.makedirs(directory)
    except:
        exceptions = sys.exc_info()[0]
        print("CreateNewDirectory ERROR, Exceptions: %s" % exceptions)
        traceback.print_exc()
#######################################################################################################################

#######################################################################################################################
def CopyEntireDirectoryWithContents(SourceDir, DestDir): #Destination directory doesn't need to exist first
    distutils.dir_util.copy_tree(SourceDir, DestDir)  # Copies the entire directoy
#######################################################################################################################

#######################################################################################################################
def getTimeStampString():

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%m_%d_%Y---%H_%M_%S')

    return st
#######################################################################################################################

#######################################################################################################################
def IsTheTimeCurrentlyAM():
    ts = time.time()
    hour = int(datetime.datetime.fromtimestamp(ts).strftime('%H'))
    if hour < 12:
        return 1
    else:
        return 0
#######################################################################################################################

FileWorkingDirectory = "E:\\" #Use "E:\\" if the filepath length is too long
#FileWorkingDirectory = os.getcwd() #Use "E:\\" if the filepath length is too long

AMflag = IsTheTimeCurrentlyAM()
if AMflag == 1:
    AMorPMstring = "AM"
else:
    AMorPMstring = "PM"

FileDirectoryToCreate = FileWorkingDirectory + "\\Phidgets1xEncoderENC1000_ReubenPython2and3Class_PythonDeploymentFiles_" + getTimeStampString() + AMorPMstring
CreateNewDirectory(FileDirectoryToCreate)

try:

    CopyEntireDirectoryWithContents("G:\\My Drive\\CodeReuben\\Phidgets1xEncoderENC1000_ReubenPython2and3Class\\InstallFiles_and_SupportDocuments", FileDirectoryToCreate + "\\InstallFiles_and_SupportDocuments")  # Copies the entire directory

    shutil.copy("G:\\My Drive\\CodeReuben\\Phidgets1xEncoderENC1000_ReubenPython2and3Class\\Phidgets1xEncoderENC1000_ReubenPython2and3Class.py", FileDirectoryToCreate)
    shutil.copy("G:\\My Drive\\CodeReuben\\Phidgets1xEncoderENC1000_ReubenPython2and3Class\\test_program_for_Phidgets1xEncoderENC1000_ReubenPython2and3Class.py", FileDirectoryToCreate)

    shutil.copy("G:\\My Drive\\CodeReuben\\MyLowPassFilterClass\\LowPassFilter_ReubenPython2and3Class\\LowPassFilter_ReubenPython2and3Class.py", FileDirectoryToCreate)
    #shutil.copy("G:\\My Drive\\CodeReuben\\MyLowPassFilterClass\\LowPassFilter_ReubenPython2and3Class\\test_program_for_LowPassFilter_ReubenPython2and3Class.py", FileDirectoryToCreate)

    shutil.copy("G:\\My Drive\\CodeReuben\\MyPrintClass\\MyPrint_ReubenPython2and3Class\\MyPrint_ReubenPython2and3Class.py", FileDirectoryToCreate)
    #shutil.copy("G:\\My Drive\\CodeReuben\\MyPrintClass\\MyPrint_ReubenPython2and3Class\\test_program_for_MyPrint_ReubenPython2and3Class.py", FileDirectoryToCreate)

    shutil.make_archive(FileDirectoryToCreate, 'zip', FileDirectoryToCreate)

except:
    exceptions = sys.exc_info()[0]
    print("CopyAll_PythonFiles_Phidgets1xEncoderENC1000_ReubenPython2and3Class ERROR, Exceptions: %s" % exceptions)
    traceback.print_exc()

print("CopyAll_PythonFiles_Phidgets1xEncoderENC1000_ReubenPython2and3Class copied all files successfully.")
