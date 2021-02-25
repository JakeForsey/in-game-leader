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
            print(f"Unable to determine side from {location}")
            return None