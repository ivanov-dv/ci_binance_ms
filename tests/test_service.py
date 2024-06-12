import pytest

from utils.service import *
from utils.repositories import *


class TestRequest:
    @staticmethod
    def test_comparison_request_server():
        ex1 = RequestForServer(UserRequest(Symbol('BtcUsdT'), Price(70000.1), Way.down_to))
        ex2 = RequestForServer(UserRequest(Symbol('BTCUSDT'), Price(60000.1), Way.up_to))
        ex3 = RequestForServer(UserRequest(Symbol('BtcUsdT'), PercentOfPoint(23.5, 65000), Way.up_to))
        ex4 = RequestForServer(UserRequest(Symbol('BTCUSDT'), PercentOfPoint(-3.5, 65000), Way.up_to))
        ex5 = RequestForServer(UserRequest(Symbol('BTCUSDT'), PercentOfTime(-3.5, Period.v_24h), Way.up_to))
        ex6 = RequestForServer(UserRequest(Symbol('BTCUSDT'), PercentOfTime(-3.5, Period.v_4h), Way.up_to))
        ex7 = RequestForServer(UserRequest(Symbol('BTCUSDT'), PercentOfTime(-3.5, Period.v_4h), Way.up_to))
        assert ex1 == ex2
        assert ex3 == ex4
        assert ex1 == ex3
        assert ex1 != ex5
        assert ex4 != ex5
        assert ex5 != ex6
        assert ex6 == ex7

    @staticmethod
    def test_comparison_user_request():
        ex1 = UserRequest(Symbol('BTcuSDT'), PercentOfTime(20.5, Period.v_24h), Way.up_to)
        ex2 = UserRequest(Symbol('btcuSDT'), PercentOfTime(20.5, Period.v_24h), Way.up_to)
        ex3 = UserRequest(Symbol('btcuSDT'), PercentOfTime(20.4, Period.v_24h), Way.up_to)
        assert ex1 == ex2
        assert ex2 != ex3

    @staticmethod
    @pytest.mark.parametrize(
        "ex1, ex2",
        [
            (RequestForServer(UserRequest(Symbol('BTCUSDT'), Price(60000.1), Way.up_to)),
             RequestForServer(UserRequest(Symbol('BTCUSD'), Price(60000.1), Way.up_to))),
            (RequestForServer(UserRequest(Symbol('BTCUSDT'), PercentOfPoint(-3.5, 70000), Way.up_to)),
             RequestForServer(UserRequest(Symbol('EThUSDT'), PercentOfPoint(-3.5, 70000), Way.up_to))),
            (UserRequest(Symbol('BTcuSDt'), PercentOfTime(20.5, Period.v_24h), Way.up_to),
             UserRequest(Symbol('BTcuSDT'), PercentOfTime(20.5, Period.v_4h), Way.up_to))
        ]
    )
    def test_comparison_requests_different(ex1, ex2):
        assert ex1 != ex2


