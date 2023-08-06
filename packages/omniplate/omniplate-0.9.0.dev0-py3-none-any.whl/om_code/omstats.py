# functions to calculate the statistics from the Gaussian process
# fit to the data
# and getfitnesspenalty
import om_code.genutils as gu
import pandas as pd
import numpy as np
from scipy.signal import find_peaks
from scipy import integrate
from scipy.interpolate import interp1d
import matplotlib.pylab as plt
import om_code.errors as errors


def statserr(d):
    """
    Errors in statistics calculated from samples from a
    Gaussian process are half the interquartile range (consistent with
    fitderiv).
    """
    return gu.findiqr(d) / 2

###


def cleansc(inst):
    """
    Ensure that NaNs do not change numeric variables from being floats.
    """
    floatvars = [
        "log2 OD ratio",
        "log2 OD ratio err",
        "local max gr",
        "local max gr err",
        "time of local max gr",
        "time of local max gr err",
        "area under gr vs OD",
        "area under gr vs OD err",
        "normalized area under gr vs OD",
        "normalized area under gr vs OD err",
        "area under OD",
        "area under OD err",
        "normalized area under OD",
        "normalized area under OD err",
        "OD logmaxlike",
        "max gr",
        "max gr err",
        "time of max gr",
        "time of max gr err",
        "doubling time",
        "doubling time err",
        "max OD",
        "max OD err",
        "lag time",
        "lag time err",
    ]
    for var in floatvars:
        if var in inst.sc.columns:
            inst.sc[var] = inst.sc[var].astype(float)

###


def findsummarystats(
    dtype,
    nosamples,
    f,
    t,
    e,
    c,
    s,
    findareas,
    figs,
    plotlocalmax,
    axgr,
    showpeakproperties,
    **kwargs,
):
    """
    Finds summary statistics from GP fit to time series of dtype
    """
    warning = None
    if dtype != "OD":
        # not OD
        outdf = pd.DataFrame(
            {
                "experiment": e,
                "condition": c,
                "strain": s,
                "time": t,
                "f" + dtype: f.f,
                "f" + dtype + " err": np.sqrt(f.fvar),
                "d/dt " + dtype: f.df,
                "d/dt " + dtype + " err": np.sqrt(f.dfvar),
                "d2/dt2 " + dtype: f.ddf,
                "d2/dt2 " + dtype + " err": np.sqrt(f.ddfvar),
            }
        )
        statsdict = {"experiment": e, "condition": c, "strain": s}
    else:
        # OD
        outdf = pd.DataFrame(
            {
                "experiment": e,
                "condition": c,
                "strain": s,
                "time": t,
                "flogOD": f.f,
                "flogOD err": np.sqrt(f.fvar),
                "gr": f.df,
                "gr err": np.sqrt(f.dfvar),
                "d/dt gr": f.ddf,
                "d/dt gr err": np.sqrt(f.ddfvar),
            }
        )
        # check growth rate has been sensibly defined
        if (
            np.max(np.abs(f.df)) < 1.0e-20
            and np.max(np.abs(np.diff(f.dfvar))) < 1.0e-20
        ):
            warning = (
                "\nWarning: finding gr may have failed for "
                + e
                + ": "
                + s
                + " in "
                + c
            )
        # find summary statistics
        fs, gs, hs = f.fitderivsample(nosamples)
        # log2 OD ratio
        dr = np.log2(np.exp(fs[-1, :] - fs[0, :]))
        # find local maximum growth rate
        da, dt = findlocalmaxgr(
            f, gs, axgr, figs, plotlocalmax, showpeakproperties, **kwargs
        )
        # find area under gr vs OD and area under OD
        if findareas:
            agod, angod, atod, antod = findareasunderOD(t, fs, gs)
        else:
            agod, angod, atod, antod = np.nan, np.nan, np.nan, np.nan
        # store results
        statsdict = {
            "experiment": e,
            "condition": c,
            "strain": s,
            "log2 OD ratio": np.median(dr),
            "log2 OD ratio err": statserr(dr),
            "local max gr": np.median(da),
            "local max gr err": statserr(da),
            "time of local max gr": np.median(dt),
            "time of local max gr err": statserr(dt),
            "area under gr vs OD": np.median(agod),
            "area under gr vs OD err": statserr(agod),
            "normalized area under gr vs OD": np.median(angod),
            "normalized area under gr vs OD err": statserr(angod),
            "area under OD": np.median(atod),
            "area under OD err": statserr(atod),
            "normalized area under OD": np.median(antod),
            "normalized area under OD err": statserr(antod),
        }
    return outdf, statsdict, warning

