from joconst.constant import TdxMarket, Exchange, Interval
from jotdx.params import TDXParams

TDX_JONPY_MARKET_MAP = {
    TdxMarket.DCE: Exchange.DCE.value,
    TdxMarket.SGE: Exchange.SGE.value,
    TdxMarket.CFFEX: Exchange.CFFEX.value,
    TdxMarket.SHFE: Exchange.SHFE.value,
    TdxMarket.CZCE: Exchange.CZCE.value,
}

# 这里 dict 的 key 要用 value,
# 因为 vnpy 中的 constant 和 joconst 中的 Enum class 在 dict key 中被视为两个不同的东西
INTERVAL_TDX_MAP = {
    Interval.MINUTE.value: TDXParams.KLINE_TYPE_1MIN,
    Interval.MINUTE_5.value: TDXParams.KLINE_TYPE_5MIN,
    Interval.MINUTE_15.value: TDXParams.KLINE_TYPE_15MIN,
    Interval.MINUTE_30.value: TDXParams.KLINE_TYPE_30MIN,
    Interval.HOUR.value: TDXParams.KLINE_TYPE_1HOUR,
    Interval.DAILY.value: TDXParams.KLINE_TYPE_DAILY
}

EXCHANGE_NAME_MAP = {
    Exchange.SHFE.value: "上海期货",
    Exchange.DCE.value: "大连商品",
    Exchange.CZCE.value: "郑州商品",
    Exchange.CFFEX.value: "中金所期货",
    Exchange.SGE.value: "上海黄金"
}
