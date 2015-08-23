#!/usr/bin/python3

# RX seriale da RaspberryPi -------------------------------------------------------------
# |
# valvFanCoil[int/255]
# valvFreddo[int/255]
# valvCaldo[int/255]
# releFanCoil[bool]
# releFreddo[bool]
# releCaldo[bool]
# releAriaSpinta[bool]
# releAriaEstratta[bool]
# releTrasfPannello[bool]
# releTrasfValvole[bool]
# releComandoManuale[bool]

# TX seriale verso RaspberryPi ----------------------------------------------------------
# |

# tempTuboCaldaiaIn[float]
# tempTuboCaldaiaOut[float]
# tempTuboTermosifoniOut[float]
# tempTuboTermosifoniIn[float]
# tempTuboCaldoUtaOut[float]
# tempTuboCaldoUtaIn[float]
# tempTuboFanCoilOut[float]
# tempTuboFanCoilIn[float]
# tempTuboFreddoUtaOut[float]
# tempTuboFreddoUtaIn[float]
# tempTuboCondizionatoreIn[float]
# tempTuboCondizionatoreOut[float]
# tempAriaInUTA[float]
# umidAriaInUTA[float]
# tempAriaOutUTA[float]
# umidAriaOutUTA[float]
# tempAriaEstratta[float]
# umidAriaEstratta[float]
# tempAriaEsterna[float]
# umidAriaEsterna[float]

import time
import configparser
import cherrypy

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

def serialread():
	line=ser.readline()
	inputArray=line.decode('utf-8').split(",")

def utacooler(step):
	if valveStatus[0] > 0:
		valveStatus[0] = valveStatus[0] - step
	else:
		if (compressorOn = 1):
			valveStatus[2] = valveStatus[2] + step

def utahotter(step):
	if valveStatus[2] > 0:
		valveStatus[2] = valveStatus[2] - step
	else:
		if (heaterOn = 1):
			valveStatus[0] = valveStatus[0] + step

def uta():
	if relaisStatus[4] == 1:	#If UTA fan turned on
		if (inputArray[14] > utaAirOut+utaTempDelta):
			utacooler(1);
		elif (inputArray[14] < utaAirOut-utaTempDelta):
			utahotter(1);
	else:
		valveStatus[0] = 0
		valveStatus[2] = 0
		time.sleep(0.25)


def fancoil():
	if relaisStatus[8] == 1:
		if (inputArray[6] > fancoilWaterOut-fancoilTempDelta):
			valveStatus[1] = valveStatus[1]-1
		elif (inputArray[6] < fancoilWaterOut+fancoilTempDelta):
			valveStatus[1] = valveStatus[1]+1
	else:
		valveStatus[1] = 0
		time.sleep(0.25)



#MAIN INIT
config = configparser.ConfigParser()
config.read("hvac.conf")

heaterOn 		= config["General"]["heaterOn"]
compressorOn 	= config["General"]["compressorOn"]

utaAirOut 		= config["Temp"]["utaAirOut"]
utaTempDelta 	= config["Temp"]["utaTempDelta"]
fancoilWaterOut = config["Temp"]["fancoilWaterOut"]
fancoilTempDelta= config["Temp"]["fancoilTempDelta"]

relaisStatus = [0,0,0,0,0,0,0,0]
valveStatus  = [0,0,0]
inputArray	 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
needHeat	 = [0,0]
needCold	 = [0,0]



class hvacAPI(object):
	@cherrypy.expose
	def action(self,id=0,status=0):
		answer = ""
		relaisStatus[id] = status



cherrypy.server.socket_host = "0.0.0.0"
cherrypy.quickstart(hvacAPI())