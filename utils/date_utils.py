from datetime import datetime


class DateUtils:

    @staticmethod
    def current_minute_key(timestamp: int) -> str:
        key_date = datetime.fromtimestamp(timestamp)
        return key_date.strftime("%Y-%m-%d_%H:%M")

    @staticmethod
    def current_hour_key(timestamp: int) -> str:
        key_date = datetime.fromtimestamp(timestamp)
        return key_date.strftime("%Y-%m-%d_%H")

    @staticmethod
    def round_minute_key() -> str:
        one_minute = datetime.timedelta(minutes=1)
        key_date = datetime.utcnow()
        round_date = key_date - one_minute
        return round_date.strftime("%Y-%m-%d_%H:%M")

    @staticmethod
    def round_hour_key() -> str:
        one_hour = datetime.timedelta(minutes=1)
        key_date = datetime.utcnow()
        round_date = key_date - one_hour
        return round_date.strftime("%Y-%m-%d_%H")

