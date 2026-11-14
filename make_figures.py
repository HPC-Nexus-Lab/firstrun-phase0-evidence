"""Draw every figure in figures/ from data/summary.json (aggregate numbers only).

    python make_figures.py

Needs matplotlib >= 3.7. One style for all figures: evidence badge, then the claim as title,
pass/fail thresholds drawn on the axes, source and licence in the footer.
"""
import json
import math
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

ROOT = Path(__file__).resolve().parent
S = json.loads((ROOT / "data" / "summary.json").read_text(encoding="utf-8"))
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)

# Validated reference palette, light mode. Held-out results are blue; development data is grey context.
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#8a8984"
GRID = "#e6e5e1"
HELDOUT = "#2a78d6"
HELDOUT_ALT = "#1baf7a"
DEV = "#9a9993"
ACCENT = "#eb6834"
GOOD = "#0ca30c"
BAD = "#d03b3b"
NONE = "#c9c8c2"
PASS_ZONE = "#e9f3e6"

BADGES = {
    "confirmed": ("PRE-REGISTERED · HELD-OUT TEST", HELDOUT),
    "development": ("DEVELOPMENT DATA · EXPLORATORY", INK2),
    "mixed_c1": ("DEVELOPMENT + HELD-OUT DATA", INK2),
    "mixed_c4": ("PRE-REGISTERED (FAILED) + EXPLORATORY", INK2),
    "pilot": ("EXPLORATORY PILOT · GATE RESULT IS POST HOC", ACCENT),
}
MIT = "Data: MIT Supercloud Dataset (Samsi et al., IEEE HPEC 2021), CC BY-NC-ND 4.0."

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10.5,
    "axes.edgecolor": GRID,
    "axes.labelcolor": INK2,
    "axes.titlecolor": INK,
    "xtick.color": INK2,
    "ytick.color": INK2,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": False,
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
})


def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return 100 * p, 100 * (c - h), 100 * (c + h)


def frame(title, subtitle, badge, footer, size=(11, 6.4)):
    """Badge on its own line, then title and subtitle; footer wrapped so it never clips."""
    fig = plt.figure(figsize=size)
    h = size[1]
    top = 1 - 0.22 / h
    text, colour = BADGES[badge]
    fig.text(0.035, top, text, fontsize=8.5, fontweight="bold", color=colour, va="top", ha="left",
             bbox=dict(boxstyle="round,pad=0.4", fc=SURFACE, ec=colour, lw=1.4))
    fig.text(0.035, top - 0.48 / h, title, fontsize=15, fontweight="bold", color=INK, va="top")
    fig.text(0.035, top - 0.88 / h, subtitle, fontsize=10.5, color=INK2, va="top")
    fig.text(0.035, 0.12 / h, textwrap.fill(footer, 160), fontsize=8, color=MUTED, va="bottom",
             linespacing=1.4)
    return fig


def tidy(ax, xgrid=True):
    if xgrid:
        ax.xaxis.grid(True, color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)


def verdict(ax, x, y, ok, text):
    colour, mark = (GOOD, "✓") if ok else (BAD, "✗")
    ax.text(x, y, f"{mark} {text}", color=colour, fontweight="bold", fontsize=10.5,
            transform=ax.transAxes, va="center")


def save(fig, name):
    fig.savefig(OUT / f"{name}.png", dpi=180)
    fig.savefig(OUT / f"{name}.svg")
    plt.close(fig)


