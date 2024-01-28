from enum import Enum
import time
import psutil
from statistics import mean,stdev,median,geometric_mean

from uncertainty.utypes import *

class IncubatorState(Enum):
    Heating = 1
    CoolingDown = 2

desiredTemp : ufloat = ufloat(28, 0.05)
lowerBound : ufloat = ufloat(3, 0.05)

voltage : ufloat = ufloat(0, 0.05)
onVoltage : ufloat = ufloat(18, 0.05)
current : ufloat = ufloat(4, 0.05)
tBair : ufloat = ufloat(22.8125, 0.05) #  temperature inside box
tRoom : ufloat = ufloat(20, 0.05) #  temperature of the room
currentState : IncubatorState = IncubatorState.CoolingDown
tHeater : ufloat = ufloat(25,0.05)
cAir: ufloat = ufloat(486.12, 0.05) #  mass of object inside box * capacity of air inside box
gBox: ufloat = ufloat(0.856, 0.05) #  link the difference between the room temperature and the air temperature inside the box with the energy flowing to the box
cHeater: ufloat = ufloat(33.65, 0.05)
gHeater: ufloat = ufloat(0.87, 0.05)

def caculateHeaterTemperature(timeIncrement : float) -> ufloat:
  return (voltage*current*timeIncrement - gHeater*(tHeater-tBair))/cHeater
        
def calculateTemperature() -> ufloat:
   return (gHeater*(tHeater-tBair) - gBox*(tBair-tRoom))/cAir

now : float = 0.0
timeStep : float = 3

numExecs=30

results=[]
averages=[]
medians=[]
gmeans=[]
stdevs=[]

for repetitions in range(10000,50001,10000):
    print(repetitions)
    for n in range(numExecs):
        now = 0.0
        voltage = ufloat(0, 0.05)
        onVoltage = ufloat(18, 0.05)
        current  = ufloat(4, 0.05)
        tBair  = ufloat(22.8125, 0.05) #  temperature inside box
        tRoom  = ufloat(20, 0.05) #  temperature of the room
        currentState : IncubatorState = IncubatorState.CoolingDown
        tHeater  = ufloat(25,0.05)
        cAir = ufloat(486.12, 0.05) #  mass of object inside box * capacity of air inside box
        gBox = ufloat(0.856, 0.05) #  link the difference between the room temperature and the air temperature inside the box with the energy flowing to the box
        cHeater = ufloat(33.65, 0.05)
        gHeater = ufloat(0.87, 0.05)

        start = time.process_time()
        for i in range(repetitions):
            now = now + timeStep
            # COMPUTATION
            if currentState == IncubatorState.Heating and (tBair >= desiredTemp):
                currentState = IncubatorState.CoolingDown
                voltage = ufloat(0.0, 0.05)
            elif (currentState == IncubatorState.CoolingDown) and (tBair <= (desiredTemp - lowerBound)):
                currentState = IncubatorState.Heating
                voltage = onVoltage
            tHeater =  tHeater.value + timeStep * caculateHeaterTemperature(timeStep) # ours (to explicitly deal with correlations)
            tBair =  tBair.value + timeStep * calculateTemperature()
            # print(str(now) + '\t| ' + str(currentState)+ '\t| ' + str(tBair))
            # END OF COMPUTATION
        end = time.process_time() - start
        results.append(end)
        # print(str(now) + '\t| ' + str(end) + '\t| ' + str(currentState)+ '\t| ' + str(tBair))
    averages.append(mean(results))
    medians.append(median(results))
    gmeans.append(geometric_mean(results))
    stdevs.append(stdev(results))
print(averages)
print(medians)
print(gmeans)
print(stdevs)

p = psutil.Process()
print('Memory peak: ' + str(p.memory_info().peak_wset) + ' Bytes')