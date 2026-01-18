from pandas import DataFrame
import matplotlib.pyplot as plt
import math

plt.rcParams["figure.figsize"] = 24, 10
plt.rcParams["legend.loc"] = "lower left"
plt.rcParams["figure.facecolor"] = "xkcd:grass green"


def plot_skewed_foul_line(
    origin: tuple[float, float],
    fair_df: DataFrame,
    foul_df: DataFrame,
    title: str,
    foul_angle: float,
):
    x_origin, y_origin = origin
    foul_y_change = x_origin / math.tan(foul_angle / 180 * math.pi)

    foul_y = [-y_origin + foul_y_change, -y_origin, -y_origin + foul_y_change]

    _plot_with_y_coords(origin, foul_y, fair_df, foul_df, title)


def plot_two_foul_lines(
    origin1: tuple[float, float],
    origin2: tuple[float, float],
    fair_df: DataFrame,
    foul_df: DataFrame,
    title: str,
):
    x_origin, y_origin = origin1
    foul_y_1 = [-y_origin + x_origin, -y_origin, -y_origin + x_origin]

    x_origin, y_origin = origin2
    foul_y_2 = [-y_origin + x_origin, -y_origin, -y_origin + x_origin]

    _plot_with_y_coords(origin1, foul_y_1, fair_df, foul_df, title, origin2, foul_y_2)


def plot_one_foul_line(
    origin: tuple[float, float], fair_df: DataFrame, foul_df: DataFrame, title: str
):
    x_origin, y_origin = origin
    foul_y = [-y_origin + x_origin, -y_origin, -y_origin + x_origin]

    _plot_with_y_coords(origin, foul_y, fair_df, foul_df, title)


def _plot_with_y_coords(
    origin: tuple[float, float],
    foul_y: list[float],
    fair_df: DataFrame,
    foul_df: DataFrame,
    title: str,
    origin2: tuple[float, float] = None,
    foul_y_2: list[float] = None,
):
    x_origin, _ = origin
    foul_x = [0, x_origin, 2 * x_origin]

    ax1 = plt.subplot(1, 2, 1)
    ax1.set_facecolor("xkcd:off white")
    plt.plot(foul_x, foul_y, c="k")

    if origin2 and foul_y_2:
        foul_x_2 = [0, origin2[0], 2 * origin2[0]]
        plt.plot(foul_x_2, foul_y_2, c="k")

    plt.scatter(
        fair_df["hc_x"], -fair_df["hc_y"], marker="o", c="0.5", label="Fair", alpha=0.5
    )
    plt.legend()
    plt.xticks([])
    plt.yticks([])
    ax2 = plt.subplot(1, 2, 2)
    ax2.set_facecolor("xkcd:off white")
    plt.plot(foul_x, foul_y, c="k")
    if origin2 and foul_y_2:
        plt.plot(foul_x_2, foul_y_2, c="k")

    plt.scatter(
        foul_df["hc_x"], -foul_df["hc_y"], marker="o", c="r", label="Foul", alpha=0.5
    )

    plt.legend()
    plt.xticks([])
    plt.yticks([])
    plt.suptitle(title, fontsize="xx-large")
    plt.subplots_adjust(top=0.95)

    plt.show()
