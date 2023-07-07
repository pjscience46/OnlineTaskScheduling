import math

class Model:
    name: str

    def __init(self):
        pass

    def get_alpha(self) -> float:
        raise NotImplementedError

    def get_mu(self) -> float:
        raise NotImplementedError


class AmdahlModel(Model):
    name = "Amdahl"

    def get_alpha(self) -> float:
        return (math.sqrt(2) + 1 + math.sqrt(2 * math.sqrt(2) - 1)) / 2

    def get_mu(self) -> float:
        return (1 - math.sqrt(8 * math.sqrt(2) - 11)) / 2


class CommunicationModel(Model):
    name = "Communication"

    def get_alpha(self) -> float:
        return 4 / 3

    def get_mu(self) -> float:
        return (23 - math.sqrt(313)) / 18


class GeneralModel(Model):
    name = "General"

    def get_alpha(self) -> float:
        return 2

    def get_mu(self) -> float:
        return (33 - math.sqrt(738)) / 27


class RooflineModel(Model):
    name = "Roofline"

    def get_alpha(self) -> float:
        return 1

    def get_mu(self) -> float:
        return (3 - math.sqrt(5)) / 2


