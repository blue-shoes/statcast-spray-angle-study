import pandas as pd
from pandas import DataFrame, Series
import os
import math
import warnings

import pybaseball
from pybaseball import statcast

pybaseball.cache.enable()


def _was_fair(series: Series) -> bool:
    return "foul" not in series["des"]


def _is_bip(series: Series) -> bool:
    return "homers" not in series["des"]


def _is_caught(series: Series) -> bool:
    des = series["des"]
    if "flies out" in des:
        return True
    if "sacrifice fly" in des:
        return True
    if "lines out" in des:
        return True
    return "pops out" in des


def get_statcast_data(year: int) -> DataFrame:
    sc_file = f"data/sc_{year}.csv"
    if os.path.exists(sc_file):
        return pd.read_csv(sc_file)

    with warnings.catch_warnings():
        warnings.simplefilter(action="ignore", category=FutureWarning)
        raw_sc = statcast(start_dt=f"{year}-01-01", end_dt=f"{year}-12-31")

    sc_no_st = raw_sc.loc[raw_sc["game_type"] != "S"]
    sc_batted_balls = sc_no_st.loc[sc_no_st["type"] == "X"].copy()
    sc_batted_balls.dropna(axis=0, subset="hc_x", inplace=True)
    sc_batted_balls["bip"] = sc_batted_balls.apply(_is_bip, axis=1)
    sc_batted_balls["caught"] = sc_batted_balls.apply(_is_caught, axis=1)
    sc_min = sc_batted_balls.loc[
        sc_batted_balls.bip & sc_batted_balls.caught, ["des", "hc_x", "hc_y"]
    ]
    sc_min["act_fair"] = sc_min.apply(_was_fair, axis=1)

    if not os.path.exists("data"):
        os.mkdir("data")
    sc_min.to_csv(f"data/sc_{year}.csv")

    return sc_min.copy()


def populate_spray_angle(series: Series, x: float, y: float) -> float:
    num = series["hc_x"] - x
    denom = y - series["hc_y"]

    if denom == 0:
        if num == 0:
            return 0
        return (num / abs(num)) * 90

    if num == 0:
        if denom > 0:
            return 0
        return 180

    if denom < 0:
        return (num / abs(num)) * 180 * (1 - math.atan(num / denom) / math.pi)

    rad_angle = math.atan(num / denom)

    return 180 * rad_angle / math.pi


def should_be_fair(series: Series) -> bool:
    return -45 <= series["spray"] <= 45
