from enum import Enum

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

for repetitions in range(50_000):
    now = now + timeStep
    if currentState == IncubatorState.Heating and (tBair >= desiredTemp):
        currentState = IncubatorState.CoolingDown
        voltage = ufloat(0.0, 0.05)
    elif (currentState == IncubatorState.CoolingDown) and (tBair <= (desiredTemp - lowerBound)):
        currentState = IncubatorState.Heating
        voltage = onVoltage
    tHeater =  tHeater.value + timeStep * caculateHeaterTemperature(timeStep) # ours (to explicitly deal with correlations)
    tBair =  tBair.value + timeStep * calculateTemperature()
    print(str(now) + '\t| ' + str(currentState)+ '\t| ' + str(tBair))
