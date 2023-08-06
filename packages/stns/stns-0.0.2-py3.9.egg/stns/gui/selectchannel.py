from tkinter import StringVar, OptionMenu
import tkinter as tk
from tkinter.ttk import Button, OptionMenu
from stns.io import loadspike2, get_channel_names

__all__ = ['SelectChannelPage']

class SelectChannelPage(tk.Frame):
    """

    """

    def __init__(self, parent, controller):
        """

        :param parent:
        :param controller:
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.load_file = controller.load_file
        self.channels_available = self.get_channel_names()
        # Create drop down menu for loading channels and buttons to click for plotting and analysis parameter entry
        self.channel_drop_down = StringVar(master=self.master, value="Select A Channel")
        # The *self.channels_available means extract elements of this list [self.channels_available being the list]
        OptionMenu(self.master, self.channel_drop_down, *self.channels_available).grid(row=1, column=0, sticky='nswe')
        # Create various Buttons for the start page
        Button(self.master, text="Plot Signal", command=self.select_channel).grid(row=2, column=0, sticky='nswe')
        Button(self.master, text="Enter Analysis Parameters",command=self.enter_analysis_parameters
               ).grid(row=3, column=0, sticky='nswe')
        self.visible_channels = []

    def enter_analysis_parameters(self):
        page = self.controller.get_page("ParameterEntryPage")
        page.make_analysis_parameter_window()

    def load_data(self, channel_name=None):
        return loadspike2(path=self.load_file, channel_name=channel_name)

    def get_channel_names(self):
        ch_name = get_channel_names(self.load_file)
        print('Available channels are: ', ch_name)
        return ch_name

    def show_plot(self):
        plot = self.controller.get_page("TimeseriesPage")
        plot.add_plot()

    def select_channel(self):
        """Select a channel of data to analyze using the drop-down menu and then plot it"""
        self.channel = str(self.channel_drop_down.get())
        self.set_channel_data(channel_name=self.channel)
        self.show_plot()
        return

    def set_channel_data(self, channel_name=None):
        self.channel_dict = self.load_data(channel_name=channel_name)
        self.data = self.channel_dict['data']
        self.times = self.channel_dict['times']
        self.channel = channel_name

        if self.channel not in self.visible_channels:
            self.visible_channels.append(self.channel)
            # TODO: change this into a dictionary?