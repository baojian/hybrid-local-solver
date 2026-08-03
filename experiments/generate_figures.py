"""Generate reproducible figures for the active manuscript."""

from __future__ import annotations

import argparse
import json
import math
from itertools import product
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from experiments.check_appr_lower_bound import run_checks
from src.baselines.appr import APPR_ORDERINGS

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_PATH = REPOSITORY_ROOT / "results" / "appr_star_work_bounds.json"
DEFAULT_FIGURE_STEM = REPOSITORY_ROOT / "manuscript" / "figures" / "appr_star_work_bounds"
DEFAULT_SCALED_FIGURE_STEM = REPOSITORY_ROOT / "manuscript" / "figures" / "appr_star_scaled_work"

ALPHAS = (1.0 / 4.0, 1.0 / 8.0, 1.0 / 16.0, 1.0 / 32.0)
ALPHA_LABELS = (r"1/4", r"1/8", r"1/16", r"1/32")
EPS_VALUES = tuple(2.0**-power for power in range(4, 11))
RANDOM_SEED = 17

ORDERING_STYLE = {
    "fifo": {"color": "#0072B2", "marker": "o", "label": "FIFO"},
    "lifo": {"color": "#D55E00", "marker": "s", "label": "LIFO"},
    "max-ratio": {"color": "#009E73", "marker": "^", "label": "Max ratio"},
    "random": {"color": "#CC79A7", "marker": "D", "label": "Random"},
}


def appr_star_records() -> list[dict[str, object]]:
    """Run the fixed parameter grid and retain the proved hard-star rows."""
    records = run_checks(
        list(ALPHAS),
        list(EPS_VALUES),
        list(APPR_ORDERINGS),
        random_seed=RANDOM_SEED,
        spider_length=3,
        graph_kinds=("star",),
    )
    return records


def write_experiment_data(records: list[dict[str, object]], output_path: Path) -> None:
    """Write the plotted records and fixed plotting grid with full provenance."""
    index_star_records(records)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    code_versions = {str(record["code_version"]) for record in records}
    if len(code_versions) != 1:
        raise ValueError(f"expected one code version, got {sorted(code_versions)}")
    payload = {
        "experiment": "APPR actual work versus proved star lower and upper bounds",
        "work_unit": "degree-weighted adjacency-list work W = sum_t d[u_t]",
        "code_version": code_versions.pop(),
        "alphas": ALPHAS,
        "eps_appr_values": EPS_VALUES,
        "orderings": APPR_ORDERINGS,
        "random_seed": RANDOM_SEED,
        "records": records,
    }
    output_path.write_text(json.dumps(payload, indent=2) + "\n")


def index_star_records(
    records: list[dict[str, object]],
) -> dict[tuple[float, float, str], dict[str, object]]:
    """Validate and index the complete plotted parameter grid."""
    expected = set(product(ALPHAS, EPS_VALUES, APPR_ORDERINGS))
    indexed: dict[tuple[float, float, str], dict[str, object]] = {}

    for record in records:
        if record.get("graph_kind") != "star":
            raise ValueError(
                f"figure data must contain only star rows, got {record.get('graph_kind')}"
            )
        alpha = _canonical_float(record.get("alpha"), ALPHAS, "alpha")
        eps_appr = _canonical_float(record.get("eps_appr"), EPS_VALUES, "eps_appr")
        ordering = str(record.get("ordering"))
        if ordering not in APPR_ORDERINGS:
            raise ValueError(f"unexpected ordering in figure data: {ordering}")

        key = (alpha, eps_appr, ordering)
        if key in indexed:
            raise ValueError(f"duplicate figure record for {key}")
        if record.get("lower_bound_applies") is not True:
            raise ValueError(f"star lower bound must apply to figure record {key}")

        work = float(record["work"])
        scaled_work = float(record["scaled_work"])
        if not math.isclose(scaled_work, alpha * eps_appr * work, rel_tol=1e-12):
            raise ValueError(f"inconsistent scaled work for figure record {key}")
        indexed[key] = record

    missing = expected.difference(indexed)
    if missing:
        preview = sorted(missing)[:3]
        raise ValueError(f"missing {len(missing)} figure records; first missing keys: {preview}")
    return indexed


def _canonical_float(value: object, candidates: tuple[float, ...], name: str) -> float:
    numeric = float(value)
    matches = [
        candidate
        for candidate in candidates
        if math.isclose(numeric, candidate, rel_tol=1e-12, abs_tol=1e-15)
    ]
    if len(matches) != 1:
        raise ValueError(f"unexpected {name} in figure data: {value}")
    return matches[0]


def plot_appr_star_bounds(records: list[dict[str, object]], output_stem: Path) -> None:
    """Plot actual star work against the two proved complexity bounds."""
    _plot_appr_star_metric(
        records,
        output_stem,
        metric="work",
        y_label=r"Degree-weighted work $W$",
        scaled=False,
    )


def plot_appr_star_scaled_work(records: list[dict[str, object]], output_stem: Path) -> None:
    """Plot normalized work to expose the constant-order scaling directly."""
    _plot_appr_star_metric(
        records,
        output_stem,
        metric="scaled_work",
        y_label=r"Scaled work $\alpha\epsilon_{\mathrm{appr}}W$",
        scaled=True,
    )


