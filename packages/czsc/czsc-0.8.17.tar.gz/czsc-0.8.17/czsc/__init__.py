# coding: utf-8

from .analyze import CZSC
from .traders.advanced import CzscAdvancedTrader
from .utils.ta import SMA, EMA, MACD, KDJ
from .objects import Freq, Operate, Direction, Signal, Factor, Event, RawBar, NewBar
from . import aphorism

__version__ = "0.8.17"
__author__ = "zengbin93"
__email__ = "zeng_bin8888@163.com"
__date__ = "20220218"

print(f"欢迎使用CZSC！当前版本标识为 {__version__}@{__date__}\n")

aphorism.print_one()

