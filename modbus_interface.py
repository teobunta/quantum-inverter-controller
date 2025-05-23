
from dataclasses import dataclass

@dataclass
class InverterProfile:
    model: str
    reg_soc: int
    reg_mode: int
    reg_discharge_current: int
    reg_power_output: int

class ModbusController:
    def __init__(self, ip, port, profile):
        self.ip = ip
        self.port = port
        self.profile = profile

    def read_soc(self):
        return 95  # Simulacija

    def set_mode(self, reg, mode):
        print(f"Setting mode {mode} at reg {reg}")

    def set_discharge_current(self, reg, amps):
        print(f"Setting discharge current {amps}A at reg {reg}")