# ---------------------------------------------------------------- C1
def fig_c1():
    c = S["C1_idle_waste"]
    fig = frame("Idle reserved GPUs are the most common waste, and it persists",
                "Share of batch-job GPUs idle (< 5% busy) for the whole run, and where GPU energy went",
                "mixed_c1",
                "Source: firstrun_realusers_confirm/results/scores.json; firstrun_realusers/results/REALUSERS.md, "
                "TIMEOUT_RESUBMITS.md. Batch jobs longer than 10 minutes. " + MIT)
    ax = fig.add_axes([0.09, 0.19, 0.34, 0.50])
    rows = c["idle_batch_gpus"]
    for i, (k, nm, col) in enumerate([("jobs_1_4", "Users' first 4 jobs\n(development)", DEV),
                                      ("jobs_5_8", "Users' next 4 jobs\n(held-out)", HELDOUT)]):
        p, lo, hi = wilson(rows[k]["idle"], rows[k]["gpus"])
        ax.bar(i, p, width=0.5, color=col, zorder=2)
        ax.errorbar(i, p, yerr=[[p - lo], [hi - p]], color=INK, lw=1.2, capsize=4, zorder=3)
        ax.text(i, hi + 2.5, f"{p:.0f}%", ha="center", fontsize=13, fontweight="bold", color=INK)
        ax.text(i, 3, f"{rows[k]['idle']} of {rows[k]['gpus']}\nGPUs", ha="center", fontsize=8.5, color="white")
    ax.set_xticks([0, 1], ["Users' first 4 jobs\n(development)", "Users' next 4 jobs\n(held-out)"], fontsize=9.5)
    ax.set_xlim(-0.6, 1.6)
    ax.set_ylim(0, 70)
    ax.set_ylabel("% of batch GPUs idle all run")
    ax.yaxis.grid(True, color=GRID, lw=0.8)
    tidy(ax, xgrid=False)
    ax.set_title("Idle batch GPUs (95% intervals)", fontsize=11, loc="left", color=INK)

    e = c["energy_jobs_1_4"]
    ax2 = fig.add_axes([0.58, 0.19, 0.38, 0.50])
    ax2.barh(1, e["idle_gpu_energy_pct"], height=0.42, color=HELDOUT, zorder=2)
    ax2.text(e["idle_gpu_energy_pct"] + 1.2, 1, f"{e['idle_gpu_energy_pct']:.1f}%", va="center",
             fontsize=12, fontweight="bold", color=INK)
    lo, hi = e["failed_run_energy_pct_timeout_excluded"], e["failed_run_energy_pct_all_timeout_counted"]
    ax2.plot([lo, hi], [0, 0], color=DEV, lw=7, solid_capstyle="round", zorder=2)
    ax2.plot([lo, hi], [0, 0], "o", ms=9, color=INK2, zorder=3)
    ax2.text(lo, -0.33, f"{lo:.1f}%\nTIMEOUT runs\nnot counted", ha="center", va="top", fontsize=8.5, color=INK2)
    ax2.text(hi, -0.33, f"{hi:.1f}%\nall TIMEOUT runs\ncounted as waste", ha="center", va="top", fontsize=8.5,
             color=INK2)
    ax2.set_yticks([0, 1], ["Failed runs\n(range)", "Idle GPUs"], fontsize=10)
    ax2.set_xlim(0, 62)
    ax2.set_ylim(-1.15, 1.6)
    ax2.set_xlabel("% of all GPU energy, users' first 4 jobs (1,125 jobs, 2,721 kWh)")
    tidy(ax2)
    ax2.set_title("Where GPU energy went", fontsize=11, loc="left", color=INK)
    ax2.text(0.99, 0.97, "The failed-run share depends on whether a\nTIMEOUT is waste or a long job "
             "to be continued", transform=ax2.transAxes, ha="right", va="top", fontsize=8.5, color=MUTED)
    save(fig, "C1_idle_waste")


