
from modbus_interface import InverterProfile, ModbusController
from strategy_engine import ControlStrategy
from scheduler import Scheduler
import datetime
import time

def load_inverter_profile(model: str) -> InverterProfile:
    profiles = {
        "Deye": InverterProfile(
            model="Deye 12kW LV",
            reg_soc=12307,
            reg_mode=5000,
            reg_discharge_current=12305,
            reg_power_output=12400
        ),
        "Sinexcel": InverterProfile(
            model="Sinexcel 100kW PCS",
            reg_soc=30021,
            reg_mode=40001,
            reg_discharge_current=40005,
            reg_power_output=40010
        )
    }
    return profiles.get(model)

def main():
    inverter_model = "Deye"
    profile = load_inverter_profile(inverter_model)
    controller = ModbusController(ip="192.168.1.100", port=502, profile=profile)
    strategy = ControlStrategy(profile)
    schedule = Scheduler()

    while True:
        soc = controller.read_soc()
        hour = datetime.datetime.now().hour
        action = strategy.decide(soc, hour)
        if action == "discharge":
            controller.set_mode(profile.reg_mode, 1)
            controller.set_discharge_current(profile.reg_discharge_current, 60)
        elif action == "hold":
            controller.set_mode(profile.reg_mode, 0)
        print(f"[INFO] Hour={hour}, SOC={soc}, Action={action}")
        time.sleep(300)

if __name__ == "__main__":
    main()
