from datetime import datetime, timezone

from pydantic.datetime_parse import parse_datetime


class ZonedDateTime(datetime):
    @classmethod
    def __get_validators__(cls):
        yield parse_datetime

    @staticmethod
    def to_str(dt: datetime) -> str:
        return dt.strftime("%Y-%m-%dT%H:%M:%S")
