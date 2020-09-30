import numpy as np
import matplotlib.pyplot as plt


def euler(before, rhs, dt):
    """Forward Euler time stepping

    rhs: right hand side
    """
    return before + rhs * dt


def smooth_step(x):
    return 0.5 + 0.5 * np.tanh(x)


nb_days = 130
nb_points = nb_days
timestep = nb_days / nb_points
times = np.linspace(0, nb_days, nb_points + 1)
assert len(times) == nb_points + 1
assert times[1] == timestep


def compute_incidence(sigma, incidence0=14):

    log_incidence_value = np.log(incidence0)
    log_incidences = np.empty_like(times)
    log_incidences[0] = log_incidence_value

    for it in range(1, nb_points + 1):
        log_incidences[it] = log_incidence_value = euler(
            log_incidence_value, sigma[it - 1], timestep
        )

    return np.exp(log_incidences)


fig, (ax, ax1) = plt.subplots(
    2, 1, gridspec_kw=dict(height_ratios=[2 / 3, 1 / 3])
)
ax.set_ylabel("incidence (perfect testing)")
ax1.set_ylabel("growth rate (1/day)")
ax1.set_xlabel("time (day)")

# model 0
doubling_time = 11
sigma0 = np.log(2) / doubling_time
doubling_time *= -10
sigma1 = np.log(2) / doubling_time
t1 = 30
nb_days_change = 10
sigma = sigma0 * smooth_step(
    -(times - t1) / nb_days_change
) + sigma1 * smooth_step((times - t1) / nb_days_change)
incidences = compute_incidence(sigma)

ax.plot(times, incidences, label="model 0")
ax1.plot(times, sigma)

# model 1
doubling_time = 11
sigma0 = np.log(2) / doubling_time
doubling_time *= -3
sigma1 = np.log(2) / doubling_time
t1 = 30
nb_days_change = 10
sigma = sigma0 * smooth_step(
    -(times - t1) / nb_days_change
) + sigma1 * smooth_step((times - t1) / nb_days_change)
incidences = compute_incidence(sigma)

ax.plot(times, incidences, label="model 1")
ax1.plot(times, sigma)

# model 3
doubling_time = 11
sigma0 = np.log(2) / doubling_time
doubling_time *= -4
sigma1 = np.log(2) / doubling_time
t1 = 30
doubling_time = 11
sigma2 = np.log(2) / doubling_time
t2 = 60
doubling_time *= -10
sigma3 = np.log(2) / doubling_time
t3 = 80

nb_days_change = 10
sigma = (
    sigma0 * smooth_step(-(times - t1) / nb_days_change)
    + sigma1
    * smooth_step((times - t1) / nb_days_change)
    * smooth_step(-(times - t2) / nb_days_change)
    + sigma2
    * smooth_step((times - t2) / nb_days_change)
    * smooth_step(-(times - t3) / nb_days_change)
    + sigma3 * smooth_step((times - t3) / nb_days_change)
)

incidences = compute_incidence(sigma)

ax.plot(times, incidences, label="model 2")
ax1.plot(times, sigma)

ax.legend()

fig.tight_layout()

plt.show()
