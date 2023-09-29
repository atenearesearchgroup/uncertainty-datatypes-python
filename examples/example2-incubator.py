from enum import Enum
from abc import ABC, abstractmethod

from uncertainty.utypes import *

class IncubatorState(Enum):
    Heating = 1
    CoolingDown = 2

class ActiveObject:

    @abstractmethod
    def action(self):
        pass

class Clock:

    def __init__(self):
        self.now : float = 0.0
        self.timeStep : float = 3
        self.activeObjects : list[ActiveObject] = [] 

    def tick(self):
        self.now = self.now + self.timeStep
        for o in filter(lambda p : not isinstance(p, Controller), self.activeObjects):
            o.action()
        
        for o in filter(lambda p : isinstance(p, Controller), self.activeObjects):
            o.action()
    
    def run(self, n:int):
        for i in range(n):
            self.tick()

    def addObject(self, activeObject):
        if isinstance(activeObject, ActiveObject):
            self.activeObjects.append(activeObject)


class Incubator(ActiveObject):
    def __init__(self):
        super().__init__()
        self.cAir : ufloat #  mass of object inside box * capacity of air inside box
        self.gBox : ufloat #  link the difference between the room temperature and the air temperature inside the box with the energy flowing to the box
        self.voltage : ufloat = ufloat(0, 0.05)
        self.onVoltage : ufloat = ufloat(18, 0.05)
        self.current : ufloat = ufloat(4, 0.05)
        self.tBair : ufloat = ufloat(22.8125, 0.05) #  temperature inside box
        self.tRoom : ufloat = ufloat(20, 0.05) #  temperature of the room
        self.currentState : IncubatorState = IncubatorState.CoolingDown
        self.numericalPrecision : ufloat = ufloat(0, 0.05)
    
    @abstractmethod
    def calculateTemperature(self, timeIncrement : ufloat) -> ufloat:
        pass
    

class Incubator2P(Incubator):
    def init(self):
        super().__init__()
        self.cAir = ufloat(616.56, 0.05)
        self.gBox = ufloat(0.65, 0.05)
        
    def calculateTemperature(self, timeIncrement : ufloat) -> ufloat:
            (1/self.cAir)*(self.voltage * self.current * timeIncrement - self.gBox * (self.tBair - self.tRoom))
    
    def action(self):
            self.tBair : self.tBair + self.clock.timeStep*self.calculateTemperature(self.clock.timeStep)


class Incubator4P(Incubator):
    def __init__(self, clock):
        super().__init__()
        self.tHeater : ufloat = ufloat(25,0.05)
        self.cAir: ufloat = ufloat(486.12, 0.05)
        self.gBox: ufloat = ufloat(0.856, 0.05)
        self.cHeater: ufloat = ufloat(33.65, 0.05)
        self.gHeater: ufloat = ufloat(0.87, 0.05)
        self.clock: Clock = clock

    def caculateHeaterTemperature(self, timeIncrement : ufloat) -> ufloat:
        return (1/self.cHeater) * (self.voltage * self.current * timeIncrement - self.gHeater * (self.tHeater - self.tBair))
        
    def calculateTemperature(self, timeIncrement : ufloat) -> ufloat:
        return (1/self.cAir) * (self.gHeater * (self.tHeater-self.tBair) - self.gBox * (self.tBair - self.tRoom))
        
    def action(self):
        self.tHeater = self.tHeater + self.clock.timeStep * self.caculateHeaterTemperature(self.clock.timeStep)
        self.tBair = self.tBair + self.clock.timeStep * self.calculateTemperature(self.clock.timeStep)


class Controller(ActiveObject):
    def __init__(self, clock, incubator):
        super().__init__()
        self.desiredTemp : ufloat = ufloat(28, 0.05)
        self.lowerBound : ufloat = ufloat(3, 0.05)
        self.tolerance : float = 0.99999
        self.incubator: Incubator = incubator
        self.clock: Clock = clock
    
    def action(self):            
        if self.incubator.currentState == IncubatorState.Heating and (self.incubator.tBair >= self.desiredTemp).confidence > self.tolerance:
            self.incubator.currentState = IncubatorState.CoolingDown
            self.incubator.voltage = ufloat(0, 0.05)
        elif (self.incubator.currentState == IncubatorState.CoolingDown) and ((self.incubator.tBair <= (self.desiredTemp - self.lowerBound)).confidence > self.tolerance):
            self.incubator.currentState = IncubatorState.Heating
            self.incubator.voltage = self.incubator.onVoltage

        print(str(self.clock.now) + '\t| ' + str(self.incubator.tBair.value) + '\t| ' + str(self.incubator.tBair.uncertainty))


clock = Clock()
incubator4p = Incubator4P(clock)
controller = Controller(clock, incubator4p)

clock.addObject(incubator4p)
clock.addObject(controller)

print("Time\t| Temperature\t\t| Uncertainty")
print("------------------------------------------------------")
clock.run(15)