# ---------------------------------------------------------------- C2
def fig_c2():
    c = S["C2_minute10_idle_check"]
    fig = frame("A minute-10 check finds 97% of GPUs that stay idle, with 11% false alarms",
                "Flag a GPU if it was < 5% busy over its first 10 minutes. Batch jobs longer than 10 min, "
                "users the model never saw.",
                "confirmed",
                "Source: firstrun_realusers_confirm/results/scores.json. Criteria committed in git (89bda07, "
                "2026-10-21) before the test jobs were selected. " + MIT)
    names = ["Users' first 4 jobs (development)", "Next 4 jobs (held-out, primary test)",
             "Next 4 jobs, without the 5 largest"]
    cols = [DEV, HELDOUT, HELDOUT_ALT]
    t = c["targets"]
    axes = []
    for j, (key, ci_key, xlim, lab, tgt, better) in enumerate([
            ("recall", "recall_ci", (85, 100.5), "Idle GPUs found (recall, %)", t["recall_min_pct"], "right"),
            ("false_alarm", "false_alarm_ci", (0, 20), "Flagged GPUs used later (false alarms, %)",
             t["false_alarm_max_pct"], "left")]):
        ax = fig.add_axes([0.31 + j * 0.355, 0.20, 0.29, 0.44])
        axes.append(ax)
        if better == "right":
            ax.axvspan(tgt, xlim[1], color=PASS_ZONE, zorder=0)
        else:
            ax.axvspan(xlim[0], tgt, color=PASS_ZONE, zorder=0)
        ax.axvline(tgt, color=INK2, lw=1.2, ls="--", zorder=1)
        off = 0.015 * (xlim[1] - xlim[0])
        ax.text(tgt - off, 2.7, f"target {'≥' if better == 'right' else '≤'} {tgt}%", ha="right", fontsize=8.5,
                color=INK2)
        for i, (r, col) in enumerate(zip(c["rows"], cols)):
            y = 2 - i
            ax.plot(r[ci_key], [y, y], color=col, lw=2.2, zorder=2)
            ax.plot(r[key], y, "o", ms=10, color=col, mec=SURFACE, mew=2, zorder=3)
            ax.text(r[key], y + 0.27, f"{r[key]:.1f}%", fontsize=10, fontweight="bold", color=INK, ha="center")
        ax.set_xlim(*xlim)
        ax.set_ylim(-0.6, 3.0)
        ax.set_yticks([2, 1, 0], names if j == 0 else ["", "", ""], fontsize=9.5)
        ax.set_xlabel(lab)
        tidy(ax)
    verdict(axes[0], 0.0, 1.1, True, "PASS on both criteria")
    axes[1].text(0.0, 1.1, "Green band = pass region; lines = 95% intervals",
                 transform=axes[1].transAxes, fontsize=8.5, color=MUTED, va="center")
    save(fig, "C2_minute10_idle_check")


# ---------------------------------------------------------------- C3
def fig_c3():
    c = S["C3_failure_warning"]
    fig = frame("At minute 10, telemetry warns which runs will fail: AUROC 0.78, unseen users",
                "Classifier on the first 10 minutes of telemetry plus the job request. Batch jobs that "
                "completed or failed.",
                "confirmed",
                "Source: firstrun_realusers_confirm/results/scores.json. Criterion AUROC ≥ 0.70 committed in git "
                "(89bda07) before selection. " + MIT)
    ax = fig.add_axes([0.36, 0.20, 0.58, 0.44])
    ax.axvspan(0.70, 1.0, color=PASS_ZONE, zorder=0)
    ax.axvline(0.70, color=INK2, lw=1.2, ls="--")
    ax.axvline(0.50, color=MUTED, lw=1, ls=":")
    ax.text(0.705, 4.05, "target ≥ 0.70", ha="left", fontsize=8.5, color=INK2)
    ax.text(0.505, 4.05, "coin flip", ha="left", fontsize=8.5, color=MUTED)
    colour = {"development": DEV, "primary": HELDOUT, "secondary": HELDOUT_ALT}
    labels = []
    for i, r in enumerate(c["rows"]):
        y = 3 - i
        col = colour[r["kind"]]
        ax.plot(r["ci"], [y, y], color=col, lw=2.2)
        ax.plot(r["auroc"], y, "o", ms=10, color=col, mec=SURFACE, mew=2, zorder=3)
        ax.text(r["auroc"], y + 0.3, f"{r['auroc']:.2f}", fontsize=10.5, fontweight="bold", color=INK,
                ha="center")
        labels.append(f"{r['label']}\n{r['failing']} failing / {r['completing']} completing")
    ax.set_yticks([3, 2, 1, 0], labels, fontsize=9)
    ax.set_xlim(0.45, 1.0)
    ax.set_ylim(-0.6, 4.4)
    ax.set_xlabel("AUROC (0.5 = no better than chance, 1.0 = perfect); lines = 95% bootstrap intervals")
    tidy(ax)
    verdict(ax, 0.0, 1.1, True, "PASS")
    ax.text(0.13, 1.1, f"At 10% false alarms the warning flags {c['recall_at_10pct_false_alarms_pct']}% of "
            "failing batch runs (held-out).", transform=ax.transAxes, fontsize=9, color=INK2, va="center")
    save(fig, "C3_failure_warning")


