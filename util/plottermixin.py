__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."

import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime
import constants

"""
    Wraps the parameters for plots. The static methods generated a '.png' file which name is time stamped.
    :param num_epochs  Expected number of epochs in the training or training/evaluation
    :param x_label Label for X-axis
    :param y_label Label for Y_axis
    :param title Title for the plot
"""


class PlotterParameters(object):
    def __init__(self, count: int, x_label: str, y_label: str, title: str):
        self.count = count
        self.x_label = x_label
        self.y_label = y_label
        self.title = title
        self.time_str = datetime.now().strftime("%b-%d-%Y:%H.%M")

    def __str__(self) -> str:
        return self.title

    def __repr__(self):
        return f"{self.__class__.__name__}()"


class PlotterMixin(object):
    @staticmethod
    def single_plot_np_array(np_array1: np.array, np_array2: np.array, plotter_parameters: PlotterParameters):
        fig, axes = plt.subplots()
        axes.plot(np_array1, np_array2)
        axes.set(xlabel=plotter_parameters.x_label, ylabel=plotter_parameters.y_label, title=plotter_parameters.title)
        axes.grid()
        fig.savefig(f"{constants.images_folder}/plot-{plotter_parameters.time_str}.png")
        plt.show()

    @staticmethod
    def single_plot(values1: list, plotter_parameters: PlotterParameters):
        fig, axes = plt.subplots()
        x = np.arange(0, len(values1), 1)
        y = np.asarray(values1)
        axes.plot(x, y)
        axes.set(xlabel=plotter_parameters.x_label, ylabel=plotter_parameters.y_label, title=plotter_parameters.title)
        axes.grid()
        fig.savefig(f"{constants.images_folder}/plot-{plotter_parameters.time_str}.png")
        plt.show()

    @staticmethod
    def two_plot(values1: list, values2: list, plotter_parameters_list: list):
        assert len(plotter_parameters_list) == 2, f'Number of plots {plotter_parameters_list.count} should be 2'
     #   assert len(values1) == len(values2), f'Size of features {len(values1)} should be == Size labels {len(values2)}'

        fig, axes = plt.subplots(2)
        first_plot = plotter_parameters_list[0]
        x = np.arange(0, first_plot.count, 1)
        y = np.asarray(values1)
        axes[0].plot(x, y)
        axes[0].set(xlabel=first_plot.x_label, ylabel=first_plot.y_label,title=first_plot.title)
        axes[0].grid()

        second_plot = plotter_parameters_list[1]
        y = np.asarray(values2)
        axes[1].plot(x, y)
        axes[1].set(xlabel=second_plot.x_label, ylabel=second_plot.y_label,title=second_plot.title)
        axes[1].grid()
        fig.savefig(f"{constants.images_folder}/plot-{PlotterMixin.timestr()}.png")
        plt.show()

    @staticmethod
    def three_plot(values1: list, values2: list, values3: list, plotter_parameters_list: list):
        assert len(plotter_parameters_list) == 3, f'Number of plots {plotter_parameters_list.count} should be 3'
        assert len(values1) == len(values2), f'Size of features {len(values1)} should be == Size labels {len(values2)}'
        assert len(values1) == len(values3), f'Size of features {len(values1)} should be == Size z {len(values3)}'

        fig, axes = plt.subplots(3)
        first_plot = plotter_parameters_list[0]
        x = np.arange(0, len(values1), 1)
        y = np.asarray(values1)
        axes[0].plot(x, y)
        axes[0].set(xlabel=first_plot.x_label, ylabel=first_plot.y_label, title=first_plot.title)
        axes[0].grid()

        second_plot = plotter_parameters_list[1]
        y = np.asarray(values2)
        axes[1].plot(x, y)
        axes[1].set(xlabel=second_plot.x_label, ylabel=second_plot.y_label, title=second_plot.title)
        axes[1].grid()

        third_plot = plotter_parameters_list[2]
        y = np.asarray(values3)
        axes[2].plot(x, y)
        axes[2].set(xlabel=third_plot.x_label, ylabel=third_plot.y_label, title=third_plot.title)
        axes[2].grid()
        fig.savefig(f"{constants.images_folder}/plot-{PlotterMixin.timestr()}.png")
        # plt.show()

    @staticmethod
    def timestr() -> str:
        return datetime.now().strftime("%b-%d-%Y-%H.%M.%S")
