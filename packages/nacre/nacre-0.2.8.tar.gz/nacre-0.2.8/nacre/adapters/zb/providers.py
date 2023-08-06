import asyncio
import time
from decimal import Decimal
from typing import Any, Dict, List

from nautilus_trader.common.logging import Logger
from nautilus_trader.common.logging import LoggerAdapter
from nautilus_trader.common.providers import InstrumentProvider
from nautilus_trader.model.c_enums.currency_type import CurrencyType
from nautilus_trader.model.currency import Currency
from nautilus_trader.model.identifiers import InstrumentId
from nautilus_trader.model.identifiers import Symbol
from nautilus_trader.model.identifiers import Venue
from nautilus_trader.model.instruments.crypto_perp import CryptoPerpetual
from nautilus_trader.model.instruments.currency import CurrencySpot
from nautilus_trader.model.objects import Money
from nautilus_trader.model.objects import Price
from nautilus_trader.model.objects import Quantity

from nacre.adapters.zb.common import format_websocket_market
from nacre.adapters.zb.http.api.future_market import ZbFutureMarketHttpAPI


def _quote_precision(quote_asset: str) -> int:
    if quote_asset in ("ZUSD", "USDT", "QC", "BTC"):
        return 8  # hardcode for now
    else:
        raise ValueError(f"{quote_asset} currency can't be found")


