import pytest

from utils.models import UniqueUserRequest, PercentOfTime, PercentOfPoint, Price, Way, Period


class TestMonitoring:

    def test_check_all_changes(self):
        user_requests = (
            UniqueUserRequest(Symbol('BTCUSDT'), PercentOfPoint(5, 66000), Way.all),
            UniqueUserRequest(Symbol('BTCUSDT'), PercentOfPoint(10, 60000), Way.all),
            UniqueUserRequest(Symbol('BTCUSDT'), PercentOfPoint(10, 60000), Way.down_to),
            UniqueUserRequest(Symbol('BTCUSDT'), PercentOfPoint(10, 66000), Way.down_to),
            UniqueUserRequest(Symbol('BTCUSDT'), PercentOfPoint(10, 60000), Way.up_to),
            UniqueUserRequest(Symbol('BTCUSDT'), PercentOfPoint(10, 66000), Way.up_to),
            UniqueUserRequest(Symbol('BTCUSDT'), Price(65000), Way.up_to),
            UniqueUserRequest(Symbol('BTCUSDT'), Price(65000), Way.down_to),
            UniqueUserRequest(Symbol('BTCUSDT'), PercentOfTime(1, Period.v_24h), Way.all),
            UniqueUserRequest(Symbol('BTCUSDT'), PercentOfTime(1, Period.v_24h), Way.up_to),
            UniqueUserRequest(Symbol('BTCUSDT'), PercentOfTime(1, Period.v_24h), Way.down_to),
            UniqueUserRequest(Symbol('BTCUSDT'), PercentOfTime(5, Period.v_24h), Way.all),
            UniqueUserRequest(Symbol('BTCUSDT'), PercentOfTime(5, Period.v_24h), Way.up_to),
            UniqueUserRequest(Symbol('BTCUSDT'), PercentOfTime(5, Period.v_24h), Way.down_to),
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
            UniqueUserRequest(Symbol('BTCUSDT'), PercentOfPoint(10, 60000), Way.all),
            UniqueUserRequest(Symbol('BTCUSDT'), PercentOfPoint(10, 60000), Way.up_to),
            UniqueUserRequest(Symbol('BTCUSDT'), Price(65000), Way.up_to),
            UniqueUserRequest(Symbol('BTCUSDT'), PercentOfTime(1, Period.v_24h), Way.all),
            UniqueUserRequest(Symbol('BTCUSDT'), PercentOfTime(1, Period.v_24h), Way.down_to)
        }
        assert res_monitoring == res

    def test_response(self):
        self.request_repo.user_requests = {}
        self.request_repo.unique_user_requests = {}

        from engine import binance_bot
        monitoring = Monitoring(binance_bot)
        self.request_repo.add(8866, UniqueUserRequest('BTCUSDT', PercentOfTime(20, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('ETHUSDT', PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('ETHUSDT', PercentOfPoint(10, 3600), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('XRPUSDT', PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('XRPUSDT', PercentOfPoint(5, 0.2), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('BTCusdt', Price(60000), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('ETHusdt', Price(300), Way.down_to))
        self.request_repo.add(8866, UniqueUserRequest('ETHusdt', Price(3000), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('XRPusdt', Price(100), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('XRPusdt', Price(0.1), Way.down_to))
        self.request_repo.add(8866, UniqueUserRequest('BNBUSDT', PercentOfTime(20, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('SOLUSDT', PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('BNBUSDT', PercentOfPoint(10, 3600), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('XRPUSDT', PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('NOTUSDT', PercentOfPoint(5, 0.2), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('DOGEusdt', Price(60000), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('WLDusdt', Price(300), Way.down_to))
        self.request_repo.add(8866, UniqueUserRequest('INJusdt', Price(3000), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('FILusdt', Price(100), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('ENAusdt', Price(0.1), Way.down_to))
        self.request_repo.add(8866, UniqueUserRequest('PEOPLEUSDT', PercentOfTime(20, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('HIGHUSDT', PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('IOUSDT', PercentOfPoint(10, 3600), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('FLOKIUSDT', PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('NEARUSDT', PercentOfPoint(5, 0.2), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('Wusdt', Price(60000), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('ARBusdt', Price(300), Way.down_to))
        self.request_repo.add(8866, UniqueUserRequest('LEVERusdt', Price(3000), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('BBusdt', Price(100), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('RUNEusdt', Price(0.1), Way.down_to))
        self.request_repo.add(8866, UniqueUserRequest('FETUSDT', PercentOfTime(20, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('LTCUSDT', PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('MATICUSDT', PercentOfPoint(10, 3600), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('TRXUSDT', PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('OPUSDT', PercentOfPoint(5, 0.2), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('LINKusdt', Price(60000), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('FTMusdt', Price(300), Way.down_to))
        self.request_repo.add(8866, UniqueUserRequest('ROSEusdt', Price(3000), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('TRUusdt', Price(100), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('SUIusdt', Price(0.1), Way.down_to))
        self.request_repo.add(8866, UniqueUserRequest('GALAUSDT', PercentOfTime(20, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('LPTUSDT', PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('OMUSDT', PercentOfPoint(10, 3600), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('TNSRUSDT', PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('CHZUSDT', PercentOfPoint(5, 0.2), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('TIAusdt', Price(60000), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('APTusdt', Price(300), Way.down_to))
        self.request_repo.add(8866, UniqueUserRequest('STXusdt', Price(3000), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('EURusdt', Price(100), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('CRVusdt', Price(0.1), Way.down_to))
        self.request_repo.add(8866, UniqueUserRequest('DOTUSDT', PercentOfTime(20, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('TAOUSDT', PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('ARUSDT') PercentOfPoint(10, 3600), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('SEIUSDT', PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('BCHUSDT', PercentOfPoint(5, 0.2), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('ETCusdt', Price(60000), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('PYTHusdt', Price(300), Way.down_to))
        self.request_repo.add(8866, UniqueUserRequest('ARKMusdt', Price(3000), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('LDOusdt', Price(100), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('RSRusdt', Price(0.1), Way.down_to))
        self.request_repo.add(8866, UniqueUserRequest('AEVOUSDT', PercentOfTime(20, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('PIXELUSDT', PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('ENSUSDT', PercentOfPoint(10, 3600), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('CKBUSDT', PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('AGIXUSDT', PercentOfPoint(5, 0.2), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('MANTAusdt', Price(60000), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('JTOusdt', Price(300), Way.down_to))
        self.request_repo.add(8866, UniqueUserRequest('BICOusdt', Price(3000), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('ATOMusdt', Price(100), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('REZusdt', Price(0.1), Way.down_to))
        self.request_repo.add(8866, UniqueUserRequest('DYDXUSDT', PercentOfTime(20, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('JUPUSDT', PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('BAKEUSDT', PercentOfPoint(10, 3600), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('AMPUSDT', PercentOfTime(10, Period.v_24h), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('BLZUSDT', PercentOfPoint(5, 0.2), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('MKRusdt', Price(60000), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('CAKEusdt', Price(300), Way.down_to))
        self.request_repo.add(8866, UniqueUserRequest('HBARusdt', Price(3000), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('CFXusdt', Price(100), Way.up_to))
        self.request_repo.add(8866, UniqueUserRequest('GRTusdt', Price(0.1), Way.down_to))
        requests_for_server = self.request_repo.do_unique_requests_for_server()
        res = monitoring.get_response_from_server(requests_for_server)

        for req in requests_for_server:
            if isinstance(req.data_request, (Price, PercentOfPoint)):
                assert req.symbol in res[TypeRequest.price]
            if isinstance(req.data_request, PercentOfTime):
                assert req.symbol in res[TypeRequest.period]
                assert req.data_request.period in res[TypeRequest.period][req.symbol]