# ---------------------------------------------------------------- C4
def fig_c4():
    c = S["C4_sizing"]
    fig = frame("Sizing jobs in advance does not pay: time limits and GPU counts",
                "Left: recommended time limits against users' own requests. Right: choosing the GPU count.",
                "mixed_c4",
                "Source: firstrun_realusers/results/REALUSERS_VERDICT.md (R10) and REALUSERS_POSTHOC.md (296 completed "
                "jobs, runtime not declared); firstrun_phase0/results/gpu_count/GPU_COUNT.md. " + MIT)
    tl = c["time_limits"]
    ax = fig.add_axes([0.08, 0.20, 0.39, 0.43])
    base = tl["points"][0]["median_slack_h"]
    ax.add_patch(Rectangle((-5, 0), 15, base * 0.5, color=PASS_ZONE, zorder=0))
    ax.text(-4.4, base * 0.5 - 1.2, "target: ≥ 50% less slack,\n≤ 10% more energy", fontsize=8.5,
            color=INK2, va="top")
    for i, p in enumerate(tl["points"]):
        user = i == 0
        ax.plot(p["energy_overhead_pct"], p["median_slack_h"], "s" if user else "o", ms=10,
                color=INK2 if user else HELDOUT, mec=SURFACE, mew=2, zorder=3)
        dx, ha = (0.8, "left")
        if p["energy_overhead_pct"] > 10:
            dx, ha = (-0.8, "right")
        ax.text(p["energy_overhead_pct"] + dx, p["median_slack_h"], f"{p['label']}\n{p['median_slack_h']:.0f} h",
                fontsize=8.5, color=INK, va="center", ha=ha)
    ax.set_xlim(-5, 16)
    ax.set_ylim(0, 66)
    ax.set_xlabel("Extra GPU energy from kills and retries (%)")
    ax.set_ylabel("Median reserved-but-unused time (h)")
    ax.yaxis.grid(True, color=GRID, lw=0.8)
    tidy(ax)
    ax.set_title("Time limits: no policy reaches the target", fontsize=11, loc="left", color=INK, pad=24)
    verdict(ax, 0.0, 1.05, False, "FAIL (pre-registered R10)")
    ax.text(1.0, 0.04, f"{tl['users_unlimited_pct']:.0f}% of jobs asked for\nunlimited time (not plotted)",
            transform=ax.transAxes, fontsize=8, color=MUTED, va="bottom", ha="right")

    g = c["gpu_count"]
    ax2 = fig.add_axes([0.66, 0.20, 0.31, 0.43])
    rows = g["rows"]
    for i, r in enumerate(rows):
        y = len(rows) - 1 - i
        ax2.barh(y, r["mean_regret_pct"], height=0.5, color=HELDOUT if i == 0 else DEV, zorder=2)
        ax2.plot([r["worst_model_regret_pct"]], [y], "|", ms=16, mew=2, color=INK, zorder=3)
        note = f"{r['mean_regret_pct']:.2f}% mean, {r['worst_model_regret_pct']:.1f}% worst"
        if r["probe_cost_pct"]:
            note += f"\n+ probe costs {r['probe_cost_pct']:.0f}% of a job"
        ax2.text(r["worst_model_regret_pct"] + 0.3, y, note, va="center", fontsize=8.5, color=INK2)
    ax2.set_yticks(range(len(rows))[::-1], [r["label"] for r in rows], fontsize=9.5)
    ax2.set_xlim(0, 15)
    ax2.set_xlabel("Extra energy vs the best GPU count (%)\nbar = mean over 9 models, tick = worst model")
    tidy(ax2)
    ax2.set_title("GPU count: always 1 GPU is near-best", fontsize=11, loc="left", color=INK, pad=24)
    ax2.text(0.0, 1.05, "Exploratory · V100 vision models · GPU energy only", transform=ax2.transAxes,
             fontsize=8.5, color=ACCENT, fontweight="bold", va="center")
    save(fig, "C4_sizing_does_not_pay")