class ZbInstrumentProvider(InstrumentProvider):
    """
    An example template of an ``InstrumentProvider`` showing the minimal methods
    which must be implemented for an integration to be complete.
    """

    def __init__(
        self,
        logger: Logger,
        venue: Venue,
        market_api: ZbFutureMarketHttpAPI,
        account_type: str,
    ):
        super().__init__()

        self._log = LoggerAdapter(type(self).__name__, logger)

        self.venue = venue
        self._market = market_api
        self._local_symbols_to_instrument_id = {}  # type: dict[str, InstrumentId]
        self._local_market_id_to_instrument_id = {}  # type: dict[str, InstrumentId]
        self._account_type = account_type

        self._loaded = False
        self._loading = False

    async def load_all_or_wait_async(self) -> None:
        """
        Load the latest ZB instruments into the provider asynchronously, or
        await loading.
        If `load_async` has been previously called then will immediately return.
        """
        if self._loaded:
            return  # Already loaded

        if not self._loading:
            self._log.debug("Loading instruments...")
            await self.load_all_async()
            self._log.info(f"Loaded {self.count} instruments.")
        else:
            self._log.debug("Awaiting loading...")
            while self._loading:
                # Wait 100ms
                await asyncio.sleep(0.1)

    async def load_future_markets(self):
        markets: List[Dict] = await self._market.market_list()
        for market in markets:
            # Create base asset
            base_asset = market["sellerCurrencyName"].upper()
            base_currency = Currency(
                code=base_asset,
                precision=int(market["priceDecimal"]),
                iso4217=0,  # Currently undetermined for crypto assets
                name=base_asset,
                currency_type=CurrencyType.CRYPTO,
            )

            # Create quote asset
            quote_asset = market["buyerCurrencyName"].upper()
            quote_currency = Currency(
                code=quote_asset,
                precision=_quote_precision(quote_asset),
                iso4217=0,  # Currently undetermined for crypto assets
                name=quote_asset,
                currency_type=CurrencyType.CRYPTO,
            )

            symbol = Symbol(base_currency.code + "/" + quote_currency.code)
            # symbol = Symbol(market["symbol"])
            instrument_id = InstrumentId(symbol=symbol, venue=self.venue)

            # NOTE: ZB api doesn't provide info about tick size, simulate using price_precision
            price_increment = Price(
                value=1 / (10 ** int(market["priceDecimal"])), precision=int(market["priceDecimal"])
            )
            size_increment = Quantity(
                value=1 / (10 ** int(market["amountDecimal"])),
                precision=int(market["amountDecimal"]),
            )

            # TODO: query vip status programmatically
            # default fee rate is 0.075% for taker, 0.025% for vip taker
            # default fee rate is 0 for maker, -0.025% for vip maker
            maker_fee: Decimal = Decimal("-0.00025")  # vip
            taker_fee: Decimal = Decimal("0.00025")  # vip
            # maker_fee: Decimal = Decimal(0)
            # taker_fee: Decimal = Decimal("0.00075")

            instrument = CryptoPerpetual(
                instrument_id=instrument_id,
                native_symbol=Symbol(market["symbol"]),
                base_currency=base_currency,
                quote_currency=quote_currency,
                settlement_currency=quote_currency,  # for USDT-based markets, settlement == quote
                is_inverse=False,
                price_precision=int(market["priceDecimal"]),
                size_precision=int(market["amountDecimal"]),
                price_increment=price_increment,
                size_increment=size_increment,
                max_quantity=Quantity(market["maxAmount"], int(market["amountDecimal"])),
                min_quantity=Quantity(market["minAmount"], int(market["amountDecimal"])),
                max_notional=None,
                min_notional=Money(market["minTradeMoney"], currency=quote_currency),
                max_price=None,
                min_price=None,
                margin_init=Decimal(0),
                margin_maint=Decimal(0),
                maker_fee=maker_fee,
                taker_fee=taker_fee,
                ts_event=time.time_ns(),
                ts_init=time.time_ns(),
                info=market,
            )
            self.add_currency(currency=base_currency)
            self.add_currency(currency=quote_currency)
            self.add(instrument=instrument)
            self._local_symbols_to_instrument_id[market["symbol"]] = instrument.id
            self._local_market_id_to_instrument_id[market["id"]] = instrument.id

    async def load_spot_markets(self):
        markets: Dict[str, Any] = await self._market.markets()
        for market, entry in markets.items():
            base, _, quote = market.partition("_")

            # Create base asset
            base_asset = base.upper()
            base_currency = Currency(
                code=base_asset,
                precision=4,  # Hardcoded for zb spot
                iso4217=0,  # Currently undetermined for crypto assets
                name=base_asset,
                currency_type=CurrencyType.CRYPTO,
            )

            # Create quote asset
            quote_asset = quote.upper()
            quote_currency = Currency(
                code=quote_asset,
                precision=_quote_precision(quote_asset),
                iso4217=0,  # Currently undetermined for crypto assets
                name=quote_asset,
                currency_type=CurrencyType.CRYPTO,
            )

            symbol = Symbol(base_currency.code + "/" + quote_currency.code)
            instrument_id = InstrumentId(symbol=symbol, venue=self.venue)

            price_increment = Price(
                value=1 / (10 ** int(entry["priceScale"])),
                precision=int(entry["priceScale"]),
            )
            size_increment = Quantity(
                value=1 / (10 ** int(entry["amountScale"])),
                precision=int(entry["amountScale"]),
            )
            instrument = CurrencySpot(
                instrument_id=instrument_id,
                native_symbol=Symbol(market),
                base_currency=base_currency,
                quote_currency=quote_currency,
                price_precision=int(entry["priceScale"]),
                size_precision=int(entry["amountScale"]),
                price_increment=price_increment,
                size_increment=size_increment,
                lot_size=None,
                max_quantity=None,
                min_quantity=Quantity(entry["minAmount"], int(entry["minAmount"])),
                max_notional=None,
                min_notional=None,
                max_price=None,
                min_price=None,
                margin_init=Decimal(0),
                margin_maint=Decimal(0),
                maker_fee=Decimal("0.002"),
                taker_fee=Decimal("0.002"),
                ts_event=time.time_ns(),
                ts_init=time.time_ns(),
                info=entry,
            )
            self.add_currency(currency=base_currency)
            self.add_currency(currency=quote_currency)
            self.add(instrument=instrument)
            self._local_symbols_to_instrument_id[market] = instrument.id
            # Spot websocket return symbol like "BTC/USDT" in "btcusdt", map it here
            ws_symbol = format_websocket_market(symbol.value)
            self._local_market_id_to_instrument_id[ws_symbol] = instrument.id

    async def load_all_async(self):
        """
        Load the latest ZB instruments into the provider asynchronously.
        """
        self._loading = True

        if self._account_type == "future":
            await self.load_future_markets()
        elif self._account_type == "spot":
            await self.load_spot_markets()

        # Set async loading flags
        self._loading = False
        self._loaded = True

    def find_instrument_id_by_local_symbol(self, local_symbol: str) -> InstrumentId:
        return self._local_symbols_to_instrument_id[local_symbol]

    def find_instrument_id_by_local_market_id(self, market_id: str) -> InstrumentId:
        return self._local_market_id_to_instrument_id[market_id]

    def list_local_market_ids(self) -> List[str]:
        return list(self._local_market_id_to_instrument_id.keys())
