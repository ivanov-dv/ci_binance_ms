import config


class Verifier:
    time_periods = config.TIME_PERIODS

    @classmethod
    def check_time_period(cls, value: str):
        if value in cls.time_periods:
            return value
        else:
            raise ValueError(f"Временной отрезок {value} не поддерживается")
