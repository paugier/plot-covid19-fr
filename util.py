import numpy as np

from transonic import jit

from load_data import population

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


def complete_df_1dep_1age(tmp, dep=None):

    tmp["Tc"] = cumul7(tmp["T"].values)
    tmp["Pc"] = cumul7(tmp["P"].values)
    tmp["ratio_c"] = 100 * tmp["Pc"] / tmp["Tc"]

    if dep is not None:
        tmp["incidence"] = 100000 * tmp["Pc"] / population[dep]
