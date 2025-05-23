from modbus_interface import InverterProfile, ModbusController
from strategy_engine import ControlStrategy
from scheduler import Scheduler
import time
import datetime
import yaml

# Load configuration from YAML file
def load_yaml_config(path):
    with open(path, 'r') as file:
        return yaml.safe_load(file)

def current_hour():
    return datetime.datetime.now().hour

def main():
    # Load external YAML configuration for specific inverter/strategy
    config = load_yaml_config("configs/vikend-baterija.yml")

    # Setup inverter based on config
    profile = InverterProfile(
        model=config['inverter_type'],
        reg_soc=12307,  # Placeholder values, to be loaded from profile
        reg_mode=5000,
        reg_discharge_current=12305,
        reg_power_output=12400
    )
    inverter = ModbusController(ip=config['connection']['ip'], port=config['connection']['port'], profile=profile)
    strategy = ControlStrategy(config)
    schedule = Scheduler()

    while True:
        soc = inverter.read_soc()
        hour = current_hour()
        action = strategy.decide(soc, hour)

        if action == "discharge":
            inverter.set_mode(profile.reg_mode, 1)
            inverter.set_discharge_current(profile.reg_discharge_current, 60)
        elif action == "hold":
            inverter.set_mode(profile.reg_mode, 0)

        print(f"[INFO] Hour={hour}, SOC={soc}, Action={action}")
        time.sleep(300)

if __name__ == "__main__":
    main()
