import datetime
import enum
import time

from dataclasses import dataclass
from datetime import datetime as dt


class User:
    def __init__(
            self,
            id_telegram: int,
            name: str,
            surname: str,
            username: str,
            date_registration,
            date_update,
            ban: bool = False):
        self.id_telegram = id_telegram
        self.name = name
        self.surname = surname
        self.username = username
        self.date_registration = date_registration
        self.date_update = date_update
        self.ban = ban

    def __repr__(self):
        return (f"User({self.id_telegram}, {self.name}, {self.surname}, {self.username},"
                f" {self.ban}, {self.date_registration}, {self.date_update})")

    def __str__(self):
        return (f"User id: {self.id_telegram}\n"
                f"Name: {self.name}\n"
                f"Surname: {self.surname}\n"
                f"Username: {self.username}\n"
                f"Ban: {self.ban}\n"
                f"Date registration: {self.date_registration}\n"
                f"Date update: {self.date_update})")

    def __eq__(self, other):
        if isinstance(other, User):
            return self.id_telegram == other.id_telegram
        return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.id_telegram)


class Session:
    def __init__(self, user_id):
        self.user_id = user_id
        self.time_update = time.time()


class Symbol:
    def __init__(self, symbol: str):
        self.symbol = symbol.upper()

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return self.symbol

    def __eq__(self, other):
        if isinstance(other, Symbol):
            return self.symbol == other.symbol
        if isinstance(other, str):
            return self.symbol == other

    def __ne__(self, other):
        if isinstance(other, Symbol):
            return self.symbol != other.symbol
        if isinstance(other, str):
            return self.symbol != other

    def __hash__(self):
        return hash(self.symbol)


class Period(enum.Enum):
    v_4h = '4 hours ago'
    v_8h = '8 hours ago'
    v_12h = '12 hours ago'
    v_24h = '1 day ago'


class TypeRequest(enum.Enum):
    period = 'period'
    price = 'price'


class Way(enum.Enum):
    up_to = 'up_to'
    down_to = 'down_to'
    all = 'all'


@dataclass(frozen=True)
class Percent:
    target_percent: float


@dataclass(frozen=True)
class PercentOfPoint(Percent):
    current_price: float


@dataclass(frozen=True)
class PercentOfTime(Percent):
    period: Period


@dataclass(frozen=True)
class Price:
    target_price: float


class TimeInfo:
    def __init__(self):
        self.create_time: datetime.datetime = dt.utcnow()
        self.update_time: datetime.datetime = self.create_time
        self.create_time_unix: float = time.time()
        self.update_time_unix: float = self.create_time_unix


class BaseRequest:

    def __init__(self):
        self.symbol = None
        self.data_request = None
        self.way = None
        self.time_info = TimeInfo()


class UserRequest(BaseRequest):
    """
    Класс запросов пользователя.
    Сравнение экземпляров позволяет выявить дубли (время создания и обновления не учитывается).
    """

    def __init__(
            self,
            symbol: Symbol,
            data_request: PercentOfTime | PercentOfPoint | Price,
            way: Way):
        super().__init__()
        self.symbol = symbol
        self.way = way
        self.data_request = data_request

    def __str__(self):
        return f"UserRequest({self.symbol}, {self.data_request}, {self.way})"

    def __repr__(self):
        return f"UserRequest({self.symbol}, {self.data_request}, {self.way})"

    def __eq__(self, other):
        if isinstance(other, UserRequest):
            return (self.symbol, self.data_request, self.way) == (other.symbol, other.data_request, other.way)
        return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.symbol, self.data_request, self.way))


class RequestForServer(BaseRequest):
    """
    В данном классе реализовано сравнение экземпляров запросов,
    которые позволяет сформировать уникальные запросы, поместив их в set().
    """

    def __init__(self, user_request: UserRequest):
        super().__init__()
        self.symbol = user_request.symbol
        self.data_request = user_request.data_request

    def __str__(self):
        return f"RequestForServer({self.symbol}, {self.data_request})"

    def __repr__(self):
        return f"RequestForServer({self.symbol}, {self.data_request})"

    def __eq__(self, other):
        if isinstance(other, RequestForServer):
            if isinstance(self.data_request, PercentOfTime) and isinstance(other.data_request, PercentOfTime):
                return (self.symbol, self.data_request.period) == (other.symbol, other.data_request.period)
            if (isinstance(self.data_request, (Price, PercentOfPoint)) and
                    isinstance(other.data_request, (Price, PercentOfPoint))):
                return self.symbol == other.symbol
            return (self.symbol, self.data_request) == (other.symbol, other.data_request)
        return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        # if isinstance(self.data_request, PercentOfTime):
        #     return hash((self.symbol, self.data_request.period))
        return hash(self.symbol)


class BaseResponse:
    pass


class ResponseKline(BaseResponse):
    def __init__(
            self,
            open_time,
            open_price,
            high_price,
            low_price,
            close_price,
            volume,
            close_time,
            quote_asset_volume,
            number_of_trades,
            taker_buy_base_asset_volume,
            taker_buy_quote_asset_volume
    ):
        """
        Первые 11 элементов списка из ответа сервера по запросу client.get_klines
        """

        self.open_time = open_time
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        self.volume = volume
        self.close_time = close_time
        self.quote_asset_volume = quote_asset_volume
        self.number_of_trades = number_of_trades
        self.taker_buy_base_asset_volume = taker_buy_base_asset_volume
        self.taker_buy_quote_asset_volume = taker_buy_quote_asset_volume


class ResponseGetTicker(BaseResponse):
    def __init__(self, data_dict: dict):
        """
        Ответ сервера по запросу client.get_ticker
        """

        self.symbol = data_dict['symbol']
        self.price_change = float(data_dict['priceChange'])
        self.price_change_percent = float(data_dict['priceChangePercent'])
        self.weighted_avg_price = float(data_dict['weightedAvgPrice'])
        self.prev_close_price = float(data_dict['prevClosePrice'])
        self.last_price = float(data_dict['lastPrice'])
        self.bid_price = float(data_dict['bidPrice'])
        self.ask_price = float(data_dict['askPrice'])
        self.open_price = float(data_dict['openPrice'])
        self.high_price = float(data_dict['highPrice'])
        self.low_price = float(data_dict['lowPrice'])
        self.volume = float(data_dict['volume'])
        self.open_time = float(data_dict['openTime'])
        self.close_time = float(data_dict['closeTime'])
