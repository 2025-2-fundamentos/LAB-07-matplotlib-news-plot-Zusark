"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


@dataclass(frozen=True)
class SeriesStyle:
    color: str
    zorder: int
    linewidth: int


STYLES: dict[str, SeriesStyle] = {
    "Television": SeriesStyle(color="dimgray", zorder=1, linewidth=2),
    "Newspaper": SeriesStyle(color="grey", zorder=1, linewidth=2),
    "Internet": SeriesStyle(color="tab:blue", zorder=2, linewidth=4),
    "Radio": SeriesStyle(color="Lightgrey", zorder=1, linewidth=2),
}


def _hide_axis_decoration(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.get_yaxis().set_visible(False)


def _annotate_endpoints(ax: plt.Axes, x0: int, y0: float, x1: int, y1: float, label: str, color: str, z: int) -> None:
    # Punto + texto en el primer año
    ax.scatter(x=x0, y=y0, color=color, zorder=z)
    ax.text(
        x0 - 0.2,
        y0,
        f"{label} {y0}%",
        ha="right",
        va="center",
        color=color,
    )

    # Punto + texto en el último año
    ax.scatter(x=x1, y=y1, color=color, zorder=z)
    ax.text(
        x1 + 0.2,
        y1,
        f"{y1}%",
        ha="left",
        va="center",
        color=color,
    )


def pregunta_01():
    """
    Siga las instrucciones del video https://youtu.be/qVdwpxG_JpE para
    generar el archivo `files/plots/news.png`.

    Un ejemplo de la grafica final esta ubicado en la raíz de
    este repo.

    El gráfico debe salvarse al archivo `files/plots/news.png`.
    """
    df = pd.read_csv("files/input/news.csv", index_col=0)

    fig, ax = plt.subplots()

    # Líneas
    for col in df.columns:
        style = STYLES.get(col, SeriesStyle(color="black", zorder=1, linewidth=2))
        ax.plot(
            df.index,
            df[col],
            label=col,
            color=style.color,
            zorder=style.zorder,
            linewidth=style.linewidth,
        )

    ax.set_title("How people get their news", fontsize=16)
    _hide_axis_decoration(ax)

    # Etiquetas de extremos
    first_year = int(df.index[0])
    last_year = int(df.index[-1])

    for col in df.columns:
        style = STYLES.get(col, SeriesStyle(color="black", zorder=1, linewidth=2))
        _annotate_endpoints(
            ax=ax,
            x0=first_year,
            y0=float(df.loc[first_year, col]),
            x1=last_year,
            y1=float(df.loc[last_year, col]),
            label=col,
            color=style.color,
            z=style.zorder,
        )

    ax.set_xticks(df.index)
    ax.set_xticklabels(df.index, ha="center")

    out_path = Path("files/plots/news.png")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path.as_posix())
    plt.show()