# ---------------------------------------------------------------- C5
def fig_c5():
    c = S["C5_diagnosis_pilot"]
    fig = frame("Diagnosis pilot: can a local language model name the cause of a fault?",
                "13 jobs (10 injected faults, 3 healthy). Each cell: was the named cause right? "
                "Shaded rows look the same in telemetry.",
                "pilot", "Source: firstrun_phase0/results/diagnosis_pilot/PILOT.md. Own fault-injection jobs on one "
                         "GTX 1660 SUPER, first 3 minutes of telemetry; 7 of 13 reproduce the script's GPU and CPU "
                         "load with real CUDA kernels rather than running it.",
                size=(11, 8.6))
    cols = [("rules", "Telemetry\nrules only"), ("qwen3_8b", "qwen3:8b\npre-registered"),
            ("coder30b", "qwen3-coder:30b\nnot judged"), ("coder30b_gated", "coder:30b + gate\npost hoc")]
    cases = c["cases"]
    ax = fig.add_axes([0.035, 0.08, 0.93, 0.74])
    ax.set_xlim(0, 10)
    ax.set_ylim(len(cases) + 3.6, -0.2)
    ax.axis("off")
    x0, w = 4.3, 1.42
    for j, (_, name) in enumerate(cols):
        ax.text(x0 + j * w + w / 2, 0.55, name, ha="center", va="center", fontsize=9, color=INK, fontweight="bold")
    ax.text(0.05, 0.55, "Injected cause", fontsize=9, fontweight="bold", color=INK, va="center")
    ax.text(2.55, 0.55, "Telemetry looks like", fontsize=9, fontweight="bold", color=INK, va="center")
    style = {"right": (GOOD, "✓"), "wrong": (BAD, "✗"), "none": (NONE, "–")}
    for i, r in enumerate(cases):
        y = i + 1.6
        if r["class"] == "GPU unused, CPU busy":
            ax.add_patch(Rectangle((0, y - 0.48), 10, 0.96, color="#f1f0ec", zorder=0))
        ax.text(0.05, y, r["cause"], fontsize=9, color=INK, va="center")
        ax.text(2.55, y, r["class"], fontsize=8.5, color=INK2, va="center")
        for j, (key, _) in enumerate(cols):
            col, mark = style[r[key]]
            ax.add_patch(FancyBboxPatch((x0 + j * w + 0.12, y - 0.36), w - 0.24, 0.72,
                                        boxstyle="round,pad=0,rounding_size=0.12", fc=col, ec=SURFACE, lw=2))
            ax.text(x0 + j * w + w / 2, y, mark, ha="center", va="center", color="white", fontsize=12,
                    fontweight="bold")
    t = c["totals"]
    yb = len(cases) + 1.3
    totals = [f"{t['rules']['overall']} right", f"{t['qwen3_8b']['faulty']} faults\nD1 failed",
              f"{t['coder30b']['faulty']} faults,\n2 healthy flagged",
              f"{t['coder30b_gated_post_hoc']['overall']} right\nrule chosen after the\nrun; tested in O4"]
    for j, txt in enumerate(totals):
        ax.text(x0 + j * w + w / 2, yb, txt, ha="center", va="top", fontsize=8.5, color=INK, fontweight="bold")
    ax.text(0.05, yb, "✓ right   ✗ wrong   – no usable answer", fontsize=9, color=INK2, va="top")
    ax.text(0.05, yb + 1.45, "Gate: the model may only choose causes consistent with the telemetry state. It was "
            "devised after the run and needs its own pre-registered test.\nThe pre-registered model was qwen3:8b; "
            "qwen3-coder:30b was listed in advance as a second model, reported but not judged.",
            fontsize=8.5, color=INK2, va="top", linespacing=1.5)
    save(fig, "C5_diagnosis_pilot")


