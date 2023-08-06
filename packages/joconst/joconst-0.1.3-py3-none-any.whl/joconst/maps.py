from joconst.constant import TdxMarket, Exchange, Interval
from jotdx.params import TDXParams

TDX_JONPY_MARKET_MAP = {
    TdxMarket.DCE: Exchange.DCE,
    TdxMarket.SGE: Exchange.SGE,
    TdxMarket.CFFEX: Exchange.CFFEX,
    TdxMarket.SHFE: Exchange.SHFE,
    TdxMarket.CZCE: Exchange.CZCE,
}

INTERVAL_TDX_MAP = {
    Interval.MINUTE: TDXParams.KLINE_TYPE_1MIN,
    Interval.MINUTE_5: TDXParams.KLINE_TYPE_5MIN,
    Interval.MINUTE_15: TDXParams.KLINE_TYPE_15MIN,
    Interval.MINUTE_30: TDXParams.KLINE_TYPE_30MIN,
    Interval.HOUR: TDXParams.KLINE_TYPE_1HOUR,
    Interval.DAILY: TDXParams.KLINE_TYPE_DAILY
}

EXCHANGE_NAME_MAP = {
    Exchange.SHFE: "上海期货",
    Exchange.DCE: "大连商品",
    Exchange.CZCE: "郑州商品",
    Exchange.CFFEX: "中金所期货",
    Exchange.SGE: "上海黄金"
}
