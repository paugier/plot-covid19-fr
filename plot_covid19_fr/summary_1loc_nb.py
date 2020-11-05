import matplotlib.pyplot as plt

import ipywidgets as widgets

from .util import default_first_day_in_plot, create_date_object, format_date
from .departements import DEPARTMENTS

from .plot_france import plot_france, date_file, date_file_Ymd
from .plot_1dep import plot_1dep
from .plot_hospi import plot_hospi


class Summary1loc:
    def __init__(self, loc="France"):
        self.loc = loc

        self.widget_yscale = widgets.RadioButtons(
            options=["log", "linear", "linear daily"],
            value="linear",
            description="Type:",
            disabled=False,
        )
        self.widget_yscale.observe(self.change_yscale)

        if loc != "France":
            self.widget_dep = widgets.Dropdown(
                options=[
                    (idep + " - " + dep, idep)
                    for idep, dep in DEPARTMENTS.items()
                ],
                value=loc,
                description="Département :",
            )
            self.widget_dep.observe(self.change_dep)
            top_left = self.widget_dep
        else:
            top_left = None

        self.widget_date_picker = widgets.DatePicker(
            description="Date début",
            value=create_date_object(default_first_day_in_plot),
            disabled=False,
        )
        self.widget_date_picker.observe(self.change_date)

        self.layout_inputs = widgets.TwoByTwoLayout(
            top_left=top_left,
            bottom_left=self.widget_date_picker,
            top_right=self.widget_yscale,
            bottom_right=None,
        )

        self.ax = None
        self.axes_incidence = None
        self.axes_hospi = None

    def create_subplots(self):
        fig = plt.figure(figsize=(14, 5))
        grid = plt.GridSpec(
            2,
            3,
            left=0.05,
            right=0.97,
            bottom=0.15,
            top=0.92,
            wspace=0.2,
            hspace=0.2,
        )
        ax = fig.add_subplot(grid[:, 0])
        ax_incidence = fig.add_subplot(grid[0, 1])
        ax_number_tests = fig.add_subplot(grid[1, 1], sharex=ax_incidence)
        axes_incidence = (ax_incidence, ax_number_tests)
        ax_hospi0 = fig.add_subplot(grid[0, 2])
        ax_hospi1 = fig.add_subplot(grid[1, 2], sharex=ax_hospi0)
        axes_hospi = (ax_hospi0, ax_hospi1)
        fig.text(0.02, 0.975, f"Données SI-DEP {date_file}")
        self.ax = ax
        self.axes_incidence = axes_incidence
        self.axes_hospi = axes_hospi
        return ax, axes_incidence, axes_hospi

    def clear(self):
        self.ax.clear()
        for _ in self.axes_incidence + self.axes_hospi:
            _.clear()

    def plot(self):

        if self.ax is None:
            self.create_subplots()
        else:
            self.clear()

        ax = self.ax
        axes_incidence = self.axes_incidence

        yscale = self.widget_yscale.value

        if self.loc == "France":
            plot_france(
                yscale=yscale,
                ax=ax,
                with_incidence=True,
                axes_incidence=axes_incidence,
                first_day_in_plot=format_date(self.widget_date_picker.value),
            )
        else:
            plot_1dep(
                self.widget_dep.value,
                yscale=yscale,
                ax=ax,
                with_incidence=True,
                axes_incidence=axes_incidence,
                first_day_in_plot=format_date(self.widget_date_picker.value),
            )

        plot_hospi(
            self.loc,
            axes=self.axes_hospi,
            title="Données hospitalières",
            yscale=yscale,
            first_day_in_plot=format_date(self.widget_date_picker.value),
        )

        if yscale == "log":
            ylim = list(ax.get_ylim())
            ylim[0] = 0.8
            ax.set_ylim(ylim)
            ylim = ax.get_ylim()

        if yscale == "log":
            yscale_for_title = f"_{yscale}"
        else:
            yscale_for_title = ""

        if self.loc == "France":
            loc_for_title = self.loc
        else:
            loc_for_title = f"dep{self.loc}"

        window_title = f"fig_{loc_for_title}{yscale_for_title}_{date_file_Ymd}"
        self.ax.figure.canvas.set_window_title(window_title)

        # fig.canvas.draw()
        # fig.canvas.flush_events()

        plt.show()

    def change_yscale(self, change):
        new = change["new"]
        if new not in ["linear", "log", "linear daily"]:
            return

        if change["name"] != "value":
            return

        self.plot()

    def change_dep(self, change):
        if not change.new or not isinstance(change.new, str):
            return
        dep = change.new
        if not dep[0].isnumeric() or " - " in dep:
            return

        self.loc = dep
        self.plot()

    def change_date(self, change):
        if change["name"] == "value" and change["old"] != change["new"]:
            self.plot()


if __name__ == "__main__":

    summ = Summary1loc("38")
    summ.plot()
