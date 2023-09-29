from colorama import Fore
from uncertainty.utypes import sbool, ubool
from uncertainty.utypes import ufloat


class UncertainElement:
    def __init__(self, element, opinions=None):
        if opinions is None:
            opinions = []
        self.element = element
        self.opinions = opinions


class Room:
    def __init__(self, humidity: ufloat, max_humid: float, temp: ufloat, max_temp: float):
        self.humidity = humidity
        self.temp = temp
        self.max_temp = max_temp
        self.max_humid = max_humid

    @property
    def ac_on(self) -> ubool:
        return (self.temp >= 25.0) | (self.humidity >= 80.0)


if __name__ == "__main__":
    max_temp = 25
    max_humid = 80

    print(f"--Living room--")
    living_room_temp = ufloat(24.7, 0.5)
    print(f"Temperature:\t{living_room_temp}ºC")
    living_room_humid = ufloat(79, 1)
    print(f"Humidity:\t\t{living_room_humid} %")
    living_room = Room(living_room_humid, max_humid, living_room_temp, max_temp)
    print(f"{Fore.GREEN}AC ON:\t\t\t{str(living_room.ac_on)}{Fore.RESET}")
    print("")
    print(f"Do you trust the sensor readings?")
    alice_s_opinion = sbool(0.8, 0.0, 0.2, living_room.ac_on.uncertainty)
    print(f"Alice:\t{alice_s_opinion}")
    bob_s_opinion = sbool(0.7, 0.0, 0.3, living_room.ac_on.uncertainty)
    print(f"Bob:\t{bob_s_opinion}")
    cam_s_opinion = sbool(0.0, 0.0, 1.0, living_room.ac_on.uncertainty)
    print(f"Cam:\t{cam_s_opinion}")
    ac_on_ue = UncertainElement(living_room.ac_on, [alice_s_opinion, bob_s_opinion, cam_s_opinion])
    fusion = sbool.weightedFusion(ac_on_ue.opinions)
    print(f"{Fore.GREEN}{fusion} -> {fusion.toubool()}{Fore.RESET}")

    print(f" -- Kitchen -- ")
    kitchen_temp = ufloat(25.5, 0.5)
    print(f"Temperature:\t{kitchen_temp}ºC")
    kitchen_humid = ufloat(79, 1)
    print(f"Humidity:\t\t{kitchen_humid} %")
    kitchen = Room(kitchen_humid, max_humid, kitchen_temp, max_temp)
    print(f"{Fore.GREEN}AC ON:\t\t\t{str(kitchen.ac_on)}{Fore.RESET}")

    print(f"")
    print(f"Do you trust the sensor readings?")
    alice_s_opinion = sbool(0.0, 0.8, 0.2, kitchen.ac_on.uncertainty)
    print(f"Alice:\t{alice_s_opinion}")
    bob_s_opinion = sbool(0.0, 0.5, 0.5, kitchen.ac_on.uncertainty)
    print(f"Bob:\t{bob_s_opinion}")
    cam_s_opinion = sbool(0.0, 0.6, 0.4, kitchen.ac_on.uncertainty)
    print(f"Cam:\t{cam_s_opinion}")
    ac_on_ue = UncertainElement(kitchen.ac_on, [alice_s_opinion, bob_s_opinion, cam_s_opinion])
    fusion = sbool.weightedFusion(ac_on_ue.opinions)
    print(f"{Fore.GREEN}{fusion} -> {fusion.toubool()}{Fore.RESET}")
