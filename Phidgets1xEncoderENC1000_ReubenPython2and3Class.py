# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision J, 12/31/2025

Verified working on: Python 3.12/13 for Windows 10/11 64-bit and Raspberry Pi Bookworm (no Mac testing yet).
'''

__author__ = 'reuben.brewer'

##########################################################################################################
##########################################################################################################

#########################################################
import ReubenGithubCodeModulePaths #Replaces the need to have "ReubenGithubCodeModulePaths.pth" within "C:\Anaconda3\Lib\site-packages".
ReubenGithubCodeModulePaths.Enable()
#########################################################

#########################################################
from LowPassFilter_ReubenPython2and3Class import *
#########################################################

#########################################################
import os, sys, platform
import time, datetime
import math
import collections
from copy import * #for deepcopy
import inspect #To enable 'TellWhichFileWereIn'
import threading
import queue as Queue
import traceback
#########################################################

#########################################################
from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk
#########################################################

#########################################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
#########################################################

###########################################################
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.Log import *
from Phidget22.LogLevel import *
from Phidget22.Devices.Encoder import *
###########################################################

##########################################################################################################
##########################################################################################################

class Phidgets1xEncoderENC1000_ReubenPython2and3Class(Frame): #Subclass the Tkinter Frame

    ##########################################################################################################
    ##########################################################################################################
    def __init__(self, SetupDict):

        print("#################### Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__ starting. ####################")

        #########################################################
        #########################################################
        self.EXIT_PROGRAM_FLAG = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
        self.EnableInternal_MyPrint_Flag = 0
        self.MainThread_still_running_flag = 0

        self.CurrentTime_CalculatedFromMainThread = -11111.0
        self.StartingTime_CalculatedFromMainThread = -11111.0
        self.LastTime_CalculatedFromMainThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromMainThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromMainThread = -11111.0

        self.DetectedDeviceName = "default"
        self.DetectedDeviceID = "default"
        self.DetectedDeviceVersion = "default"
        self.DetectedDeviceSerialNumber = "default"

        self.EncodersList_PhidgetsEncoderObjects = list()

        self.NumberOfEncoders = 1

        self.EncodersList_AttachedAndOpenFlag = [0.0] * self.NumberOfEncoders
        self.EncodersList_NeedsToBeHomedFlag = [0] * self.NumberOfEncoders
        self.EncodersList_UpdateDeltaTseconds = [0.0] * self.NumberOfEncoders
        self.EncodersList_UpdateFrequencyHz = [0.0] * self.NumberOfEncoders
        self.EncodersList_ErrorCallbackFiredFlag = [0.0] * self.NumberOfEncoders

        self.EncodersList_Position_EncoderTicks = [0.0] * self.NumberOfEncoders
        self.EncodersList_Position_Rev = [0.0] * self.NumberOfEncoders
        self.EncodersList_Position_Degrees = [0.0] * self.NumberOfEncoders

        self.EncodersList_IndexPosition_EncoderTicks = [-11111.0] * self.NumberOfEncoders
        self.EncodersList_IndexPosition_Rev = [-11111.0] * self.NumberOfEncoders
        self.EncodersList_IndexPosition_Degrees = [-11111.0] * self.NumberOfEncoders

        self.EncodersList_HomingOffsetPosition_EncoderTicks = [0.0] * self.NumberOfEncoders

        self.EncodersList_Speed_EncoderTicksPerSecond_Raw = [-11111.0] * self.NumberOfEncoders
        self.EncodersList_Speed_RPM_Raw = [-11111.0] * self.NumberOfEncoders
        self.EncodersList_Speed_RPS_Raw = [-11111.0] * self.NumberOfEncoders
        self.EncodersList_Speed_LowPassFilter_ListOfObjects = list()
        self.EncodersList_Speed_EncoderTicksPerSecond_Filtered = [-11111.0] * self.NumberOfEncoders
        self.EncodersList_Speed_RPM_Filtered = [-11111.0] * self.NumberOfEncoders
        self.EncodersList_Speed_RPS_Filtered = [-11111.0] * self.NumberOfEncoders

        '''
        "ENCODER_IO_MODE_PUSH_PULL", # ENCODER_IO_MODE_PUSH_PULL, 0x1, Push-Pull, No additional pull-up or pull-down resistors will be applied to the input lines.
        "ENCODER_IO_MODE_LINE_DRIVER_2K2", # ENCODER_IO_MODE_LINE_DRIVER_2K2, 0x2, Line Driver 2.2K, 2.2kΩ pull-down resistors will be applied to the input lines.
        "ENCODER_IO_MODE_LINE_DRIVER_10K", # ENCODER_IO_MODE_LINE_DRIVER_10K, 0x3, Line Driver 10K, 10kΩ pull-down resistors will be applied to the input lines.
        "ENCODER_IO_MODE_OPEN_COLLECTOR_2K2", # ENCODER_IO_MODE_OPEN_COLLECTOR_2K2, 0x4, Open Collector 2.2K, 2.2kΩ pull-up resistors will be applied to the input lines.
        "ENCODER_IO_MODE_OPEN_COLLECTOR_10K"]  # ENCODER_IO_MODE_OPEN_COLLECTOR_10K, 0x5, Open Collector 10K, 10kΩ pull-up resistors will be applied to the input lines.
        '''

        self.EncodersList_ElectricalIOmode_AcceptableValuesDictIntsAsKeys = dict([(1, "ENCODER_IO_MODE_PUSH_PULL"),
                                                                                     (2, "ENCODER_IO_MODE_LINE_DRIVER_2K2"),
                                                                                     (3, "ENCODER_IO_MODE_LINE_DRIVER_10K"),
                                                                                     (4, "ENCODER_IO_MODE_OPEN_COLLECTOR_2K2"),
                                                                                     (5, "ENCODER_IO_MODE_OPEN_COLLECTOR_10K")])

        self.EncodersList_ElectricalIOmode_AcceptableValuesDictStringsAsKeys = dict([("ENCODER_IO_MODE_PUSH_PULL", 1),
                                                                                     ("ENCODER_IO_MODE_LINE_DRIVER_2K2", 2),
                                                                                     ("ENCODER_IO_MODE_LINE_DRIVER_10K", 3),
                                                                                     ("ENCODER_IO_MODE_OPEN_COLLECTOR_2K2", 4),
                                                                                     ("ENCODER_IO_MODE_OPEN_COLLECTOR_10K", 5)])

        self.MostRecentDataDict = dict()
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if platform.system() == "Linux":

            if "raspberrypi" in platform.uname(): #os.uname() doesn't work in windows
                self.my_platform = "pi"
            else:
                self.my_platform = "linux"

        elif platform.system() == "Windows":
            self.my_platform = "windows"

        elif platform.system() == "Darwin":
            self.my_platform = "mac"

        else:
            self.my_platform = "other"

        print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: The OS platform is: " + self.my_platform)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "GUIparametersDict" in SetupDict:
            self.GUIparametersDict = SetupDict["GUIparametersDict"]

            #########################################################
            #########################################################
            if "USE_GUI_FLAG" in self.GUIparametersDict:
                self.USE_GUI_FLAG = self.PassThrough0and1values_ExitProgramOtherwise("USE_GUI_FLAG", self.GUIparametersDict["USE_GUI_FLAG"])
            else:
                self.USE_GUI_FLAG = 0

            print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "EnableInternal_MyPrint_Flag" in self.GUIparametersDict:
                self.EnableInternal_MyPrint_Flag = self.PassThrough0and1values_ExitProgramOtherwise("EnableInternal_MyPrint_Flag", self.GUIparametersDict["EnableInternal_MyPrint_Flag"])
            else:
                self.EnableInternal_MyPrint_Flag = 0

            print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "PrintToConsoleFlag" in self.GUIparametersDict:
                self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", self.GUIparametersDict["PrintToConsoleFlag"])
            else:
                self.PrintToConsoleFlag = 1

            print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: PrintToConsoleFlag: " + str(self.PrintToConsoleFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "NumberOfPrintLines" in self.GUIparametersDict:
                self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", self.GUIparametersDict["NumberOfPrintLines"], 0.0, 50.0))
            else:
                self.NumberOfPrintLines = 10

            print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: NumberOfPrintLines: " + str(self.NumberOfPrintLines))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "UseBorderAroundThisGuiObjectFlag" in self.GUIparametersDict:
                self.UseBorderAroundThisGuiObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseBorderAroundThisGuiObjectFlag", self.GUIparametersDict["UseBorderAroundThisGuiObjectFlag"])
            else:
                self.UseBorderAroundThisGuiObjectFlag = 0

            print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: UseBorderAroundThisGuiObjectFlag: " + str(self.UseBorderAroundThisGuiObjectFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_ROW" in self.GUIparametersDict:
                self.GUI_ROW = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROW", self.GUIparametersDict["GUI_ROW"], 0.0, 1000.0))
            else:
                self.GUI_ROW = 0

            print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: GUI_ROW: " + str(self.GUI_ROW))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMN" in self.GUIparametersDict:
                self.GUI_COLUMN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMN", self.GUIparametersDict["GUI_COLUMN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMN = 0

            print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: GUI_COLUMN: " + str(self.GUI_COLUMN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADX" in self.GUIparametersDict:
                self.GUI_PADX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADX", self.GUIparametersDict["GUI_PADX"], 0.0, 1000.0))
            else:
                self.GUI_PADX = 0

            print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: GUI_PADX: " + str(self.GUI_PADX))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADY" in self.GUIparametersDict:
                self.GUI_PADY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADY", self.GUIparametersDict["GUI_PADY"], 0.0, 1000.0))
            else:
                self.GUI_PADY = 0

            print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: GUI_PADY: " + str(self.GUI_PADY))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_ROWSPAN" in self.GUIparametersDict:
                self.GUI_ROWSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROWSPAN", self.GUIparametersDict["GUI_ROWSPAN"], 0.0, 1000.0))
            else:
                self.GUI_ROWSPAN = 1

            print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: GUI_ROWSPAN: " + str(self.GUI_ROWSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMNSPAN" in self.GUIparametersDict:
                self.GUI_COLUMNSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMNSPAN", self.GUIparametersDict["GUI_COLUMNSPAN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMNSPAN = 1

            print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: GUI_COLUMNSPAN: " + str(self.GUI_COLUMNSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_STICKY" in self.GUIparametersDict:
                self.GUI_STICKY = str(self.GUIparametersDict["GUI_STICKY"])
            else:
                self.GUI_STICKY = "w"

            print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: GUI_STICKY: " + str(self.GUI_STICKY))
            #########################################################
            #########################################################

        else:
            self.GUIparametersDict = dict()
            self.USE_GUI_FLAG = 0
            print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: No GUIparametersDict present, setting USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))

        #print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: GUIparametersDict: " + str(self.GUIparametersDict))
        #########################################################
        #########################################################

        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "VINT_DesiredSerialNumber" in SetupDict:
            try:
                self.VINT_DesiredSerialNumber = int(SetupDict["VINT_DesiredSerialNumber"])
            except:
                print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: Error, VINT_DesiredSerialNumber invalid.")
        else:
            self.VINT_DesiredSerialNumber = -1

        print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: VINT_DesiredSerialNumber: " + str(self.VINT_DesiredSerialNumber))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "VINT_DesiredPortNumber" in SetupDict:
            try:
                self.VINT_DesiredPortNumber = int(SetupDict["VINT_DesiredPortNumber"])
            except:
                print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: Error, VINT_DesiredPortNumber invalid.")
        else:
            print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: Error, must initialize object with 'VINT_DesiredPortNumber' argument.")
            return

        print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: VINT_DesiredPortNumber: " + str(self.VINT_DesiredPortNumber))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DesiredDeviceID" in SetupDict:
            try:
                self.DesiredDeviceID = int(SetupDict["DesiredDeviceID"])
            except:
                print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: Error, DesiredDeviceID invalid.")
        else:
            print("Phidgets1xEncoderENC1000_ReubenPython2and3Class Error: Must initialize object with 'DesiredDeviceID' argument.")
            return

        print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: DesiredDeviceID: " + str(self.DesiredDeviceID))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "NameToDisplay_UserSet" in SetupDict:
            self.NameToDisplay_UserSet = str(SetupDict["NameToDisplay_UserSet"])
        else:
            self.NameToDisplay_UserSet = ""

        print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: NameToDisplay_UserSet: " + str(self.NameToDisplay_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "WaitForAttached_TimeoutDuration_Milliseconds" in SetupDict:
            self.WaitForAttached_TimeoutDuration_Milliseconds = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("WaitForAttached_TimeoutDuration_Milliseconds", SetupDict["WaitForAttached_TimeoutDuration_Milliseconds"], 0.0, 60000.0))

        else:
            self.WaitForAttached_TimeoutDuration_Milliseconds = 5000

        print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: WaitForAttached_TimeoutDuration_Milliseconds: " + str(self.WaitForAttached_TimeoutDuration_Milliseconds))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "UsePhidgetsLoggingInternalToThisClassObjectFlag" in SetupDict:
            self.UsePhidgetsLoggingInternalToThisClassObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UsePhidgetsLoggingInternalToThisClassObjectFlag", SetupDict["UsePhidgetsLoggingInternalToThisClassObjectFlag"])
        else:
            self.UsePhidgetsLoggingInternalToThisClassObjectFlag = 1

        print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: UsePhidgetsLoggingInternalToThisClassObjectFlag: " + str(self.UsePhidgetsLoggingInternalToThisClassObjectFlag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "EncoderUpdateDeltaT_ms" in SetupDict:
            self.EncoderUpdateDeltaT_ms = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("EncoderUpdateDeltaT_ms", SetupDict["EncoderUpdateDeltaT_ms"], 20.0, 1000.0))
        else:
            self.EncoderUpdateDeltaT_ms = 20

        print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: EncoderUpdateDeltaT_ms: " + str(self.EncoderUpdateDeltaT_ms))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "EncodersList_CPR" in SetupDict:
            EncodersList_CPR_TEMP = SetupDict["EncodersList_CPR"]
            if self.IsInputList(EncodersList_CPR_TEMP) == 1 and len(EncodersList_CPR_TEMP) == self.NumberOfEncoders:
                self.EncodersList_CPR = list()
                for EncoderChannel, CPR_TEMP in enumerate(EncodersList_CPR_TEMP):
                    CPR = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("EncodersList_CPR, EncoderChannel " + str(EncoderChannel), CPR_TEMP, 0, 250000)
                    self.EncodersList_CPR.append(CPR)
            else:
                print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: Error, 'EncodersList_CPR' must be a length of length 4 with values of 0 or 1.")
                return
        else:
            self.EncodersList_CPR = [1] * self.NumberOfEncoders

        print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: EncodersList_CPR: " + str(self.EncodersList_CPR))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "EncodersList_SpeedExponentialFilterLambda" in SetupDict:
            EncodersList_SpeedExponentialFilterLambda_TEMP = SetupDict["EncodersList_SpeedExponentialFilterLambda"]
            if self.IsInputList(EncodersList_SpeedExponentialFilterLambda_TEMP) == 1 and len(EncodersList_SpeedExponentialFilterLambda_TEMP) == self.NumberOfEncoders:
                self.EncodersList_SpeedExponentialFilterLambda = list()
                for EncoderChannel, SpeedExponentialFilterLambda_TEMP in enumerate(EncodersList_SpeedExponentialFilterLambda_TEMP):
                    SpeedExponentialFilterLambda = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("EncodersList_SpeedExponentialFilterLambda, EncoderChannel " + str(EncoderChannel), SpeedExponentialFilterLambda_TEMP, 0.0, 1.0)
                    self.EncodersList_SpeedExponentialFilterLambda.append(SpeedExponentialFilterLambda)
            else:
                print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: Error, 'EncodersList_SpeedExponentialFilterLambda' must be a length of length 4 with values of 0 or 1.")
                return
        else:
            self.EncodersList_SpeedExponentialFilterLambda = [1.0] * self.NumberOfEncoders #Default to no filtering, new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value

        print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: EncodersList_SpeedExponentialFilterLambda: " + str(self.EncodersList_SpeedExponentialFilterLambda))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "EncodersList_ElectricalIOmode" in SetupDict:
            EncodersList_ElectricalIOmode_TEMP = SetupDict["EncodersList_ElectricalIOmode"]
            if self.IsInputList(EncodersList_ElectricalIOmode_TEMP) == 1 and len(EncodersList_ElectricalIOmode_TEMP) == self.NumberOfEncoders:
                self.EncodersList_ElectricalIOmode = list()
                for EncoderChannel, ElectricalIOmode_TEMP in enumerate(EncodersList_ElectricalIOmode_TEMP):
                    if ElectricalIOmode_TEMP in self.EncodersList_ElectricalIOmode_AcceptableValuesDictStringsAsKeys:
                        self.EncodersList_ElectricalIOmode.append(ElectricalIOmode_TEMP)
                    else:
                        print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: Error, 'EncodersList_ElectricalIOmode' values must be contained within the set " + str(self.EncodersList_ElectricalIOmode_AcceptableValuesDictStringsAsKeys))
                        return
            else:
                print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: Error, 'EncodersList_ElectricalIOmode' must be a length of length 4 with values of 0 or 1.")
                return
        else:
            self.EncodersList_ElectricalIOmode = ["ENCODER_IO_MODE_PUSH_PULL"] * self.NumberOfEncoders

        print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: EncodersList_ElectricalIOmode: " + str(self.EncodersList_ElectricalIOmode))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "MainThread_TimeToSleepEachLoop" in SetupDict:
            self.MainThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("MainThread_TimeToSleepEachLoop", SetupDict["MainThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.MainThread_TimeToSleepEachLoop = 0.005

        print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: MainThread_TimeToSleepEachLoop: " + str(self.MainThread_TimeToSleepEachLoop))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:

            for EncoderChannel in range(0, self.NumberOfEncoders):
                self.EncodersList_Speed_LowPassFilter_ListOfObjects.append(LowPassFilter_ReubenPython2and3Class(dict([("UseMedianFilterFlag", 0),
                                                                                                                        ("UseExponentialSmoothingFilterFlag", 1),
                                                                                                                        ("ExponentialSmoothingFilterLambda", self.EncodersList_SpeedExponentialFilterLambda[EncoderChannel])])))

                LowPassFilter_OPEN_FLAG = self.EncodersList_Speed_LowPassFilter_ListOfObjects[EncoderChannel].OBJECT_CREATED_SUCCESSFULLY_FLAG
    
                if LowPassFilter_OPEN_FLAG != 1:
                    print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: Failed to open LowPassFilter_ReubenPython2and3ClassObject.")
                    return

        except:
            exceptions = sys.exc_info()[0]
            print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: Exceptions: %s" % exceptions)
            return
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.PrintToGui_Label_TextInputHistory_List = [" "]*self.NumberOfPrintLines
        self.PrintToGui_Label_TextInput_Str = ""
        self.GUI_ready_to_be_updated_flag = 0
        #########################################################
        #########################################################

        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:

            #########################################################
            self.Encoder0object = Encoder()
            self.EncodersList_PhidgetsEncoderObjects.append(self.Encoder0object)
            self.Encoder0object.setHubPort(self.VINT_DesiredPortNumber)

            if self.VINT_DesiredSerialNumber != -1:
                self.Encoder0object.setDeviceSerialNumber(self.VINT_DesiredSerialNumber)

            self.Encoder0object.setOnPositionChangeHandler(self.Encoder0onPositionChangeCallback)
            self.Encoder0object.setOnAttachHandler(self.Encoder0onAttachCallback)
            self.Encoder0object.setOnDetachHandler(self.Encoder0onDetachCallback)
            self.Encoder0object.setOnErrorHandler(self.Encoder0onErrorCallback)
            self.Encoder0object.openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)
            #########################################################

            self.PhidgetsDeviceConnectedFlag = 1

        except PhidgetException as e:
            self.PhidgetsDeviceConnectedFlag = 0
            print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: Failed to attach, Phidget Exception %i: %s" % (e.code, e.details))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if self.PhidgetsDeviceConnectedFlag == 1:

            #########################################################
            #########################################################
            if self.UsePhidgetsLoggingInternalToThisClassObjectFlag == 1:
                try:
                    Log.enable(LogLevel.PHIDGET_LOG_INFO, os.getcwd() + "\Phidgets1xEncoderENC1000_ReubenPython2and3Class_PhidgetLog_INFO.txt")
                    print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: Enabled Phidget Logging.")
                except PhidgetException as e:
                    print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: Failed to enable Phidget Logging, Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            try:
                self.DetectedDeviceName = self.Encoder0object.getDeviceName()
                print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: DetectedDeviceName: " + self.DetectedDeviceName)

            except PhidgetException as e:
                print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: Failed to call 'getDeviceName', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            try:
                self.VINT_DetectedSerialNumber = self.Encoder0object.getDeviceSerialNumber()
                print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: VINT_DetectedSerialNumber: " + str(self.VINT_DetectedSerialNumber))

            except PhidgetException as e:
                print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: Failed to call 'getDeviceSerialNumber', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            try:
                self.DetectedDeviceID = self.Encoder0object.getDeviceID()
                print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: DetectedDeviceID: " + str(self.DetectedDeviceID))

            except PhidgetException as e:
                print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: Failed to call 'getDesiredDeviceID', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            try:
                self.DetectedDeviceVersion = self.Encoder0object.getDeviceVersion()
                print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: DetectedDeviceVersion: " + str(self.DetectedDeviceVersion))

            except PhidgetException as e:
                print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: Failed to call 'getDeviceVersion', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            try:
                self.DetectedDeviceLibraryVersion = self.Encoder0object.getLibraryVersion()
                print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: DetectedDeviceLibraryVersion: " + str(self.DetectedDeviceLibraryVersion))

            except PhidgetException as e:
                print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: Failed to call 'getLibraryVersion', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if self.VINT_DesiredSerialNumber != -1:  # '-1' means we should open the device regardless os serial number.
                if self.VINT_DetectedSerialNumber != self.VINT_DesiredSerialNumber:
                    print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: The desired Serial Number (" + str(self.VINT_DesiredSerialNumber) + ") does not match the detected serial number (" + str(self.VINT_DetectedSerialNumber) + ").")
                    input("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: Press any key (and enter) to exit.")
                    sys.exit()
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if self.DetectedDeviceID != self.DesiredDeviceID:
                print("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: The desired DesiredDeviceID (" + str(self.DesiredDeviceID) + ") does not match the detected Device ID (" + str(self.DetectedDeviceID) + ").")
                input("Phidgets1xEncoderENC1000_ReubenPython2and3Class __init__: Press any key (and enter) to exit.")
                sys.exit()
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            self.MainThread_ThreadingObject = threading.Thread(target=self.MainThread, args=())
            self.MainThread_ThreadingObject.start()
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 1
            #########################################################
            #########################################################

        #########################################################
        #########################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def LimitNumber_IntOutputOnly(self, min_val, max_val, test_val):
        if test_val > max_val:
            test_val = max_val

        elif test_val < min_val:
            test_val = min_val

        else:
            test_val = test_val

        test_val = int(test_val)

        return test_val
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def LimitNumber_FloatOutputOnly(self, min_val, max_val, test_val):
        if test_val > max_val:
            test_val = max_val

        elif test_val < min_val:
            test_val = min_val

        else:
            test_val = test_val

        test_val = float(test_val)

        return test_val
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def PassThrough0and1values_ExitProgramOtherwise(self, InputNameString, InputNumber, ExitProgramIfFailureFlag=1):

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            InputNumber_ConvertedToFloat = float(InputNumber)
            ##########################################################################################################

        except:

            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error. InputNumber must be a numerical value, Exceptions: %s" % exceptions)

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -1
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            if InputNumber_ConvertedToFloat == 0.0 or InputNumber_ConvertedToFloat == 1.0:
                return InputNumber_ConvertedToFloat

            else:

                print("PassThrough0and1values_ExitProgramOtherwise Error. '" +
                      str(InputNameString) +
                      "' must be 0 or 1 (value was " +
                      str(InputNumber_ConvertedToFloat) +
                      ").")

                ##########################
                if ExitProgramIfFailureFlag == 1:
                    sys.exit()

                else:
                    return -1
                ##########################

            ##########################################################################################################

        except:

            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -1
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def PassThroughFloatValuesInRange_ExitProgramOtherwise(self, InputNameString, InputNumber, RangeMinValue, RangeMaxValue, ExitProgramIfFailureFlag=1):

        ##########################################################################################################
        ##########################################################################################################
        try:
            ##########################################################################################################
            InputNumber_ConvertedToFloat = float(InputNumber)
            ##########################################################################################################

        except:
            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)
            traceback.print_exc()

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -11111.0
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            InputNumber_ConvertedToFloat_Limited = self.LimitNumber_FloatOutputOnly(RangeMinValue, RangeMaxValue, InputNumber_ConvertedToFloat)

            if InputNumber_ConvertedToFloat_Limited != InputNumber_ConvertedToFloat:
                print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '" +
                      str(InputNameString) +
                      "' must be in the range [" +
                      str(RangeMinValue) +
                      ", " +
                      str(RangeMaxValue) +
                      "] (value was " +
                      str(InputNumber_ConvertedToFloat) + ")")

                ##########################
                if ExitProgramIfFailureFlag == 1:
                    sys.exit()
                else:
                    return -11111.0
                ##########################

            else:
                return InputNumber_ConvertedToFloat_Limited
            ##########################################################################################################

        except:
            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            traceback.print_exc()

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -11111.0
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TellWhichFileWereIn(self):

        #We used to use this method, but it gave us the root calling file, not the class calling file
        #absolute_file_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        #filename = absolute_file_path[absolute_file_path.rfind("\\") + 1:]

        frame = inspect.stack()[1]
        filename = frame[1][frame[1].rfind("\\") + 1:]
        filename = filename.replace(".py","")

        return filename
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def EncoderGENERALonAttachCallback(self, EncoderChannel):

        try:
            ##############################
            self.EncodersList_PhidgetsEncoderObjects[EncoderChannel].setDataInterval(self.EncoderUpdateDeltaT_ms)
            print("EncoderGENERALonAttachCallback: Set EncoderChannel " + \
                  str(EncoderChannel) + \
                  " DataInterval to " + \
                  str(self.EncodersList_PhidgetsEncoderObjects[EncoderChannel].getDataInterval()) + \
                  "ms.")
            ##############################

            ##############################
            self.EncodersList_PhidgetsEncoderObjects[EncoderChannel].setIOMode(self.EncodersList_ElectricalIOmode_AcceptableValuesDictStringsAsKeys[self.EncodersList_ElectricalIOmode[EncoderChannel]])
            print("EncoderGENERALonAttachCallback: Set EncoderChannel " + \
                  str(EncoderChannel) + \
                  " IOmode to " + \
                  str(self.EncodersList_ElectricalIOmode_AcceptableValuesDictIntsAsKeys[self.EncodersList_PhidgetsEncoderObjects[EncoderChannel].getIOMode()]))
            ##############################

            ##############################
            self.EncodersList_PhidgetsEncoderObjects[EncoderChannel].setPositionChangeTrigger(0) #Setting the trigger to 0 makes the onPositionChange callback fire every self.EncoderUpdateDeltaT_ms
            print("EncoderGENERALonAttachCallback: Set EncoderChannel " + \
            str(EncoderChannel) + \
            " PositionChangeTrigger to " + \
            str(self.EncodersList_PhidgetsEncoderObjects[EncoderChannel].getPositionChangeTrigger()))
            ##############################

            self.EncodersList_AttachedAndOpenFlag[EncoderChannel] = 1
            self.MyPrint_WithoutLogFile("$$$$$$$$$$ EncoderGENERALonAttachCallback event for EncoderChannel " + str(EncoderChannel) + ", Attached! $$$$$$$$$$")

        except PhidgetException as e:
            self.EncodersList_AttachedAndOpenFlag[EncoderChannel] = 0
            self.MyPrint_WithoutLogFile("EncoderGENERALonAttachCallback event for EncoderChannel " + str(EncoderChannel) + ", ERROR: Failed to attach Encoder0, Phidget Exception %i: %s" % (e.code, e.details))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def EncoderGENERALonDetachCallback(self, EncoderChannel):

        self.EncodersList_AttachedAndOpenFlag[EncoderChannel] = 0
        self.MyPrint_WithoutLogFile("$$$$$$$$$$ EncoderGENERALonDetachCallback event for EncoderChannel " + str(EncoderChannel) + ", Detatched! $$$$$$$$$$")

        try:
            self.EncodersList_PhidgetsEncoderObjects[EncoderChannel].openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)
            time.sleep(0.250)

        except PhidgetException as e:
            self.MyPrint_WithoutLogFile("EncoderGENERALonDetachCallback event for Encoder Channel " + str(EncoderChannel) + ", failed to openWaitForAttachment, Phidget Exception %i: %s" % (e.code, e.details))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ########################################################################################################## unicorn
    def EncoderGENERALonPositionChangeCallback(self, EncoderChannel, positionChange, timeChangeInMilliseconds, indexTriggered):

        ################################
        self.EncodersList_Position_EncoderTicks[EncoderChannel] = self.EncodersList_Position_EncoderTicks[EncoderChannel] + positionChange
        self.EncodersList_Position_Rev[EncoderChannel] = self.EncodersList_Position_EncoderTicks[EncoderChannel]/(4.0*self.EncodersList_CPR[EncoderChannel])
        self.EncodersList_Position_Degrees[EncoderChannel] = 360.0*self.EncodersList_Position_Rev[EncoderChannel]
        ################################

        ################################
        if indexTriggered == 1:
            self.EncodersList_IndexPosition_EncoderTicks[EncoderChannel] = self.EncodersList_PhidgetsEncoderObjects[EncoderChannel].getIndexPosition()
            self.EncodersList_IndexPosition_Rev[EncoderChannel] = self.EncodersList_IndexPosition_EncoderTicks[EncoderChannel]/(4.0*self.EncodersList_CPR[EncoderChannel])
            self.EncodersList_IndexPosition_Degrees[EncoderChannel] = 360.0 * self.EncodersList_IndexPosition_Rev[EncoderChannel]
        ################################

        ################################
        if timeChangeInMilliseconds > 0.0:
            self.EncodersList_UpdateDeltaTseconds[EncoderChannel] = timeChangeInMilliseconds/1000.0
            self.EncodersList_UpdateFrequencyHz[EncoderChannel] = 1.0/self.EncodersList_UpdateDeltaTseconds[EncoderChannel]
            self.EncodersList_Speed_EncoderTicksPerSecond_Raw[EncoderChannel] = positionChange/self.EncodersList_UpdateDeltaTseconds[EncoderChannel]
            self.EncodersList_Speed_RPS_Raw[EncoderChannel] = self.EncodersList_Speed_EncoderTicksPerSecond_Raw[EncoderChannel]/(4.0*self.EncodersList_CPR[EncoderChannel])
            self.EncodersList_Speed_RPM_Raw[EncoderChannel] = self.EncodersList_Speed_RPS_Raw[EncoderChannel]*60.0

            self.EncodersList_Speed_EncoderTicksPerSecond_Filtered[EncoderChannel] = self.EncodersList_Speed_LowPassFilter_ListOfObjects[EncoderChannel].AddDataPointFromExternalProgram(self.EncodersList_Speed_EncoderTicksPerSecond_Raw[EncoderChannel])["SignalOutSmoothed"]
            self.EncodersList_Speed_RPS_Filtered[EncoderChannel] = self.EncodersList_Speed_EncoderTicksPerSecond_Filtered[EncoderChannel]/(4.0*self.EncodersList_CPR[EncoderChannel])
            self.EncodersList_Speed_RPM_Filtered[EncoderChannel] = self.EncodersList_Speed_RPS_Filtered[EncoderChannel] * 60.0
        ################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def EncoderGENERALonErrorCallback(self, EncoderChannel, code, description):

        self.EncodersList_ErrorCallbackFiredFlag[EncoderChannel] = 1

        self.MyPrint_WithoutLogFile("EncoderGENERALonErrorCallback event for Encoder Channel " + str(EncoderChannel) + ", Error Code " + ErrorEventCode.getName(code) + ", description: " + str(description))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Encoder0onAttachCallback(self, HandlerSelf):

        EncoderChannel = 0
        self.EncoderGENERALonAttachCallback(EncoderChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Encoder0onDetachCallback(self, HandlerSelf):

        EncoderChannel = 0
        self.EncoderGENERALonDetachCallback(EncoderChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Encoder0onPositionChangeCallback(self, HandlerSelf, positionChange, timeChangeInMilliseconds, indexTriggered):

        EncoderChannel = 0
        self.EncoderGENERALonPositionChangeCallback(EncoderChannel, positionChange, timeChangeInMilliseconds, indexTriggered)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Encoder0onErrorCallback(self, HandlerSelf, code, description):

        EncoderChannel = 0
        self.EncoderGENERALonErrorCallback(EncoderChannel, code, description)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def getPreciseSecondsTimeStampString(self):
        ts = time.time()

        return ts
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def EncoderHome(self, EncoderChannel, PositionToSetAsZero_EncoderTicks = -11111.0):

        if EncoderChannel in range(0, self.NumberOfEncoders):

            ###########################
            if PositionToSetAsZero_EncoderTicks == -11111.0:
                PositionToSetAsZero_EncoderTicks = self.EncodersList_Position_EncoderTicks[EncoderChannel]
            ###########################

            self.EncodersList_HomingOffsetPosition_EncoderTicks[EncoderChannel] = PositionToSetAsZero_EncoderTicks
            self.EncodersList_Position_EncoderTicks[EncoderChannel] = self.EncodersList_Position_EncoderTicks[EncoderChannel] - self.EncodersList_HomingOffsetPosition_EncoderTicks[EncoderChannel]
            return 1

        else:
            self.MyPrint_WithoutLogFile("EncoderHome ERROR: EncoderChannel must be in set " + str(list(range(0, self.NumberOfEncoders))) + ".")
            return 0
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GetMostRecentDataDict(self):

        if self.EXIT_PROGRAM_FLAG == 0:
            self.MostRecentDataDict = dict([("EncodersList_Position_EncoderTicks", self.EncodersList_Position_EncoderTicks),
                                                 ("EncodersList_Position_Rev", self.EncodersList_Position_Rev),
                                                 ("EncodersList_Position_Degrees", self.EncodersList_Position_Degrees),
                                                 ("EncodersList_IndexPosition_EncoderTicks", self.EncodersList_IndexPosition_EncoderTicks),
                                                 ("EncodersList_IndexPosition_Rev", self.EncodersList_IndexPosition_Rev),
                                                 ("EncodersList_IndexPosition_Degrees", self.EncodersList_IndexPosition_Degrees),
                                                 ("EncodersList_Speed_EncoderTicksPerSecond_Raw", self.EncodersList_Speed_EncoderTicksPerSecond_Raw),
                                                 ("EncodersList_Speed_RPM_Raw", self.EncodersList_Speed_RPM_Raw),
                                                 ("EncodersList_Speed_RPS_Raw", self.EncodersList_Speed_RPS_Raw),
                                                 ("EncodersList_Speed_EncoderTicksPerSecond_Filtered", self.EncodersList_Speed_EncoderTicksPerSecond_Filtered),
                                                 ("EncodersList_Speed_RPM_Filtered", self.EncodersList_Speed_RPM_Filtered),
                                                 ("EncodersList_Speed_RPS_Filtered", self.EncodersList_Speed_RPS_Filtered),
                                                 ("EncodersList_ErrorCallbackFiredFlag", self.EncodersList_ErrorCallbackFiredFlag),
                                                 ("Time", self.CurrentTime_CalculatedFromMainThread)])

            return deepcopy(self.MostRecentDataDict) #deepcopy IS required as MostRecentDataDict contains lists.

        else:
            return dict() #So that we're not returning variables during the close-down process.
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_MainThread(self):

        try:
            self.DataStreamingDeltaT_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread - self.LastTime_CalculatedFromMainThread

            if self.DataStreamingDeltaT_CalculatedFromMainThread != 0.0:
                self.DataStreamingFrequency_CalculatedFromMainThread = 1.0/self.DataStreamingDeltaT_CalculatedFromMainThread

            self.LastTime_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_MainThread ERROR with Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ########################################################################################################## unicorn
    def MainThread(self):

        self.MyPrint_WithoutLogFile("Started MainThread for Phidgets1xEncoderENC1000_ReubenPython2and3Class object.")
        
        self.MainThread_still_running_flag = 1

        self.StartingTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString()

        ###############################################
        while self.EXIT_PROGRAM_FLAG == 0:

            ###############################################
            self.CurrentTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromMainThread
            ###############################################

            ###############################################
            for EncoderChannel, NeedsToBeHomedFlag in enumerate(self.EncodersList_NeedsToBeHomedFlag):
                if NeedsToBeHomedFlag == 1:
                    SuccessFlag = self.EncoderHome(EncoderChannel)

                    if SuccessFlag == 1:
                        self.EncodersList_NeedsToBeHomedFlag[EncoderChannel] = 0
            ###############################################

            ############################################### USE THE TIME.SLEEP() TO SET THE LOOP FREQUENCY
            ###############################################
            ###############################################
            self.UpdateFrequencyCalculation_MainThread()

            if self.MainThread_TimeToSleepEachLoop > 0.0:
                time.sleep(self.MainThread_TimeToSleepEachLoop)

            ###############################################
            ###############################################
            ###############################################

        ###############################################

        self.MyPrint_WithoutLogFile("Finished MainThread for Phidgets1xEncoderENC1000_ReubenPython2and3Class object.")
        
        self.MainThread_still_running_flag = 0
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("Exiting all threads for Phidgets1xEncoderENC1000_ReubenPython2and3Class object")

        self.EXIT_PROGRAM_FLAG = 1

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CreateGUIobjects(self, TkinterParent):

        print("Phidgets1xEncoderENC1000_ReubenPython2and3Class, CreateGUIobjects event fired.")

        #################################################
        self.root = TkinterParent
        self.parent = TkinterParent
        #################################################

        #################################################
        self.myFrame = Frame(self.root)

        if self.UseBorderAroundThisGuiObjectFlag == 1:
            self.myFrame["borderwidth"] = 2
            self.myFrame["relief"] = "ridge"

        self.myFrame.grid(row = self.GUI_ROW,
                          column = self.GUI_COLUMN,
                          padx = self.GUI_PADX,
                          pady = self.GUI_PADY,
                          rowspan = self.GUI_ROWSPAN,
                          columnspan= self.GUI_COLUMNSPAN,
                          sticky = self.GUI_STICKY)
        #################################################

        #################################################
        self.TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150) #RGB
        self.TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150) #RGB
        self.TKinter_LightYellowColor = '#%02x%02x%02x' % (255, 255, 150)  # RGB
        self.TKinter_DefaultGrayColor = '#%02x%02x%02x' % (240, 240, 240)  # RGB
        #################################################

        #################################################
        self.DeviceInfo_Label = Label(self.myFrame, text="Device Info", width=50)

        self.DeviceInfo_Label["text"] = self.NameToDisplay_UserSet + \
                                        "\nDevice Name: " + self.DetectedDeviceName + \
                                        "\nDevice Serial Number: " + str(self.VINT_DetectedSerialNumber) + \
                                        "\nDevice ID: " + str(self.DetectedDeviceID) + \
                                        "\nDevice Version: " + str(self.DetectedDeviceVersion)

        self.DeviceInfo_Label.grid(row=0, column=0, padx=5, pady=1, columnspan=1, rowspan=1)
        #################################################

        #################################################
        self.Encoders_Label = Label(self.myFrame, text="Encoders_Label", width=120)
        self.Encoders_Label.grid(row=0, column=1, padx=5, pady=1, columnspan=1, rowspan=1)
        #################################################
        
        #################################################
        self.EncoderHomingButtonsFrame = Frame(self.myFrame)
        self.EncoderHomingButtonsFrame.grid(row = 1, column = 0, padx = 1, pady = 1, rowspan = 1, columnspan = 1)

        self.EncodersList_HomingButtonObjects = []
        for EncoderChannel in range(0, self.NumberOfEncoders):
            self.EncodersList_HomingButtonObjects.append(Button(self.EncoderHomingButtonsFrame, text="Home Encoder " + str(EncoderChannel), state="normal", width=15, command=lambda i=EncoderChannel: self.EncodersList_HomingButtonObjectsResponse(i)))
            self.EncodersList_HomingButtonObjects[EncoderChannel].grid(row=1, column=EncoderChannel, padx=1, pady=1)
        #################################################

        #################################################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=75)
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=2, column=0, padx=1, pady=1, columnspan=10, rowspan=10)
        #################################################

        #################################################
        self.GUI_ready_to_be_updated_flag = 1
        #################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_update_clock(self):

        #######################################################
        #######################################################
        #######################################################
        #######################################################
        if self.USE_GUI_FLAG == 1 and self.EXIT_PROGRAM_FLAG == 0:

            #######################################################
            #######################################################
            #######################################################
            if self.GUI_ready_to_be_updated_flag == 1:

                #######################################################
                #######################################################
                try:

                    #######################################################
                    self.Encoders_Label["text"] = "Encoder Position Ticks: " + str(self.EncodersList_Position_EncoderTicks) + \
                                                "\nEncoder Position Degrees: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.EncodersList_Position_Degrees, 0, 3) + \
                                                "\nEncoder Position Rev: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.EncodersList_Position_Rev, 0, 3) + \
                                                "\nIndex Pos: " + str(self.EncodersList_IndexPosition_EncoderTicks) + \
                                                "\nSpeed Ticks/S Raw: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.EncodersList_Speed_EncoderTicksPerSecond_Raw, 0, 5)+ \
                                                "\nSpeed RPM Raw: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.EncodersList_Speed_RPM_Raw, 0, 5) + \
                                                "\nSpeed RPS Raw: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.EncodersList_Speed_RPS_Raw, 0, 5) + \
                                                "\nSpeed Ticks/S Filtered: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.EncodersList_Speed_EncoderTicksPerSecond_Filtered, 0, 5)+ \
                                                "\nSpeed RPM Filtered: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.EncodersList_Speed_RPM_Filtered, 0, 5) + \
                                                "\nSpeed RPS Filtered: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.EncodersList_Speed_RPS_Filtered, 0, 5) + \
                                                "\nEncodersList_UpdateDeltaTseconds: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.EncodersList_UpdateDeltaTseconds, 0, 5) + \
                                                "\nEncodersList_ElectricalIOmode: " + str(self.EncodersList_ElectricalIOmode) + \
                                                "\nEncodersList_CPR: " + str(self.EncodersList_CPR) + \
                                                "\nTime: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.CurrentTime_CalculatedFromMainThread, 0, 3) + \
                                                "\nMain Thread Frequency: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DataStreamingFrequency_CalculatedFromMainThread, 0, 3)
                    #######################################################

                    #######################################################
                    self.PrintToGui_Label.config(text=self.PrintToGui_Label_TextInput_Str)
                    #######################################################

                except:
                    exceptions = sys.exc_info()[0]
                    print("Phidgets1xEncoderENC1000_ReubenPython2and3Class GUI_update_clock ERROR: Exceptions: %s" % exceptions)
                    traceback.print_exc()
                #######################################################
                #######################################################

            #######################################################
            #######################################################
            #######################################################

        #######################################################
        #######################################################
        #######################################################
        #######################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def EncodersList_HomingButtonObjectsResponse(self, EncoderChannelNumber):

        self.EncodersList_NeedsToBeHomedFlag[EncoderChannelNumber] = 1
        #self.MyPrint_WithoutLogFile("EncodersList_HomingButtonObjectsResponse: Event fired for EncoderChannelNumber " + str(EncoderChannelNumber))

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def MyPrint_WithoutLogFile(self, input_string):

        input_string = str(input_string)

        if input_string != "":

            #input_string = input_string.replace("\n", "").replace("\r", "")

            ################################ Write to console
            # Some people said that print crashed for pyinstaller-built-applications and that sys.stdout.write fixed this.
            # http://stackoverflow.com/questions/13429924/pyinstaller-packaged-application-works-fine-in-console-mode-crashes-in-window-m
            if self.PrintToConsoleFlag == 1:
                sys.stdout.write(input_string + "\n")
            ################################

            ################################ Write to GUI
            self.PrintToGui_Label_TextInputHistory_List.append(self.PrintToGui_Label_TextInputHistory_List.pop(0)) #Shift the list
            self.PrintToGui_Label_TextInputHistory_List[-1] = str(input_string) #Add the latest value

            self.PrintToGui_Label_TextInput_Str = ""
            for Counter, Line in enumerate(self.PrintToGui_Label_TextInputHistory_List):
                self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + Line

                if Counter < len(self.PrintToGui_Label_TextInputHistory_List) - 1:
                    self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + "\n"
            ################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def IsInputList(self, InputToCheck):

        result = isinstance(InputToCheck, list)
        return result
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self, input, number_of_leading_numbers = 4, number_of_decimal_places = 3):

        number_of_decimal_places = max(1, number_of_decimal_places) #Make sure we're above 1

        ListOfStringsToJoin = []

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if isinstance(input, str) == 1:
            ListOfStringsToJoin.append(input)
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, int) == 1 or isinstance(input, float) == 1:
            element = float(input)
            prefix_string = "{:." + str(number_of_decimal_places) + "f}"
            element_as_string = prefix_string.format(element)

            ##########################################################################################################
            ##########################################################################################################
            if element >= 0:
                element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1)  # +1 for sign, +1 for decimal place
                element_as_string = "+" + element_as_string  # So that our strings always have either + or - signs to maintain the same string length
            else:
                element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1 + 1)  # +1 for sign, +1 for decimal place
            ##########################################################################################################
            ##########################################################################################################

            ListOfStringsToJoin.append(element_as_string)
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, list) == 1:

            if len(input) > 0:
                for element in input: #RECURSION
                    ListOfStringsToJoin.append(self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a list() or []
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, tuple) == 1:

            if len(input) > 0:
                for element in input: #RECURSION
                    ListOfStringsToJoin.append("TUPLE" + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a list() or []
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, dict) == 1:

            if len(input) > 0:
                for Key in input: #RECURSION
                    ListOfStringsToJoin.append(str(Key) + ": " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input[Key], number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a dict()
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        else:
            ListOfStringsToJoin.append(str(input))
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if len(ListOfStringsToJoin) > 1:

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            StringToReturn = ""
            for Index, StringToProcess in enumerate(ListOfStringsToJoin):

                ################################################
                if Index == 0: #The first element
                    if StringToProcess.find(":") != -1 and StringToProcess[0] != "{": #meaning that we're processing a dict()
                        StringToReturn = "{"
                    elif StringToProcess.find("TUPLE") != -1 and StringToProcess[0] != "(":  # meaning that we're processing a tuple
                        StringToReturn = "("
                    else:
                        StringToReturn = "["

                    StringToReturn = StringToReturn + StringToProcess.replace("TUPLE","") + ", "
                ################################################

                ################################################
                elif Index < len(ListOfStringsToJoin) - 1: #The middle elements
                    StringToReturn = StringToReturn + StringToProcess + ", "
                ################################################

                ################################################
                else: #The last element
                    StringToReturn = StringToReturn + StringToProcess

                    if StringToProcess.find(":") != -1 and StringToProcess[-1] != "}":  # meaning that we're processing a dict()
                        StringToReturn = StringToReturn + "}"
                    elif StringToProcess.find("TUPLE") != -1 and StringToProcess[-1] != ")":  # meaning that we're processing a tuple
                        StringToReturn = StringToReturn + ")"
                    else:
                        StringToReturn = StringToReturn + "]"

                ################################################

            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

        elif len(ListOfStringsToJoin) == 1:
            StringToReturn = ListOfStringsToJoin[0]

        else:
            StringToReturn = ListOfStringsToJoin

        return StringToReturn
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ConvertDictToProperlyFormattedStringForPrinting(self, DictToPrint, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3):

        ProperlyFormattedStringForPrinting = ""
        ItemsPerLineCounter = 0

        for Key in DictToPrint:

            ##########################################################################################################
            if isinstance(DictToPrint[Key], dict): #RECURSION
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     str(Key) + ":\n" + \
                                                     self.ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key], NumberOfDecimalsPlaceToUse, NumberOfEntriesPerLine, NumberOfTabsBetweenItems)

            else:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     str(Key) + ": " + \
                                                     self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DictToPrint[Key], 0, NumberOfDecimalsPlaceToUse)
            ##########################################################################################################

            ##########################################################################################################
            if ItemsPerLineCounter < NumberOfEntriesPerLine - 1:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\t"*NumberOfTabsBetweenItems
                ItemsPerLineCounter = ItemsPerLineCounter + 1
            else:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\n"
                ItemsPerLineCounter = 0
            ##########################################################################################################

        return ProperlyFormattedStringForPrinting
    ##########################################################################################################
    ##########################################################################################################
