import enum

from ingameleader.utils import format_location


class Side(enum.Enum):
    CT = 0
    T = 1

    @staticmethod
    def from_location(location):
        if location == format_location("CT Start"):
            return Side.CT
        elif location == format_location("T Start"):
            return Side.T
        else:
            print(f"WARNING: Unable to determine side from {location}")
            return None

    @staticmethod
    def from_initial(initial):
        if initial == "T":
            return Side.T
        elif initial == "CT":
            return Side.CT
        else:
            print(f"WARNING: Unable to determine side from {initial}")
            return None
