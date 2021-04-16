from datetime import datetime, timedelta

import numpy as np

from numba import jit

from .load_data import population
from .load_data import load_dataframe_dep

default_first_day_in_plot = "2021-03-01"

fmt_date = "%Y-%m-%d"


def compute_min_incidence_default():
    df = load_dataframe_dep()
    df = df[df.cl_age90 == 0]
    incidences = []
    for dep in df.dep.unique():
        if len(dep) > 2:
            # skip DOM-TOM (only "métropole")
            continue
        tmp = df[df.dep == dep].copy()
        complete_df_1loc_1age(tmp, dep)
        last = tmp[tmp.index == tmp.index.max()]
        incidences.append(last["incidence"].values[0])
    incidences.sort()
    return round(incidences[-13])


def create_date_object(date: str):
    return datetime.strptime(date, fmt_date)


def format_date_for_human(date: str):
    date_obj = create_date_object(date)
    return date_obj.strftime("%d/%m/%Y")


def format_date(date_obj):
    return date_obj.strftime(fmt_date)


def shift_date_str(date: str, nb_days: int):
    date_new = create_date_object(date) + timedelta(nb_days)
    return format_date(date_new)


@jit
def cumul7(data: "int[]"):
    n = 7
    ret = np.empty_like(data)

    tmp = 0
    for i in range(n):
        ret[i] = tmp = tmp + data[i]

    for i in range(n, len(data)):
        ret[i] = tmp = tmp + data[i] - data[i - n]

    return ret


def complete_df_1loc_1age(tmp, dep=None):

    tmp["Tc"] = cumul7(tmp["T"].values)
    tmp["Pc"] = cumul7(tmp["P"].values)
    tmp["ratio_c"] = 100 * tmp["Pc"] / tmp["Tc"]

    if dep is not None:
        tmp["incidence"] = 100000 / population[dep] * tmp["Pc"]


def estimate_Reff(serie, date_R_begin, date_R_end):
    serie = serie[(serie.index >= date_R_begin) & (serie.index <= date_R_end)]
    log2_I = np.log2(serie.values)
    sigma12, _ = np.polyfit(np.arange(len(log2_I)), log2_I, 1)
    R_eff = 2 ** (7 * sigma12)
    return R_eff, 1 / sigma12


min_incidence_default = compute_min_incidence_default()
