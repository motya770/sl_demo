import datetime


class DateUtils:

    @staticmethod
    def current_minute_key(timestamp: int) -> str:
        key_date = datetime.datetime.fromtimestamp(timestamp)
        return key_date.strftime("%Y-%m-%d_%H")

    @staticmethod
    def current_hour_key(timestamp: int) -> str:
        key_date = datetime.datetime.fromtimestamp(timestamp)
        return key_date.strftime("%Y-%m-%d")

    @staticmethod
    def round_minute_key() -> str:
        one_minute = datetime.timedelta(minutes=1)
        key_date = datetime.datetime.utcnow()
        round_date = key_date - one_minute
        return round_date.strftime("%Y-%m-%d_%H")

    @staticmethod
    def round_minute_date():
        one_minute = datetime.timedelta(minutes=1)
        key_date = datetime.datetime.utcnow()
        round_date = key_date - one_minute
        round_minute = round_date.strftime("%Y-%m-%d %H:%M")
        result = datetime.datetime.fromisoformat(round_minute) + datetime.timedelta(seconds=59)
        return result

    @staticmethod
    def is_bigger_than_round_minute(timestamp: int) -> bool:
        timestamp_date = datetime.datetime.fromtimestamp(timestamp)
        round_date = DateUtils.round_minute_date()
        return timestamp_date > round_date

    @staticmethod
    def round_hour_key() -> str:
        one_hour = datetime.timedelta(hour=1)
        key_date = datetime.datetime.utcnow()
        round_date = key_date - one_hour
        return round_date.strftime("%Y-%m-%d")

