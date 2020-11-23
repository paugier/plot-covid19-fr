import matplotlib.pyplot as plt
import ipywidgets as widgets

from .plot_faster_dyn import plot_faster_dyn
from .plot_france import date_file
from .util import default_first_day_in_plot, create_date_object, format_date


class PlotFasterDyn:
    def __init__(self, min_incidence=250):

        self.axes = None

        self.min_incidence = min_incidence
        self.max_incidence = None

        self.widget_min_incidence = widgets.IntText(
            value=min_incidence, description="Minimum:", disabled=False
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

        self.widget_date_picker = widgets.DatePicker(
            description="Date début",
            value=create_date_object(default_first_day_in_plot),
            disabled=False,
        )

        self.widget_button.on_click(self.sync)

        self.layout_inputs = widgets.TwoByTwoLayout(
            top_left=self.widget_max_incidence,
            bottom_left=self.widget_min_incidence,
            top_right=self.widget_date_picker,
            bottom_right=self.widget_button,
        )

    def set_axes(self, axes):
        self.axes = axes

    def create_axes(self):
        _, self.axes = plt.subplots(1, 3, figsize=(14, 5))

    def sync(self, button):
        self.min_incidence = self.widget_min_incidence.value
        self.max_incidence = self.widget_max_incidence.value
        self.plot()

    def plot(self):
        if self.axes is None:
            self.create_axes()

        fig = self.axes[0].figure
        fig.texts.clear()
        for _ in self.axes:
            _.clear()
        plot_faster_dyn(
            axes=self.axes,
            min_incidence=self.min_incidence,
            max_incidence=self.max_incidence,
            first_day_in_plot=format_date(self.widget_date_picker.value),
        )
        for _ in self.axes[1:]:
            _.get_legend().remove()

        text = f"Données SI-DEP {date_file}, "
        if self.max_incidence is None:
            text += f"incidence > {self.min_incidence}"
        else:
            text += f"{self.min_incidence} < incidence < {self.max_incidence}"

        fig.text(0.03, 0.975, text)
        fig.tight_layout(rect=(0, 0, 1, 0.98))