def _plot_appr_star_metric(
    records: list[dict[str, object]],
    output_stem: Path,
    *,
    metric: str,
    y_label: str,
    scaled: bool,
) -> None:
    indexed = index_star_records(records)
    plt.rcParams.update(
        {
            "font.size": 8.5,
            "axes.labelsize": 8,
            "axes.titlesize": 9,
            "legend.fontsize": 5.5,
            "xtick.labelsize": 7,
            "ytick.labelsize": 7,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )
    figure, axes = plt.subplots(
        1,
        4,
        figsize=(7.25, 2.25),
        sharex=True,
        sharey=True,
        layout="constrained",
    )

    inverse_eps = [1.0 / eps_appr for eps_appr in EPS_VALUES]
    for axis, alpha, alpha_label in zip(axes, ALPHAS, ALPHA_LABELS, strict=True):
        if scaled:
            lower_bound = [3.0 / 128.0] * len(inverse_eps)
            upper_bound = [1.0] * len(inverse_eps)
        else:
            lower_bound = [3.0 * value / (128.0 * alpha) for value in inverse_eps]
            upper_bound = [value / alpha for value in inverse_eps]
        axis.fill_between(
            inverse_eps,
            lower_bound,
            upper_bound,
            color="#D9D9D9",
            alpha=0.42,
            linewidth=0,
            zorder=0,
        )
        axis.plot(
            inverse_eps,
            lower_bound,
            color="#4D4D4D",
            linestyle="--",
            linewidth=1.25,
            zorder=1,
        )
        axis.plot(
            inverse_eps,
            upper_bound,
            color="#111111",
            linestyle=":",
            linewidth=1.4,
            zorder=1,
        )

        for ordering in APPR_ORDERINGS:
            style = ORDERING_STYLE[ordering]
            selected = [indexed[(alpha, eps_appr, ordering)] for eps_appr in EPS_VALUES]
            axis.plot(
                [1.0 / float(record["eps_appr"]) for record in selected],
                [float(record[metric]) for record in selected],
                color=style["color"],
                marker=style["marker"],
                markersize=3.2,
                markerfacecolor="white",
                markeredgewidth=0.75,
                linewidth=1.05,
                zorder=2,
            )

        axis.set_title(rf"$\alpha={alpha_label}$")
        axis.set_xscale("log", base=2)
        axis.set_yscale("log", base=10)
        axis.set_xlim(min(inverse_eps), max(inverse_eps))
        if scaled:
            axis.set_ylim(2.0e-2, 1.1)
        axis.set_xticks(
            [2.0**power for power in (4, 6, 8, 10)],
            [rf"$2^{{{power}}}$" for power in (4, 6, 8, 10)],
        )
        axis.grid(which="major", color="#E7E7E7", linewidth=0.65)
        axis.set_axisbelow(True)

    axes[0].set_ylabel(y_label)
    figure.text(
        0.5,
        -0.045,
        r"Inverse residual tolerance $1/\epsilon_{\mathrm{appr}}$",
        ha="center",
        va="top",
        fontsize=8,
    )

    handles = [
        Line2D(
            [0],
            [0],
            color=ORDERING_STYLE[ordering]["color"],
            marker=ORDERING_STYLE[ordering]["marker"],
            markerfacecolor="white",
            markersize=4.5,
            linewidth=1.35,
            label=ORDERING_STYLE[ordering]["label"],
        )
        for ordering in APPR_ORDERINGS
    ]
    handles.extend(
        [
            Line2D(
                [0],
                [0],
                color="#4D4D4D",
                linestyle="--",
                linewidth=1.25,
                label="Lower bound",
            ),
            Line2D(
                [0],
                [0],
                color="#111111",
                linestyle=":",
                linewidth=1.4,
                label="Upper bound",
            ),
        ]
    )
    axes[0].legend(
        handles=handles,
        loc="upper left",
        ncol=2,
        frameon=True,
        framealpha=0.92,
        facecolor="white",
        edgecolor="#BDBDBD",
        borderpad=0.35,
        labelspacing=0.25,
        columnspacing=0.6,
        handlelength=1.6,
    )
    figure.get_layout_engine().set(w_pad=0.025, h_pad=0.02, wspace=0.035)

    output_stem.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(
        output_stem.with_suffix(".pdf"),
        bbox_inches="tight",
        metadata={
            "Creator": "experiments.generate_figures",
            "CreationDate": None,
            "ModDate": None,
        },
    )
    figure.savefig(
        output_stem.with_suffix(".png"),
        dpi=240,
        bbox_inches="tight",
        metadata={"Software": "experiments.generate_figures"},
    )
    plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-output", type=Path, default=DEFAULT_DATA_PATH)
    parser.add_argument("--figure-stem", type=Path, default=DEFAULT_FIGURE_STEM)
    parser.add_argument(
        "--scaled-figure-stem",
        type=Path,
        default=DEFAULT_SCALED_FIGURE_STEM,
    )
    args = parser.parse_args()

    records = appr_star_records()
    write_experiment_data(records, args.data_output)
    plot_appr_star_bounds(records, args.figure_stem)
    plot_appr_star_scaled_work(records, args.scaled_figure_stem)

    lower_verified = sum(bool(record["lower_bound_verified"]) for record in records)
    upper_verified = sum(bool(record["upper_bound_verified"]) for record in records)
    print(
        f"generated {args.figure_stem.with_suffix('.pdf')} and "
        f"{args.scaled_figure_stem.with_suffix('.pdf')} (plus PNGs) from "
        f"{len(records)} star runs; lower {lower_verified}/{len(records)}, "
        f"upper {upper_verified}/{len(records)}"
    )


if __name__ == "__main__":
    main()
