import ipywidgets as widgets

from .plot_incidence_versus_tests import plot_incidence_vs_tests, date_file


class StatePlotIncidenceVersusTests:
    def __init__(self, min_incidence=150):
        self.index_friday = 0
        self.last_days = False
        self.min_incidence = min_incidence
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
            value=120, description="Minimum:", disabled=False
        )
        self.widget_max_incidence = widgets.IntText(
            value=2000, description="Maximum:", disabled=False
        )

        self.widget_button = widgets.Button(
            description="Retracer",
            disabled=False,
            button_style="",  # 'success', 'info', 'warning', 'danger' or ''
            tooltip="Retracer la figure avec les nouvelles données d'entrée",
            icon="sync-alt",  # (FontAwesome names without the `fa-` prefix)
        )

        self.widget_button.on_click(self.sync)

        self.layout_inputs = widgets.TwoByTwoLayout(
            top_left=self.widget_max_incidence,
            bottom_left=self.widget_min_incidence,
            top_right=self.widget_button,
        )

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

    def sync(self, button):
        self.min_incidence = self.widget_min_incidence.value
        self.max_incidence = self.widget_max_incidence.value
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
