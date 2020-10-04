import ipywidgets as widgets

from .plot_incidence_versus_tests import plot_incidence_vs_tests, date_file


class StatePlotIncidenceVersusTests:
    def __init__(self):
        self.index_friday = 0
        self.last_days = False
        self.min_incidence = 120
        self.max_incidence = None

        options = [
            "Derniers jours",
            "Dernière semaine",
            "Avant dernière semaine",
            "Avant avant dernière semaine",
        ]
        self.widget_date = widgets.Dropdown(
            options=options, value=options[1], description="Période :",
        )
        self.widget_date.observe(self.handle_change_date)

        self.widget_min_incidence = widgets.IntText(
            value=120, description="Incidence minimum:", disabled=False
        )
        self.widget_min_incidence.observe(self.handle_change_min_incidence)

        self.widget_max_incidence = widgets.IntText(
            value=2000, description="Incidence maximum:", disabled=False
        )
        self.widget_max_incidence.observe(self.handle_change_max_incidence)

    def set_ax(self, ax):
        self.ax = ax

    def handle_change_date(self, change):
        if change["name"] != "index" or change["type"] != "change":
            return

        new = change["new"]
        if change["old"] == new:
            return

        if new == 0:
            self.last_days = True
            self.index_friday = 0
        else:
            self.last_days = False
            self.index_friday = -new + 1

        self.plot()

    def handle_change_min_incidence(self, change):
        if change["name"] != "value" or change["type"] != "change":
            return
        self.min_incidence = change["new"]
        self.plot()

    def handle_change_max_incidence(self, change):
        if change["name"] != "value" or change["type"] != "change":
            return
        self.max_incidence = change["new"]
        self.plot()

    def plot(self):
        self.ax.clear()
        plot_incidence_vs_tests(
            index_friday=self.index_friday,
            last_days=self.last_days,
            ax=self.ax,
            min_incidence=self.min_incidence,
            max_incidence=self.max_incidence,
        )
        self.ax.figure.tight_layout()
        window_title = f"incidence_vs_tests{date_file}"
        self.ax.figure.canvas.set_window_title(window_title)
