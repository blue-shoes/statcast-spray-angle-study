import pandas as pd
from pandas import DataFrame, Series
import os

import pybaseball
from pybaseball import statcast

pybaseball.cache.enable()


def _was_fair(series: Series) -> bool:
    return "foul" not in series["des"]


def _is_bip(series: Series) -> bool:
    return "homers" not in series["des"]


def get_statcast_data() -> DataFrame:
    if os.path.exists("data/sc.csv"):
        return pd.read_csv("data/sc.csv")

    raw_sc = statcast(start_dt="2025-01-01", end_dt="2025-12-31")
    sc_no_st = raw_sc.loc[raw_sc["game_type"] != "S"]
    sc_batted_balls = sc_no_st.loc[sc_no_st["type"] == "X"]
    sc_batted_balls.dropna(axis=0, subset="hc_x", inplace=True)
    sc_batted_balls["bip"] = sc_batted_balls.apply(_is_bip, axis=1)
    sc_min = sc_batted_balls.loc[sc_batted_balls.bip, ["des", "hc_x", "hc_y"]]
    sc_min["act_fair"] = sc_min.apply(_was_fair, axis=1)

    if not os.path.exists("data"):
        os.mkdir("data")
    sc_min.to_csv("data/sc.csv")

    return sc_min


def main():
    print("Hello from statcast-spray-angle-study!")


if __name__ == "__main__":
    main()
