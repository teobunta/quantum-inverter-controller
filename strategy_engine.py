
class ControlStrategy:
    def __init__(self, profile):
        self.profile = profile

    def decide(self, soc, hour):
        if soc > 90 and (hour >= 23 or hour < 5):
            return "discharge"
        return "hold"