class TestRepositories:
    request_repo = RequestRepository('db')

    user_request1 = UserRequest(Symbol('btcusdt'), PercentOfTime(23, Period.v_24h), Way.up_to)
    user_request2 = UserRequest(Symbol('btcusdt'), PercentOfTime(23, Period.v_24h), Way.up_to)
    user_request3 = UserRequest(Symbol('btcusdt'), PercentOfPoint(23, 70000), Way.up_to)
    user_request4 = UserRequest(Symbol('ethusdt'), PercentOfPoint(23, 70000), Way.up_to)
    user_request5 = UserRequest(Symbol('btcusdt'), Price(69000), Way.up_to)
    user_request6 = UserRequest(Symbol('btcusdt'), Price(68000), Way.down_to)
    user_request7 = UserRequest(Symbol('ETHUsdt'), PercentOfTime(23, Period.v_24h), Way.up_to)

    def test_add(self):
        self.request_repo.user_requests = {}
        self.request_repo.unique_user_requests = {}

        self.request_repo.add(1, self.user_request1)
        self.request_repo.add(1, self.user_request2)
        self.request_repo.add(1, self.user_request3)
        self.request_repo.add(1, self.user_request4)
        self.request_repo.add(1, self.user_request5)
        self.request_repo.add(1, self.user_request6)
        self.request_repo.add(2, self.user_request2)
        self.request_repo.add(2, self.user_request4)
        self.request_repo.add(2, self.user_request5)

        res_user_requests = {1: {UserRequest(Symbol('btcusdt'), PercentOfTime(23, Period.v_24h), Way.up_to),
                                 UserRequest(Symbol('btcusdt'), PercentOfPoint(23, 70000), Way.up_to),
                                 UserRequest(Symbol('ethusdt'), PercentOfPoint(23, 70000), Way.up_to),
                                 UserRequest(Symbol('btcusdt'), Price(69000), Way.up_to),
                                 UserRequest(Symbol('btcusdt'), Price(68000), Way.down_to)},
                             2: {UserRequest(Symbol('btcusdt'), PercentOfTime(23, Period.v_24h), Way.up_to),
                                 UserRequest(Symbol('ethusdt'), PercentOfPoint(23, 70000), Way.up_to),
                                 UserRequest(Symbol('btcusdt'), Price(69000), Way.up_to)}}
        res_unique = {UserRequest(Symbol('btcusdt'), PercentOfTime(23, Period.v_24h), Way.up_to): {1, 2},
                      UserRequest(Symbol('btcusdt'), PercentOfPoint(23, 70000), Way.up_to): {1},
                      UserRequest(Symbol('ethusdt'), PercentOfPoint(23, 70000), Way.up_to): {1, 2},
                      UserRequest(Symbol('btcusdt'), Price(69000), Way.up_to): {1, 2},
                      UserRequest(Symbol('btcusdt'), Price(68000), Way.down_to): {1}}
        assert self.request_repo.user_requests == res_user_requests
        assert self.request_repo.unique_user_requests == res_unique
        assert self.request_repo.get(1, self.user_request1) == self.user_request1
        assert self.request_repo.get(1, self.user_request7) is None
        assert self.request_repo.get_all_for_user_id(2) == res_user_requests[2]

        self.request_repo.delete(1, self.user_request2)  # req2 = req1
        self.request_repo.delete(1, self.user_request3)
        self.request_repo.delete(1, self.user_request5)
        self.request_repo.delete(2, self.user_request2)
        self.request_repo.delete(2, self.user_request4)
        self.request_repo.delete(2, self.user_request5)

        res_user_requests_delete = {1: {self.user_request4, self.user_request6}}
        res_unique_delete = {UserRequest(Symbol('ethusdt'), PercentOfPoint(23, 70000), Way.up_to): {1},
                             UserRequest(Symbol('btcusdt'), Price(68000), Way.down_to): {1}}

        assert self.request_repo.user_requests == res_user_requests_delete
        assert self.request_repo.unique_user_requests == res_unique_delete

    def test_response(self):
        self.request_repo.user_requests = {}
        self.request_repo.unique_user_requests = {}

        from engine import binance_bot
        resp_repo = ResponseRepository('123', binance_bot)
        self.request_repo.add(8866, UserRequest(Symbol('BTCUSDT'), PercentOfTime(20, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('ETHUSDT'), PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('ETHUSDT'), PercentOfPoint(10, 3600), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('XRPUSDT'), PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('XRPUSDT'), PercentOfPoint(5, 0.2), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('BTCusdt'), Price(60000), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('ETHusdt'), Price(300), Way.down_to))
        self.request_repo.add(8866, UserRequest(Symbol('ETHusdt'), Price(3000), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('XRPusdt'), Price(100), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('XRPusdt'), Price(0.1), Way.down_to))
        self.request_repo.add(8866, UserRequest(Symbol('BNBUSDT'), PercentOfTime(20, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('SOLUSDT'), PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('BNBUSDT'), PercentOfPoint(10, 3600), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('XRPUSDT'), PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('NOTUSDT'), PercentOfPoint(5, 0.2), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('DOGEusdt'), Price(60000), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('WLDusdt'), Price(300), Way.down_to))
        self.request_repo.add(8866, UserRequest(Symbol('INJusdt'), Price(3000), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('FILusdt'), Price(100), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('ENAusdt'), Price(0.1), Way.down_to))
        self.request_repo.add(8866, UserRequest(Symbol('PEOPLEUSDT'), PercentOfTime(20, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('HIGHUSDT'), PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('IOUSDT'), PercentOfPoint(10, 3600), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('FLOKIUSDT'), PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('NEARUSDT'), PercentOfPoint(5, 0.2), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('Wusdt'), Price(60000), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('ARBusdt'), Price(300), Way.down_to))
        self.request_repo.add(8866, UserRequest(Symbol('LEVERusdt'), Price(3000), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('BBusdt'), Price(100), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('RUNEusdt'), Price(0.1), Way.down_to))
        self.request_repo.add(8866, UserRequest(Symbol('FETUSDT'), PercentOfTime(20, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('LTCUSDT'), PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('MATICUSDT'), PercentOfPoint(10, 3600), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('TRXUSDT'), PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('OPUSDT'), PercentOfPoint(5, 0.2), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('LINKusdt'), Price(60000), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('FTMusdt'), Price(300), Way.down_to))
        self.request_repo.add(8866, UserRequest(Symbol('ROSEusdt'), Price(3000), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('TRUusdt'), Price(100), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('SUIusdt'), Price(0.1), Way.down_to))
        self.request_repo.add(8866, UserRequest(Symbol('GALAUSDT'), PercentOfTime(20, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('LPTUSDT'), PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('OMUSDT'), PercentOfPoint(10, 3600), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('TNSRUSDT'), PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('CHZUSDT'), PercentOfPoint(5, 0.2), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('TIAusdt'), Price(60000), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('APTusdt'), Price(300), Way.down_to))
        self.request_repo.add(8866, UserRequest(Symbol('STXusdt'), Price(3000), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('EURusdt'), Price(100), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('CRVusdt'), Price(0.1), Way.down_to))
        self.request_repo.add(8866, UserRequest(Symbol('DOTUSDT'), PercentOfTime(20, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('TAOUSDT'), PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('ARUSDT'), PercentOfPoint(10, 3600), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('SEIUSDT'), PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('BCHUSDT'), PercentOfPoint(5, 0.2), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('ETCusdt'), Price(60000), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('PYTHusdt'), Price(300), Way.down_to))
        self.request_repo.add(8866, UserRequest(Symbol('ARKMusdt'), Price(3000), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('LDOusdt'), Price(100), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('RSRusdt'), Price(0.1), Way.down_to))
        self.request_repo.add(8866, UserRequest(Symbol('AEVOUSDT'), PercentOfTime(20, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('PIXELUSDT'), PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('ENSUSDT'), PercentOfPoint(10, 3600), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('CKBUSDT'), PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('AGIXUSDT'), PercentOfPoint(5, 0.2), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('MANTAusdt'), Price(60000), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('JTOusdt'), Price(300), Way.down_to))
        self.request_repo.add(8866, UserRequest(Symbol('BICOusdt'), Price(3000), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('ATOMusdt'), Price(100), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('REZusdt'), Price(0.1), Way.down_to))
        self.request_repo.add(8866, UserRequest(Symbol('DYDXUSDT'), PercentOfTime(20, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('JUPUSDT'), PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('BAKEUSDT'), PercentOfPoint(10, 3600), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('AMPUSDT'), PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('BLZUSDT'), PercentOfPoint(5, 0.2), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('MKRusdt'), Price(60000), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('CAKEusdt'), Price(300), Way.down_to))
        self.request_repo.add(8866, UserRequest(Symbol('HBARusdt'), Price(3000), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('CFXusdt'), Price(100), Way.up_to))
        self.request_repo.add(8866, UserRequest(Symbol('GRTusdt'), Price(0.1), Way.down_to))
        requests_for_server = self.request_repo.do_unique_requests_for_server()
        res = resp_repo.get_response_from_server(requests_for_server)

        for req in requests_for_server:
            if isinstance(req.data_request, (Price, PercentOfPoint)):
                assert req.symbol in res[TypeRequest.price]
            if isinstance(req.data_request, PercentOfTime):
                assert req.symbol in res[TypeRequest.period]
                assert req.data_request.period in res[TypeRequest.period][req.symbol]


class TestMonitoring:
    class Client:
        pass

    ex_monitoring = Monitoring(Client())

    def test_check_all_changes(self):
        user_requests = (
            UserRequest(Symbol('BTCUSDT'), PercentOfPoint(5, 66000), Way.all),
            UserRequest(Symbol('BTCUSDT'), PercentOfPoint(10, 60000), Way.all),
            UserRequest(Symbol('BTCUSDT'), PercentOfPoint(10, 60000), Way.down_to),
            UserRequest(Symbol('BTCUSDT'), PercentOfPoint(10, 66000), Way.down_to),
            UserRequest(Symbol('BTCUSDT'), PercentOfPoint(10, 60000), Way.up_to),
            UserRequest(Symbol('BTCUSDT'), PercentOfPoint(10, 66000), Way.up_to),
            UserRequest(Symbol('BTCUSDT'), Price(65000), Way.up_to),
            UserRequest(Symbol('BTCUSDT'), Price(65000), Way.down_to),
            UserRequest(Symbol('BTCUSDT'), PercentOfTime(1, Period.v_24h), Way.all),
            UserRequest(Symbol('BTCUSDT'), PercentOfTime(1, Period.v_24h), Way.up_to),
            UserRequest(Symbol('BTCUSDT'), PercentOfTime(1, Period.v_24h), Way.down_to),
            UserRequest(Symbol('BTCUSDT'), PercentOfTime(5, Period.v_24h), Way.all),
            UserRequest(Symbol('BTCUSDT'), PercentOfTime(5, Period.v_24h), Way.up_to),
            UserRequest(Symbol('BTCUSDT'), PercentOfTime(5, Period.v_24h), Way.down_to),
        )
        resp_klines = [[1718161020000, '67416.05000000', '67424.00000000', '67403.47000000', '67423.99000000', '16.27187000', 1718161079999, '1096929.92503660', 953, '14.05869000', '947727.05331980', '0'], [1718161080000, '67423.99000000', '67424.00000000', '67390.00000000', '67412.88000000', '17.88840000', 1718161139999, '1205803.03555260', 619, '11.85720000', '799239.09187210', '0'], [1718161140000, '67412.89000000', '67415.26000000', '67412.89000000', '67415.26000000', '0.82518000', 1718161199999, '55629.70425540', 105, '0.74282000', '50077.38426540', '0']]
        list_response = [ResponseKline(*map(float, i[:11])) for i in resp_klines]
        resp_get_ticker = {'symbol': 'BTCUSDT', 'priceChange': '-792.24000000', 'priceChangePercent': '-1.161', 'weightedAvgPrice': '67209.61946402', 'prevClosePrice': '68228.73000000', 'lastPrice': '67436.48000000', 'lastQty': '0.00013000', 'bidPrice': '67436.47000000', 'bidQty': '4.21751000', 'askPrice': '67436.48000000', 'askQty': '5.53934000', 'openPrice': '68228.72000000', 'highPrice': '68488.00000000', 'lowPrice': '66051.00000000', 'volume': '36978.88700000', 'quoteVolume': '2485336923.47281260', 'openTime': 1718074837077, 'closeTime': 1718161237077, 'firstId': 3630981707, 'lastId': 3632578416, 'count': 1596710}
        response_from_server = {
            TypeRequest.price:
                {
                    Symbol('BTCUSDT'):
                        list_response
                },
            TypeRequest.period:
                {
                    Symbol('BTCUSDT'):
                        {
                            Period.v_24h:
                                ResponseGetTicker(resp_get_ticker)
                        }
                }
        }
        res_monitoring = self.ex_monitoring.check_all_changes(user_requests, response_from_server)
        res = {
            UserRequest(Symbol('BTCUSDT'), PercentOfPoint(10, 60000), Way.all),
            UserRequest(Symbol('BTCUSDT'), PercentOfPoint(10, 60000), Way.up_to),
            UserRequest(Symbol('BTCUSDT'), Price(65000), Way.up_to),
            UserRequest(Symbol('BTCUSDT'), PercentOfTime(1, Period.v_24h), Way.all),
            UserRequest(Symbol('BTCUSDT'), PercentOfTime(1, Period.v_24h), Way.down_to)
        }
        assert res_monitoring == res
