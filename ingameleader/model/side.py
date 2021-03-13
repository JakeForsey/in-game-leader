import enum
import logging

from ingameleader.utils import format_location


logger = logging.getLogger(__name__)


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
            logger.warning("Unable to determine side from %s", location)
            return None

    @staticmethod
    def from_initial(initial):
        if initial == "T":
            return Side.T
        elif initial == "CT":
            return Side.CT
        else:
            logger.warning("Unable to determine side from %s", initial)
            return None

    @staticmethod
    def from_playing_on_team(playing_on_team):
        playing_on_team = playing_on_team.lower()
        for ct_text in ["counter", "cdunter"]:
            if ct_text in playing_on_team:
                return Side.CT

        for t_text in ["terrorist", "terrdrist"]:
            if t_text in playing_on_team:
                return Side.T

        logger.warning("Unable to determine side from %s", playing_on_team)
        return None
