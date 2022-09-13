from __future__ import annotations
from typing import Union
from datetime import datetime
from pydantic import BaseModel, Field


class Ticker(BaseModel):
    symbol: str
    kline: dict[str, Union[Kline, None]]


class Kline(BaseModel):
    type: str = Field(alias='e')
    time: datetime = Field(alias='E')
    symbol: str = Field(alias='s')
    data: KlineData = Field(alias='k')

    class Config:
        allow_population_by_field_name = True


class KlineData(BaseModel):
    startTime: datetime = Field(alias='t')
    closeTime: datetime = Field(alias='T')
    symbol: str = Field(alias='s')
    interval: str = Field(alias='i')
    firstTradeId: int = Field(alias='f')
    lastTradeId: int = Field(alias='L')
    openPrice: float = Field(alias='o')
    closePrice: float = Field(alias='c')
    highPrice: float = Field(alias='h')
    lowPrice: float = Field(alias='l')
    baseAssetVolume: float = Field(alias='v', default=0.0)
    numberOfTrades: int = Field(alias='n')
    isThisKlineClosed: bool = Field(alias='x')
    quoteAssetVolume: float = Field(alias='q')
    takerBuyBaseAssetVolume: str = Field(alias='V')
    takerBuyQuoteAssetVolume: float = Field(alias='Q')
    ignore: str = Field(alias='B')

    class Config:
        allow_population_by_field_name = True


Kline.update_forward_refs()
Ticker.update_forward_refs()