###


def findlocalmaxgr(
    f, gs, axgr, figs, plotlocalmax, showpeakproperties, **kwargs
):
    """
    Check if growth rate has a local maxima.
    If so, find the local maximum with the highest growth rate using samples
    of gs of growth rates.
    The keyword variables kwargs are passed to scipy's find_peaks.
    """
    # find peaks in mean gr
    lpksmn, lpksmndict = find_peaks(f.df, **kwargs)
    if np.any(lpksmn):
        if showpeakproperties:
            # display properties of peaks
            print("Peak properties\n---")
            for prop in lpksmndict:
                print("{:15s}".format(prop), lpksmndict[prop])
        # da: samples of local max growth rate
        # dt: samples of time of local max growth rate
        da, dt = [], []
        # find peaks of sampled growth rates
        for gsample in np.transpose(gs):
            tpks = find_peaks(gsample, **kwargs)[0]
            if np.any(tpks):
                da.append(np.max(gsample[tpks]))
                dt.append(f.pt[tpks[np.argmax(gsample[tpks])]])
        if figs and plotlocalmax:
            # plot local max gr as a point
            axgr.plot(
                np.median(dt),
                np.median(da),
                "o",
                color="yellow",
                markeredgecolor="k",
            )
        return da, dt
    else:
        # mean gr has no peaks
        return np.nan, np.nan

###


def findareasunderOD(t, fs, gs):
    """
    Given samples of log OD and of growth rate, find the area
    under gr vs OD and the area under OD vs time.
    """
    # agod: samples of area under gr vs OD
    # angod: samples of normalised area under gr vs OD
    # atod: samples of area under OD vs time
    # antod: samples of normalised area under OD vs time
    agod, angod, atod, antod = [], [], [], []
    for fsample, gsample in zip(np.transpose(fs), np.transpose(gs)):
        sod = np.exp(fsample)
        # area under gr vs OD: integrand has OD as x and gr as y

        def integrand(x):
            return interp1d(sod, gsample)(x)

        iresult = integrate.quad(
            integrand, np.min(sod), np.max(sod), limit=100, full_output=1
        )[0]
        agod.append(iresult)
        angod.append(iresult / (np.max(sod) - np.min(sod)))
        # area under OD vs t: integrand has t as x and OD as y

        def integrand(x):
            return interp1d(t, sod)(x)

        iresult = integrate.quad(
            integrand, np.min(t), np.max(t), limit=100, full_output=1
        )[0]
        atod.append(iresult)
        antod.append(iresult / (np.max(t) - np.min(t)))
    return agod, angod, atod, antod


###