# ---------------------------------------------------------------- C6
def fig_c6():
    c = S["C6_measurement"]
    fig = frame("Measuring a job's cycle: trust it only when GPU activity and power agree",
                "Left: how often 90% runtime bounds contained the true runtime. Right: power drawn by a GPU "
                "that holds a job but does no work.",
                "development",
                "Source: firstrun_phase0/analysis/V03_DEVELOPMENT.md (benchmark jobs, MIT Supercloud); "
                "firstrun_phase0/results/hetero/HETERO_PROBE.md (Elsayed et al. 2026, CC BY-NC-ND 4.0); MIT "
                "Supercloud real users. H100/B200: floor power, range over two workloads. V100: idle real-user "
                "GPUs, energy / time.")
    pa = c["period_agreement"]
    ax = fig.add_axes([0.08, 0.20, 0.46, 0.44])
    groups = ["Activity and power periods agree", "Periods disagree by > 10%", "Only one period found"]
    gcols = [HELDOUT, ACCENT, DEV]
    for k, cut in enumerate([10, 20]):
        for g, (gname, gcol) in enumerate(zip(groups, gcols)):
            r = next(x for x in pa["rows"] if x["cut_min"] == cut and x["group"] == gname)
            x = k * 4 + g
            ax.bar(x, r["coverage_pct"], width=0.8, color=gcol, zorder=2)
            ax.text(x, r["coverage_pct"] - 3, f"{r['coverage_pct']}%", ha="center", va="top", fontsize=10.5,
                    fontweight="bold", color="white", zorder=4)
            ax.text(x, 4, f"n={r['jobs']}", ha="center", fontsize=8, color="white")
    ax.axhline(pa["nominal_coverage_pct"], color=INK2, ls="--", lw=1.2)
    ax.text(7.45, pa["nominal_coverage_pct"] + 2, "nominal 90%", ha="right", fontsize=8.5, color=INK2)
    ax.set_xticks([1, 5], ["10 minutes of watching", "20 minutes of watching"])
    ax.set_xlim(-0.6, 7.6)
    ax.set_ylim(0, 108)
    ax.set_ylabel("Bounds containing\nthe true runtime (%)")
    ax.yaxis.grid(True, color=GRID, lw=0.8)
    tidy(ax, xgrid=False)
    handles = [Rectangle((0, 0), 1, 1, color=col) for col in gcols]
    ax.legend(handles, groups, loc="lower left", bbox_to_anchor=(0.0, 1.02), ncol=3, frameon=False,
              fontsize=8.5, handlelength=1.2, columnspacing=1.0)
    ax.set_title("Strong-rhythm benchmark jobs (v0.2)", fontsize=11, loc="left", color=INK, pad=26)

    ip = c["idle_power_w_per_gpu"]
    ax2 = fig.add_axes([0.67, 0.20, 0.29, 0.44])
    for i, r in enumerate(ip["rows"]):
        w = r["watts"]
        mid = sum(w) / len(w)
        ax2.bar(i, mid, width=0.6, color=HELDOUT if r["gpu"] == "B200" else DEV, zorder=2)
        if len(w) > 1:
            ax2.plot([i, i], [min(w), max(w)], color=INK, lw=1.4, zorder=3)
            txt = f"{min(w):.0f}–{max(w):.0f} W"
        else:
            txt = f"{w[0]:.0f} W"
        ax2.text(i, max(w) + 7, txt, ha="center", fontsize=10, fontweight="bold", color=INK)
    ax2.set_xticks(range(3), [r["gpu"] for r in ip["rows"]])
    ax2.set_ylim(0, 240)
    ax2.set_ylabel("Watts per GPU,\nholding a job but idle")
    ax2.yaxis.grid(True, color=GRID, lw=0.8)
    tidy(ax2, xgrid=False)
    ax2.set_title("Idle power by GPU type", fontsize=11, loc="left", color=INK, pad=26)
    save(fig, "C6_measurement")


if __name__ == "__main__":
    for f in (fig_c1, fig_c2, fig_c3, fig_c4, fig_c5, fig_c6):
        f()
    print("figures written to", OUT)
