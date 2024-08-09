import enum

from pydantic import BaseModel


class Period(enum.Enum):
    v_4h = "4h"
    v_8h = "8h"
    v_12h = "12h"
    v_24h = "24h"


class Way(enum.Enum):
    up_to = "up_to"
    down_to = "down_to"
    all = "all"


class TypeRequest(enum.Enum):
    price = "price"
    period = "period"


class PercentOfPoint(BaseModel):
    target_percent: float
    current_price: float
    weight: int
    type_request: str = "percent_of_point"


class PercentOfTime(BaseModel):
    target_percent: float
    period: Period
    weight: int
    type_request: str = "percent_of_time"


class Price(BaseModel):
    target_price: float
    weight: int
    type_request: str = "price"


class UniqueUserRequest(BaseModel):
    request_id: int
    symbol: str
    way: Way
    request_data: PercentOfTime | PercentOfPoint | Price

    def __repr__(self):
        return (f'UniqueUserRequest(request_id={self.request_id}, symbol="{self.symbol}", '
                f'way={self.way}, request_data={self.request_data})')

    def __str__(self):
        return self.__repr__()


class RequestForServer(BaseModel):
    symbol: str
    request_data: PercentOfTime | PercentOfPoint | Price

    def __repr__(self):
        return f'RequestForServer(symbol="{self.symbol}", request_data={self.request_data})'

    def __str__(self):
        return self.__repr__()


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

    def __repr__(self):
        return f"ResponseKline(open_time={self.open_time}, open_price={self.open_price}, " \
               f"high_price={self.high_price}, low_price={self.low_price}, close_price={self.close_price}, " \
               f"volume={self.volume}, close_time={self.close_time}, quote_asset_volume={self.quote_asset_volume}, " \
               f"number_of_trades={self.number_of_trades}, taker_buy_base_asset_volume={self.taker_buy_base_asset_volume}, " \
               f"taker_buy_quote_asset_volume={self.taker_buy_quote_asset_volume})"


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

    def __repr__(self):
        return (f"ResponseGetTicker(symbol={self.symbol}, price_change={self.price_change}, "
                f"price_change_percent={self.price_change_percent}, weighted_avg_price={self.weighted_avg_price}, "
                f"prev_close_price={self.prev_close_price}, last_price={self.last_price}, "
                f"bid_price={self.bid_price}, ask_price={self.ask_price}, open_price={self.open_price}, "
                f"high_price={self.high_price}, low_price={self.low_price}, volume={self.volume}, "
                f"open_time={self.open_time}, close_time={self.close_time})")
