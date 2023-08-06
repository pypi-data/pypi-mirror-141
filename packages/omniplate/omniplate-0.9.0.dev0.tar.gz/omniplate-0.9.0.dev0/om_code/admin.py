# General admin functions
# generating and updating dataframes and the progress dictionary
import pandas as pd


def initialiseprogress(inst, experiment):
    """
    Initialises progress dictionary.
    """
    inst.progress["ignoredwells"][experiment] = []
    inst.progress["negativevalues"][experiment] = False
    inst.progress["getstatsGP"][experiment] = {
        c: {} for c in inst.allconditions[experiment]
    }
    inst.progress["gc"][experiment] = None


###


def makewellsdf(df_r):
    """
    Makes a dataframe that stores the contents of
    the wells
    """
    df = df_r[["experiment", "condition", "strain", "well"]].drop_duplicates()
    df = df.reset_index(drop=True)
    return df


###


def make_s(inst, tmin=None, tmax=None):
    """
    Generate s datafram by calculating means and variances of all datatypes
    from raw data
    """
    # restrict time
    if tmin and not tmax:
        rdf = inst.r[inst.r.time >= tmin]
    elif tmax and not tmin:
        rdf = inst.r[inst.r.time <= tmax]
    elif tmin and tmax:
        rdf = inst.r[(inst.r.time >= tmin) & (inst.r.time <= tmax)]
    else:
        rdf = inst.r
    # find means
    df1 = (
        rdf.groupby(["experiment", "condition", "strain", "time"])
        .mean()
        .reset_index()
    )
    for exp in inst.allexperiments:
        for dtype in inst.datatypes[exp]:
            df1 = df1.rename(columns={dtype: dtype + " mean"})
    # find errors
    df2 = (
        rdf.groupby(["experiment", "condition", "strain", "time"])
        .std()
        .reset_index()
    )
    for exp in inst.allexperiments:
        for dtype in inst.datatypes[exp]:
            df2 = df2.rename(columns={dtype: dtype + " err"})
    return pd.merge(df1, df2)


###


def update_s(inst):
    """
    Updates means and errors of all datatypes from raw data
    """
    # find tmin and tmax in case restrict_time has been called
    tmin = inst.s.time.min()
    tmax = inst.s.time.max()
    # recalculate s dataframe
    inst.s.update(make_s(inst, tmin, tmax))


###
