import numpy as np
from scipy import constants as sc
import matplotlib.pyplot as plt
import glob
import os


def make_plot(ts, e, e_err, plot_title, filename, xlabel, ylabel, extrap=None):
    fig, ax = plt.subplots()
    fig.set_size_inches(6.6, 2.8)
    ax.errorbar(ts, e, yerr=e_err, linestyle="", marker="d")
    if extrap is not None:
        min_ts, max_ts = ax.get_xlim()
        line_ts = np.linspace(min_ts, max_ts, 1000)
        m = extrap[1, 0]
        m_err = extrap[1, 1]
        b = extrap[0, 0]
        b_err = extrap[0, 1]
        y = (m * line_ts) + b
        y_plus_err = ((m + m_err) * line_ts) + (b + b_err)
        y_minus_err = ((m - m_err) * line_ts) + (b - b_err)

        ax.plot(
            line_ts,
            y,
            linestyle="--",
            label=r"$E=({}\pm{})\tau+({}\pm{})$".format(m, m_err, b, b_err),
            color="black",
        )
        ax.fill_between(line_ts, y, y_plus_err, alpha=0.5, color="dodgerblue")
        ax.fill_between(line_ts, y, y_minus_err, alpha=0.5, color="dodgerblue")
        ax.legend()

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(plot_title)  # , fontsize=8)

    plt.tight_layout()
    plt.savefig(filename, dpi=600)
    plt.close(fig)


for job in glob.glob("../data/*"):
    neutral_data = np.loadtxt(
        "{}/neutral_energies.txt".format(job), skiprows=1, delimiter=","
    )
    anion_data = np.loadtxt(
        "{}/anion_energies.txt".format(job), skiprows=1, delimiter=","
    )
    neutral_extrap_data = np.loadtxt("{}/neutral_extrapolation.txt".format(job))
    anion_extrap_data = np.loadtxt("{}/anion_extrapolation.txt".format(job))
    assert np.all(neutral_data[:, 0] == anion_data[:, 0])
    ts = neutral_data[:, 0]

    anion_energies = anion_data[:, 1]
    anion_err = anion_data[:, 2]
    neutral_energies = neutral_data[:, 1]
    neutral_err = neutral_data[:, 2]

    plot_title = job.split("/")[-1]
    plot_title = plot_title.replace("shiv", "/")
    plot_title = plot_title.replace("upa", "(")
    plot_title = plot_title.replace("Napu", "N)")
    plot_title = plot_title.replace("Aapu", "A)\n")
    plot_title = plot_title.replace("p0", ".0")
    trialwfn = plot_title.split("__")[0]
    basis = plot_title.split("__")[1]
    separation = plot_title.split("__")[2]

    trialwfn = trialwfn.replace("_", " ")
    basis = basis.replace("_", " ")
    separation = separation.replace("_", " ")

    if "//" in trialwfn:
        neutral_trialwfn = trialwfn.split("//")[0]
        anion_trialwfn = trialwfn.split("//")[1]
    else:
        neutral_trialwfn = trialwfn
        anion_trialwfn = trialwfn
    neutral_title = "{} {} {} neutral".format(neutral_trialwfn, basis, separation)
    anion_title = "{} {} {} anion".format(anion_trialwfn, basis, separation)
    combined_title = "{} {} {} EBE".format(trialwfn, basis, separation)

    filename = job.split("/")[-1]
    filename = os.path.splitext(filename)[0]

    x_label = r"$\tau$ / a.u."
    y_label = r"E / a.u."
    make_plot(
        ts,
        neutral_energies,
        neutral_err,
        neutral_title,
        "{}_01_neutral.png".format(filename),
        x_label,
        y_label,
        neutral_extrap_data,
    )
    make_plot(
        ts,
        anion_energies,
        anion_err,
        anion_title,
        "{}_02_anion.png".format(filename),
        x_label,
        y_label,
        anion_extrap_data,
    )

    x_label = r"$\tau$ / a.u."
    y_label = r"EBE / meV"
    ebe = neutral_energies - anion_energies
    ebe_err = np.sqrt(neutral_err ** 2 + anion_err ** 2)

    har_to_ev = sc.physical_constants["Hartree energy in eV"][0]
    ebe *= har_to_ev * 1000
    ebe_err *= har_to_ev * 1000
    make_plot(
        ts,
        ebe,
        ebe_err,
        combined_title,
        "{}_03_ebe.png".format(filename),
        x_label,
        y_label,
    )