def getfitnesspenalty(
    inst, ref, com, y="gr", abs=False, figs=True, nosamples=100, norm=False
):
    """
    Calculates - as a measure of fitness - the area between typically
    two growth rate versus OD curves, normalized by the length along the
    OD-axis where they overlap.

    Parameters
    -----------
    ref: list of strings
        For only a single experiment, a list of two strings. The first string
        specifies the condition and the second specifies the strain to be used
        for the reference to which fitness is to be calculated.
        With multiple experiments, a list of three strings. The first string
        specifies the experiment, the second specifies the condition, and the
        third specifies the strain.
    com: list of strings
        For only a single experiment, a list of two strings. The first string
        specifies the condition and the second specifies the strain to be
        compared with the reference.
        With multiple experiments, a list of three strings. The first string
        specifies the experiment, the second specifies the condition, and the
        third specifies the strain.
    y: string, optional
        The variable to be compared.
    figs: boolean, optional
        If True, a plot of the area between the two growth rate versus OD
        curves is shown.
    nosamples: integer
        The number bootstraps used to estimate the error.
    norm: boolean
        If True, returns the mean and variance of the area under the reference
        strain for normalisation.

    Returns
    -------
    fp: float
        The area between the two curves.
    err: float
        An estimate of the error in the calculated error, found by
        bootstrapping.
    reffp: float, optional
        The area beneath the reference strain.
    referr: float, optional
        An estimate of the erroe in the calculated area for the reference
        strain.

    Example
    -------
    >>> p.getfitnesspenalty(['1% raf 0.0µg/ml cyclohex', 'WT'],
    ...                     ['1% raf 0.5µg/ml cyclohex', 'WT'])
    """
    if len(inst.allexperiments) == 1:
        ref.insert(0, inst.allexperiments[0])
        com.insert(0, inst.allexperiments[0])
    # get and sample from Gaussian processes
    if nosamples and y == "gr":
        # estimate errors
        try:
            # sample from Gaussian process
            f0s, g0s, h0s = inst.progress["getstatsGP"][ref[0]][ref[1]][
                ref[2]
            ].fitderivsample(nosamples)
            f1s, g1s, h1s = inst.progress["getstatsGP"][com[0]][com[1]][
                com[2]
            ].fitderivsample(nosamples)
            xsref, ysref = np.exp(f0s), g0s
            xscom, yscom = np.exp(f1s), g1s
        except KeyError:
            raise errors.GetFitnessPenalty(
                "getstats('OD') needs to be run for these strains to "
                "estimate errors or else set nosamples= 0"
            )
    else:
        # no estimates of errors
        if nosamples:
            print(
                "Cannot estimate errors - require y= 'gr' and a recently "
                "run getstats"
            )
        xsref = inst.s.query(
            "experiment == @ref[0] and condition == @ref[1] and "
            "strain == @ref[2]"
        )["OD mean"][:, None]
        ysref = inst.s.query(
            "experiment == @ref[0] and condition == @ref[1] and "
            "strain == @ref[2]"
        )[y].to_numpy()[:, None]
        xscom = inst.s.query(
            "experiment == @com[0] and condition == @com[1] and "
            "strain == @com[2]"
        )["OD mean"].to_numpy()[:, None]
        yscom = inst.s.query(
            "experiment == @com[0] and condition == @com[1] and "
            "strain == @com[2]"
        )[y].to_numpy()[:, None]
        if xsref.size == 0 or ysref.size == 0:
            print(ref[0] + ": Data missing for", ref[2], "in", ref[1])
            return np.nan, np.nan
        elif xscom.size == 0 or yscom.size == 0:
            print(com[0] + ": Data missing for", com[2], "in", com[1])
            return np.nan, np.nan
    fps = np.zeros(xsref.shape[1])
    nrm = np.zeros(xsref.shape[1])
    samples = zip(
        np.transpose(xsref),
        np.transpose(ysref),
        np.transpose(xscom),
        np.transpose(yscom),
    )
    # process samples
    for j, (xref, yref, xcom, ycom) in enumerate(samples):
        # remove any double values in OD because of OD plateau'ing
        uxref, uiref = np.unique(xref, return_inverse=True)
        uyref = np.array(
            [
                np.median(yref[np.nonzero(uiref == i)[0]])
                for i in range(len(uxref))
            ]
        )
        uxcom, uicom = np.unique(xcom, return_inverse=True)
        uycom = np.array(
            [
                np.median(ycom[np.nonzero(uicom == i)[0]])
                for i in range(len(uxcom))
            ]
        )
        # interpolate data
        iref = interp1d(uxref, uyref, fill_value="extrapolate", kind="slinear")
        icom = interp1d(uxcom, uycom, fill_value="extrapolate", kind="slinear")
        # find common range of x
        uxi = np.max([uxref[0], uxcom[0]])
        uxf = np.min([uxref[-1], uxcom[-1]])
        # perform integration to find normalized area between curves
        if abs:

            def igrand(x):
                return np.abs(iref(x) - icom(x))

        else:

            def igrand(x):
                return iref(x) - icom(x)

        fps[j] = integrate.quad(igrand, uxi, uxf, limit=100, full_output=1)[
            0
        ] / (uxf - uxi)
        if norm:
            # calculate area under curve of reference strain as a normalisation
            def igrand(x):
                return iref(x)

            nrm[j] = integrate.quad(
                igrand, uxi, uxf, limit=100, full_output=1
            )[0] / (uxf - uxi)
        # an example figure
        if figs and j == 0:
            plt.figure()
            plt.plot(uxref, uyref, "k-", uxcom, uycom, "b-")
            x = np.linspace(uxi, uxf, np.max([len(uxref), len(uxcom)]))
            plt.fill_between(x, iref(x), icom(x), facecolor="red", alpha=0.5)
            plt.xlabel("OD")
            plt.ylabel(y)
            plt.legend(
                [
                    ref[0] + ": " + ref[2] + " in " + ref[1],
                    com[0] + ": " + com[2] + " in " + com[1],
                ],
                loc="upper left",
                bbox_to_anchor=(-0.05, 1.15),
            )
            plt.show()
    if norm:
        return (
            np.median(fps),
            statserr(fps),
            np.median(nrm),
            statserr(nrm),
        )
    else:
        return np.median(fps), statserr(fps)
