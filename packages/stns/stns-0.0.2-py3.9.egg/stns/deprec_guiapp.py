"""deprec_guiapp.py contains the SpikeDetectionGUI class used for data analysis in python
author: loganfickling@gmail.com

DEPRECIATED See stns.gui for more recent code
"""
from tkinter import Tk, StringVar, OptionMenu, IntVar, BooleanVar
import tkinter as tk
from tkinter.ttk import Button, Checkbutton, Entry, Label, OptionMenu
import matplotlib #as mpl
from matplotlib import rcParams
import numpy as np
import pandas as pd
from matplotlib.figure import Figure
from scipy.stats import zscore
import sys
import os
import re
from stns.io import loadspike2, get_channel_names
from stns.detect import find_close_data, find_spike_indices, find_nearest
from tkinter.filedialog import askopenfilename, askdirectory, asksaveasfilename
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RectangleSelector
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from copy import deepcopy
from glob import glob
import seaborn as sns
from pandastable import Table
from functools import partial


matplotlib.use("TkAgg")
# Below fixes OverflowError: In draw_path: Exceeded cell block limit
rcParams['agg.path.chunksize'] = 10000
sns.set(context='paper', style='darkgrid', palette='colorblind')
#sns.set_palette('colorblind')
LARGE_FONT= ("Verdana", 12)

__all__ = ['SpikeDetectionGUI', 'str_to_class']

# TODO BUGS:
"""

-Need to make sure that it functions correctly if only a start or only an end time is given but not the other. 
-When a channel is initially loaded (e.g. dvn) then a second channel is plotted (e.g. lgn) and a z-score is done
for some reason it applies it to the first ch not the most recent one...

-When the x-axis is updated for example changing from default 50 to 25 there's a bug where the slider won't be able to
slide all the way, for some reason this bug is ended when the z-score is applied

TODO: y-axis shouldn't be reset whenever spikes are detected, keep old y-axis...!

# If you put a start but not an end it does all the time but it should instead auto-enter the last time point

"""

# TODO FEATURES:
"""
- when clicking plot signal if there's a large amount of data have some feature for slicing the data around specific 
points if the user knows when the relevant part of the data is -> load_add=True, default setting?

# Add ch window: Should automatically close once user hits the button

TODO: Need to remove delete channel button if channel is deleted

# The Burst line indicater plots at 0, this is an issue for intracellulars where values are ~-60:-30

-Needs a check to ensure that the maximum is < minimum if both are provided

TODO: Be able to save changes when redoing detect?

"""
# Utility functions
def str_to_class(classname):
    """Returns the given object in namespace when given a string input of the obect's name

    :param classname: str, object.__main__, e.g. 'Cat' -> class Cat
    :return:
    """
    return getattr(sys.modules[__name__], classname)

class TimeseriesPage(tk.Frame):
    """
    """

    def __init__(self, parent, controller):
        """

        :param parent:
        :param controller:
        """
        tk.Frame.__init__(self, parent)
        #self.create_adjust_y_axis_window = None
        self.controller = controller
        self.spikes_user_added = []
        self.spikes_user_removed = []
        # These parameters will correspond to a button and user feedback later
        self.toggle_add_spike_button = False
        self.toggle_del_spike_button = False
        self.toggle_rect_button = False
        self.RS = None
        self.cid_add = None
        self.cid_remove = None
        self.cid_rect = None
        self.applied_zscore = False
        self.x_axis_step = IntVar(value=50)
        self.y_axis_entry = {v: StringVar() for v in ['maximum y', 'minimum y']}
        self.canvas = None
        self.y_mins = {}
        self.y_maxs = {}
        self.x_axis_n_ticks = IntVar(value=5)
        self.y_axis_n_ticks = IntVar(value=5)
        self._added_lines = []

    def apply_zscore(self): # Move
        if not hasattr(self, 'data'):
            self.set_data()
        # Want function to behave such that clicking it once turns it on, clicking it again turns it off
        if self.applied_zscore:
            print('Undoing applied_zscore')
            self.data = deepcopy(self._data)
            self._data = None
            self.applied_zscore = False

        elif not self.applied_zscore:
            print('Doing applied_zscore')
            self._data = deepcopy(self.data)
            self.data = zscore(self.data)
            self.applied_zscore = True
        # TODO: There has to be a better way than just re-rendering the entire thing
        #self.plot_ts_slide(y_data=self.data, x_data=self.times, channel=self.channel)
        try:
            self.add_plot()
        except AttributeError as e:
            print(e)
            self.plot_ts_slide(y_data=self.data, x_data=self.times, channel=self.channel)

    def reset_slider(self):
        self.spos.reset()
        return

    def create_adjust_x_axis_window(self):
        """Creates a new window to adjust the x-axis"""
        self.x_axis_window = tk.Toplevel(self.master)
        Label(self.x_axis_window, text='Change x axis range').grid(row=0, column=0)
        Entry(self.x_axis_window, textvariable=self.x_axis_step).grid(row=0, column=1)
        Label(self.x_axis_window, text='Change number of ticks').grid(row=1, column=0)
        Entry(self.x_axis_window, textvariable=self.x_axis_n_ticks).grid(row=1, column=1)
        Button(self.x_axis_window, text="Draw", command=self.update_x_axis).grid(row=2, column=1)

    def update_x_axis(self):
        """Updates the x-axis based upon user input"""
        if not hasattr(self, 'data'): # TODO: Under which conditions does this need to be done?
            print('Setting data....')
            self.set_data()
        n_ticks = self.x_axis_n_ticks.get()

        for i, ax in enumerate(self.fig.axes):
            if i + 1 == len(self.fig.axes):
                break
            start, end = ax.get_xlim()
            if start-end != self.x_axis_step.get():

                #TODO: Need to change this so that the slider doesn't limit the x-range
                # Change the xaxis in the matplotlib figure
                ax.set_xlim(start, start+self.x_axis_step.get())
                ax.xaxis.set_ticks(np.arange(start, start + self.x_axis_step.get(), self.x_axis_step.get() / n_ticks))
        self.fig.canvas.draw()
        self.x_axis_window.destroy()

        #axpos = self.fig.add_axes([0.12, 0.1, 0.75, 0.05], facecolor="#3498db")
        #self.spos = Slider(ax=axpos, label='', valmin=x_dat[0], valmax=x_dat[-1] - int(self.x_axis_step.get()))

    def create_adjust_y_axis_window(self):
        """Creates a new window to adjust the y-axis"""
        self.y_axis_window = tk.Toplevel(self.master)
        for k,v in enumerate(self.y_axis_entry):
            Label(self.y_axis_window, text="{} =".format(v)).grid(row=k, column=0)
            Entry(self.y_axis_window, textvariable=self.y_axis_entry[v]).grid(row=k, column=1)
        Button(self.y_axis_window, text="Update", command=self.update_y_axis).grid(row=3, column=1)

        # Make sure you know for which channel
        page = self.controller.get_page("SelectChannelPage")
        #channels_available = page.get_channel_names()
        Label(self.y_axis_window, text='Change number of ticks').grid(row=2, column=0)
        Entry(self.y_axis_window, textvariable=self.y_axis_n_ticks).grid(row=2, column=1)
        self.yaxis_channel_drop_down = StringVar(master=self.y_axis_window, value="Select A Channel")
        #self.yaxis_channel_section = OptionMenu(self.y_axis_window, self.yaxis_channel_drop_down, *channels_available)

        self.yaxis_channel_section = OptionMenu(self.y_axis_window, self.yaxis_channel_drop_down, *page.visible_channels)
        self.yaxis_channel_section.grid(row=3, column=0)

    def update_y_axis(self, n_ticks=10.):
        """Updates the y-axis based upon user input"""
        # User input
        yaxis_ch_selection = self.yaxis_channel_drop_down.get()
        self.y_maxs[yaxis_ch_selection] = self.y_axis_entry['maximum y'].get()
        self.y_mins[yaxis_ch_selection] = self.y_axis_entry['minimum y'].get()
        # Stored as stringvars so need to convert into a float
        y_min = float(self.y_mins[yaxis_ch_selection])
        y_max = float(self.y_maxs[yaxis_ch_selection])
        # Find out which axis you want to update from ch name
        page = self.controller.get_page("SelectChannelPage")
        index = [i for i, channel in enumerate(page.visible_channels) if channel==yaxis_ch_selection][0]
        # TODO: This will fail if user inputs multiple of same channel
        self.fig.axes[index].set_ylim(y_min, y_max)
        #self.fig.axes[index].yaxis.set_ticks(np.arange(y_min, y_max, (y_max-y_min) / self.y_axis_n_ticks.get()))
        self.fig.axes[index].yaxis.set_ticks(np.arange(y_min, y_max, (y_max-y_min) / float(self.y_axis_n_ticks.get())))
        self.fig.canvas.draw()
        self.y_axis_window.destroy()
        return


    def set_data(self):
        page = self.controller.get_page("SelectChannelPage")
        self.channel = page.channel
        self.data = page.data
        self.times = page.times
        #self.channel_dict = page.channel_dict


    def add_channel(self):
        self.add_ch_window = tk.Toplevel(self.master)
        page = self.controller.get_page("SelectChannelPage")
        channels_available = page.channels_available
        self.channel_drop_down = StringVar(master=self.add_ch_window, value="Select A Channel")
        # Create drop down menu for loading channels and buttons to click for plotting and analysis parameter entry
        # The *self.channels_available means extract elements of this list (self.channels_available being the list)
        self.second_ch_selection = OptionMenu(self.add_ch_window, self.channel_drop_down, *channels_available)
        self.second_ch_selection.grid(row=1, column=0, sticky='nswe')
        #Button(self.add_ch_window, text="Add Channel", command=self.__add_second_channel).grid(row=2, column=0)
        Button(self.add_ch_window, text="Add Channel", command=self._add_plot).grid(row=2, column=0)

    def make_plot_buttons(self):
        # Buttons for various changing of view for graph
        b0 = Button(self.master, text="Reset Slider", command=self.reset_slider)
        b0.grid(row=2, column=1, sticky='nsew')
        b1 = Button(self.master, text="Adjust y-axis", command=self.create_adjust_y_axis_window)
        b1.grid(row=3, column=1, sticky='nsew')
        b2 = Button(self.master, text="Adjust x-axis", command=self.create_adjust_x_axis_window)
        b2.grid(row=4, column=1, sticky='nsew')
        b3 = Button(self.master, text="Z-score Data", command=self.apply_zscore)
        b3.grid(row=5, column=1, sticky='nsew')
        # TODO: Burst analysis or just the add click thing here?
        b4 = Button(self.master, text="Toggle Add Spikes With Right Click", command=self.toggle_add)
        b4.grid(row=2, column=2, sticky='nsew')
        b5 = Button(self.master, text="Add Another Channel", command=self.add_channel)
        b5.grid(row=5, column=0, sticky='nsew')

    def rectangle_add_line(self, eclick, erelease):
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        if x2 <= x1:
            return
        print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
        print(" The button you used were: %s %s" % (eclick.button, erelease.button))

        if ((eclick.inaxes != self.fig.axes[0]) or (eclick.button != 3)):
            return

        if (y1, x1, x2) not in self._added_lines:
            self._added_lines.append((y1, x1, x2))


        self.fig.axes[0].hlines(y=y1, xmin=x1, xmax=x2, color='k')
        # This is now functional, need similiar func as with the rect_remove
        self.fig.canvas.draw_idle()



    def rectangle_remove(self, eclick, erelease):
        'eclick and erelease are the press and release events'
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        if x2 <= x1:
            return
        print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
        print(" The button you used were: %s %s" % (eclick.button, erelease.button))

        if ((eclick.inaxes != self.fig.axes[0]) or (eclick.button != 3)):
            return

        page = self.controller.get_page("DataEntry")
        try:
            offsets = page.spike_sc.get_offsets()
        except AttributeError: # If click before spikes are detected
            return
        x = offsets[:, 0]
        keep = (x > x1) & (x < x2)
        new_xydata = offsets[~keep]
        page.spike_sc.set_offsets(new_xydata)
        self.fig.canvas.draw_idle()

    def destroy_canvas(self):
        if self.canvas != None:
            self.canvas._tkcanvas.destroy()
            self.canvas = None

    def _add_plot(self):
        channel = self.channel_drop_down.get()
        page = self.controller.get_page("SelectChannelPage")
        if channel not in page.visible_channels:
            page.visible_channels.append(channel)
        self.add_plot()

    def add_plot(self):
        self.destroy_canvas()
        page = self.controller.get_page("SelectChannelPage")
        self.make_plot_buttons()

        self.fig = Figure(figsize=(10, 5), dpi=100)
        colors = sns.color_palette("colorblind", n_colors=len(page.visible_channels))
        for i, ch in enumerate(page.visible_channels):
            page.set_channel_data(channel_name=ch)
            self.axes = self.fig.add_subplot(len(page.visible_channels), 1, i + 1) # row, col, index; mpl syntax
            self.axes.plot(page.times, page.data, color=colors[i])#, color="#2ecc71")
            #self.axes[i].set_title('{} Spikes'.format(ch), fontsize=30, y=.98)
            if i == len(page.visible_channels) - 1:
                self.axes.set_xlabel('Time (s)', fontsize=16)
            self.axes.set_ylabel('{}\nVoltage (μV)'.format(ch), fontsize=16)
            self.axes.tick_params(axis='y', which='both', labelsize=12)
            self.y_mins[ch] = np.min(page.data)
            self.y_maxs[ch] = np.max(page.data)
            self.axes.axis([page.times[0], page.times[0] + int(self.x_axis_step.get()),
                            float(self.y_mins[ch]), float(self.y_maxs[ch])]) # [xmin, xmax, ymin, ymax]
            self.axes.yaxis.set_ticks(np.arange(self.y_mins[ch],
                                                self.y_maxs[ch],
                                                (self.y_maxs[ch] - self.y_mins[ch]) / self.y_axis_n_ticks.get()))
            command_w_args = partial(self.delete_channel, ch) # partial() is done to insert an arg to a function
            b1 = Button(self.master, text="Delete Channel", command=command_w_args)
            b1.grid(row=i, column=4, sticky='nw')

        # This needs to be done in order to set the first plot done as the active one
        page.set_channel_data(channel_name=page.visible_channels[0])

        self.canvas = FigureCanvasTkAgg(self.fig, self.master)
        self.canvas.draw()
        # Create Slider object to change time value  [Left Bottom width height]
        self.axpos = self.fig.add_axes([0.12, 0.1, 0.75, 0.05], facecolor="#3498db")#'#00A08A')
        self.spos = Slider(ax=self.axpos, label='', valmin=page.times[0],
                           valmax=page.times[-1] - int(self.x_axis_step.get()))#, color="#FF0000")

        def update_xaxis(val):
            """Throw-away function that updates when the slider is moved"""
            pos = self.spos.val
            for i, ax in enumerate(self.fig.axes):
                _channel = page.visible_channels[i]
                self.fig.axes[i].axis([pos, pos + int(self.x_axis_step.get()),
                                       float(self.y_mins[_channel]), float(self.y_maxs[_channel])])
                self.fig.axes[i].xaxis.set_ticks(np.arange(pos, pos + self.x_axis_step.get(),
                                                           self.x_axis_step.get() / self.x_axis_n_ticks.get()))
                if i == (len(self.fig.axes) -2): # Should have n plots + 1 axes, the +1 being from the self.axpos slider
                    break # Want it to end after finishing the second to last axis and not include the slider
            self.fig.canvas.draw_idle()

        self.spos.on_changed(update_xaxis)  # Whenever the position of the slider changes
        self.canvas.draw_idle()
        self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=4, sticky='nesw')

        data_page = self.controller.get_page("DataEntry")

        if data_page.spike_sc is not None: # This way we skip this part when initially plotting the signal
            data_page.plot_detected_spikes()

    def delete_channel(self, channel):
        page = self.controller.get_page("SelectChannelPage")
        print('Pressed Delete Channel {}'.format(channel))
        print('Visible Channels: ', page.visible_channels)
        page.visible_channels.remove(channel)
        print('Visible Channels: ', page.visible_channels)
        self.add_plot()

    def add_spike_onclick(self, event):
        if ((event.inaxes != self.fig.axes[0]) or (event.button != 3)):
            return
        page = self.controller.get_page("DataEntry")
        try:
            offsets = page.spike_sc.get_offsets()
        except AttributeError:
            # This is when the use tries to click it before the data is set
            print('Please detect spikes first')
            return
        new_xydata = np.insert(offsets, 0, [event.xdata, event.ydata], axis=0)
        new_xydata = new_xydata[np.argsort(new_xydata[:, 0])]  # Sort based on x-axis values
        page.spike_sc.set_offsets(new_xydata)  # Add x and y data
        self.fig.canvas.draw_idle()
        return

    def remove_spike_onclick(self, event):
        print('Spike removed')
        if ((event.inaxes != self.fig.axes[0]) or (event.button != 3)):
            return
        page = self.controller.get_page("DataEntry")
        try:
            offsets = page.spike_sc.get_offsets()
        except AttributeError:
            # This is when the use tries to click it before the data is set
            print('Please detect spikes first',flush=True)
            return
        xdata = offsets[:, 0]
        xdata_click = event.xdata  # X position in values for mouse click
        xdata_nearest_index = (np.abs(xdata - xdata_click)).argmin()  # Closest index value to mouse click
        new_xydata = np.delete(offsets, np.where(xdata == xdata[xdata_nearest_index]), axis=0)  # Remove xdata
        page.spike_sc.set_offsets(new_xydata)  # update scatter plot
        self.fig.canvas.draw_idle()
        return

    def toggle_rect(self):
        self.disconnect_rect()
        if self.toggle_rect_button:
            self.connect_rect()
            print('Right click and drag to remove points')
            self.toggle_rect_button = False
        else:
            self.disconnect_rect()
            print('Stopped Rectangle Remover', flush=True)
            self.toggle_rect_button = True

    def connect_rect(self):
        self.RS = RectangleSelector(ax=self.fig.axes[0], #onselect=self.rectangle_add_line,
                                    onselect=self.rectangle_remove,
                                    drawtype='box', useblit=True,
                                    button=[1, 3],  # don't use middle button
                                    # minspanx=5, minspany=5,
                                    spancoords='data',
                                    interactive=True)
        self.RS.set_active(True)

    def disconnect_rect(self):
        if self.RS is None:
            return
        self.RS.set_active(False)

    def toggle_add(self):
        self.disconnect_remove()

        if self.toggle_add_spike_button:
            self.connect_add()
            print('Right Click to Add a Spike', flush=True)
            self.toggle_add_spike_button = False

        else:
            self.disconnect_add()
            print('Stopped Adding Spikes', flush=True)
            self.toggle_add_spike_button = True

    def connect_add(self):
        self.cid_add = self.fig.canvas.mpl_connect('button_press_event', self.add_spike_onclick)

    def disconnect_add(self):
        if self.cid_add is None:
            return
        self.fig.canvas.mpl_disconnect(self.cid_add)

    def toggle_remove(self):
        if self.toggle_del_spike_button:
            self.connect_remove()
            print('Right Click to Remove a Spike', flush=True)
            self.toggle_del_spike_button = False
        else:
            self.disconnect_remove()
            print('Removing Spikes Disabled', flush=True)
            self.toggle_del_spike_button = True

    def connect_remove(self):
        self.cid_remove = self.fig.canvas.mpl_connect('button_press_event', self.remove_spike_onclick)

    def disconnect_remove(self):
        if self.cid_remove is None:
            return
        self.fig.canvas.mpl_disconnect(self.cid_remove)


class SelectChannelPage(tk.Frame):
    """

    """
    visible_channels = []

    def __init__(self, parent, controller):
        """

        :param parent:
        :param controller:
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.load_file = controller.load_file
        #label = Label(self, text="Channel Selection Page", font=controller.title_font)
        self.channels_available = self.get_channel_names()
        self.channel_drop_down = StringVar(master=self.master, value="Select A Channel")
        # Create drop down menu for loading channels and buttons to click for plotting and analysis parameter entry
        # The *self.channels_available means extract elements of this list (self.channels_available being the list)
        OptionMenu(self.master, self.channel_drop_down, *self.channels_available
                   ).grid(row=1, column=0, sticky='nswe')
        # Create various Buttons for the start page
        Button(self.master, text="Plot Signal", command=self.select_channel).grid(row=2, column=0, sticky='nswe')
        Button(self.master, text="Enter Analysis Parameters",command=self.enter_analysis_parameters
               ).grid(row=3, column=0, sticky='nswe')
        Button(self.master, text="Analyze Channel For All .smr Files In Folder", command=self.all_files_in_folder
               ).grid(row=4, column=0, sticky='nswe')

    def all_files_in_folder(self):
        """Function for applying inputted parameters on all .smr files in the file's directory"""
        loadfile = self.load_file
        go_through = [x for x in glob(os.path.dirname(loadfile)+'/*.smr') if x != loadfile]
        ch  = self.channel_drop_down.get()
        page = self.controller.get_page("ParameterEntryPage")
        neuron = page.analysis_parameters['Neuron (Required)'].get()
        Z = page.analysis_parameters_booleans['Use Z-score (defaults as False)'].get()

        for p in go_through:
            print('Starting file {}'.format(p))
            try:
                launch = tk.Toplevel(master=self.master)
                gui = self.controller.reset(provided_path=p, root=launch)
                gui.create_main_page() # AttributeError: '_tkinter.tkapp' object has no attribute 'create_main_page' TODO FIX
                gui.channel_drop_down.set(ch)
                gui.analysis_parameters['Neuron (Required)'].set(neuron)
                gui.analysis_parameters_booleans['Use Z-score (defaults as False)'].set(Z)
                sns.set(context='paper', style='darkgrid', palette='colorblind')

            except AssertionError as e:
                print(e, 'Skipping {} for now'.format(p))
            self.master.wait_window(launch)  # Make it wait
            try:
                plt.close(gui.fig)
            except AttributeError as e:
                print(e, 'skipping {} for now'.format(p))
                continue

    def enter_analysis_parameters(self):
        page = self.controller.get_page("ParameterEntryPage")
        page.make_analysis_parameter_window()

    def load_data(self, channel_name=None):
        return loadspike2(path=self.load_file, channel_name=channel_name)

    def get_channel_names(self):
        ch_name = get_channel_names(self.load_file)
        print('channel names are: ', ch_name)
        return ch_name

    def show_plot(self):
        self.controller.show_frame("TimeseriesPage")
        plot = self.controller.get_page("TimeseriesPage")
        #plot.plot_ts_slide()
        plot.add_plot()

    def select_channel(self):
        """Select a channel of data to analyze using the drop-down menu and then plot it"""
        self.channel = str(self.channel_drop_down.get())
        self.set_channel_data(channel_name=self.channel)
        print('You got it dude! Plotting {}'.format(self.channel))
        if self.channel not in self.visible_channels:
            self.visible_channels.append(self.channel)
        self.show_plot()
        return

    def set_channel_data(self, channel_name=None):
        self.channel_dict = self.load_data(channel_name=channel_name)
        self.data = self.channel_dict['data']
        self.times = self.channel_dict['times']
        self.channel = channel_name

        if self.channel not in self.visible_channels:
            self.visible_channels.append(self.channel)


class ParameterEntryPage(tk.Frame):
    """An Object used to create related windows/frames/pages in the gui related to Parameter Entry for spike detecting

    """
    # Class level attributes
    entry_params = ['Start Time (Optional)', 'End Time (Optional)', 'Minimum Threshold (Required)',
                    'Maximum Threshold (Optional)', 'Required ISI (defaults at .01s)',
                    'Burst Tolerance (defaults at 2s)', 'Stimulation Kind (Required)', 'Date (Required)',
                    'Neuron (Required)', 'Stimulation (Required)', 'Condition (Optional)', 'Notebook (Required)']

    boolean_params = ['Find Troughs (defaults as False)', 'Use Z-score (defaults as False)']

    params = ['analysis_parameters', 'analysis_parameter_window', 'spike_detection_window']


    def __init__(self, parent, controller):
        """

        :param parent:
        :param controller:
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.load_file = controller.load_file
        # Set attributes for all the params above
        for param in ParameterEntryPage.params:
            setattr(self, param, None)

        # Create variables that will be used for storing various user inputs
        self.analysis_parameters = {v: StringVar() for k, v in enumerate(ParameterEntryPage.entry_params)}
        self.analysis_parameters_booleans = {v: BooleanVar(value=False) for v in ParameterEntryPage.boolean_params}
        #self.analysis_parameters_booleans['Find Troughs (defaults as False)'] = BooleanVar(value=False)
        self.analysis_parameters_booleans['Find Troughs (defaults as False)'] = BooleanVar(value=False)
        self.multiple_conditions_entry = {1: [IntVar(), IntVar(), IntVar()]} # Let user add arbitrary amount of conds.

        # Manually set certain parameters
        for k,v in enumerate(self.analysis_parameters):
            if 'Optional' in v:
                self.analysis_parameters[v].set(None)
            elif (('defaults at' in v) and ('.01s' in v)):
                self.analysis_parameters[v].set(.01)
            elif (('defaults at' in v) and ('2s' in v)):
                self.analysis_parameters[v].set(2)

        self.analysis_parameter_window = self # This is used in different places below
        self.has_multiple_conditions = False


    def make_analysis_parameter_window(self):
        """Creates a new window where relevant analysis parameters can be entered for spike detection"""
        self.analysis_parameter_window = tk.Toplevel(self.master)
        # Create locations to enter values for each relevant analysis parameters
        counter = 0
        for param in self.entry_params: # Changed below column 0->3, 1->4 trying to shift it over
            Label(self.analysis_parameter_window, text="{} =".format(param)).grid(row=counter, column=0,
                                                        sticky=tk.E)
            Entry(self.analysis_parameter_window, textvariable=self.analysis_parameters[param]).grid(row=counter, column=1,
                                                                           sticky=tk.E)
            counter += 1
        # Since these are True or False, we'll use a check button inside of a text enter
        for i, param in enumerate(self.analysis_parameters_booleans):
            Checkbutton(self.analysis_parameter_window, text="{}".format(param),
                        variable=self.analysis_parameters_booleans[param]).grid(row=counter, column=0, sticky=tk.E)
            counter += 1
        # Create a button for extrapolating information from the path
        self.path_extrapolation()
        # Create a button to add multiple conditions
        b1 = Button(self.analysis_parameter_window, text="Add Multiple Conditions", command=self.multiple_conditions)
        b1.grid(row=counter - 1, column=1, sticky=tk.E)
        # Create a button to collect all the values once they're entered
        b2 = Button(self.analysis_parameter_window, text="Detect Spikes", command=self.detect_spikes)
        b2.grid(row=counter - 2, column=1, sticky=tk.E)
        return

    def detect_spikes(self):
        page = self.controller.get_page("DataEntry")
        page.detect_spikes()
        page.plot_detected_spikes()
        page.create_pandas_df()
        page.plot_detected_bursts()
        #page.plot_detected_bursts()
        self.create_plot_buttons()
        self.analysis_parameter_window.destroy()

    def create_plot_buttons(self):
        # Buttons for adding and removing spikes
        page = self.controller.get_page("TimeseriesPage")
        Button(self.master, text="Toggle Add Spikes With Right Click", command=page.toggle_add).grid(row=2, column=2,
                                                                                                     sticky='nsew')
        Button(self.master, text='Toggle Remove Spikes with Right Click', command=page.toggle_remove).grid(
            row=3, column=2, sticky='nsew')
        Button(self.master, text='Toggle Remove Spikes Hold and Drag', command=page.toggle_rect).grid(
            row=4, column=2, sticky='nsew')
        Button(self.master, text='Toggle Add Burst Duration Hold and Drag', command=page.toggle_rect).grid(
            row=5, column=2, sticky='nsew')
        # Buttons for making and saving dataframes, and generating tables for data analysis
        page = self.controller.get_page("DataEntry")
        Button(self.master, text='Make DataFrames', command=page.create_pandas_df).grid(row=2, column=3, sticky='nsew')
        Button(self.master, text='Save DataFrames', command=page.save_pandas).grid(row=3, column=3, sticky='nsew')
        Button(self.master, text='Show Data by Bursts', command=page.show_burst_df).grid(row=4, column=3, sticky='nsew')
        Button(self.master, text='Show Data by Spikes', command=page.show_spike_df).grid(row=5, column=3, sticky='nsew')


    def path_extrapolation(self):
        """Uses regular expressions to extract values from the path. Assumes formatted something like:
        'b#p###-cond conditionhere-ions #_#V ##hz- intracellular neuron names in caps -cogs off_export.smr
        Note, the exact ordering of when something is entered is irrelevant, so long as the fields are there.
        """
        # Use regular expressions to do matching of string patterns in the path
        # See: https://docs.python.org/3/howto/regex.html for explanation of syntax
        # But in brief {at least, at most}, [inhereisvalid], # (?<=matchafterthis)
        matches = ['(?<=-cond) [A-Z a-z 0-9]*', 'b[0-9]p[0-9]{1,3}', '[0-9_]{1,3}[vV][0-9 hHzZ]{3,5}', 'ion[slrLR]',
                   '[0-9]{1,2}-[0-9]{1,2}-[0-9]{1,2}']
        params = ['Condition (Optional)', 'Notebook (Required)', 'Stimulation (Required)',
                  'Stimulation Kind (Required)', 'Date (Required)']
        for match, param in zip(matches, params):
            param_value = re.findall(match, self.load_file)
            try:
                param_value = param_value[0]
                if param == 'Stimulation (Required)':
                    param_value = param_value.replace('_', '.')
                elif param == 'Condition (Optional)':
                     param_value = param_value[1:]
                self.analysis_parameters[param].set(param_value)

            except IndexError:
                pass
        #intra_match = '(?<=-)[A-Z ]{2,30}(?=.*-|_)'
        #intra_cellulars = re.findall(intra_match, p)[0].split(' ')

    def add_more_condition_entries(self):
        """Add more conditions"""
        row = list(self.multiple_conditions_entry.keys())[np.argmax(list(self.multiple_conditions_entry.keys()))]
        row += 1
        self.multiple_conditions_entry[row] = [IntVar(), IntVar(), IntVar()]
        Entry(self.multi_cond_window, textvariable=self.multiple_conditions_entry[row][0]).grid(row=row, column=1)
        Entry(self.multi_cond_window, textvariable=self.multiple_conditions_entry[row][1]).grid(row=row, column=2)
        Entry(self.multi_cond_window, textvariable=self.multiple_conditions_entry[row][2]).grid(row=row, column=3)

    def multiple_conditions(self):
        self.multi_cond_window = tk.Toplevel(self.master)
        Button(self.multi_cond_window, text="Add More", command=self.add_more_condition_entries).grid(row=0, column=0)
        Label(self.multi_cond_window, text="Condition Label").grid(row=0, column=1, sticky='nsew')
        Label(self.multi_cond_window, text="Start Time").grid(row=0, column=2, sticky='nsew')
        Label(self.multi_cond_window, text="End Time").grid(row=0, column=3, sticky='nsew')
        for i in range(1,4):
            self.multiple_conditions_entry[i] = [StringVar(), StringVar(), StringVar()]
            Entry(self.multi_cond_window, textvariable=self.multiple_conditions_entry[i][0]).grid(row=i, column=1)
            Entry(self.multi_cond_window, textvariable=self.multiple_conditions_entry[i][1]).grid(row=i, column=2)
            Entry(self.multi_cond_window, textvariable=self.multiple_conditions_entry[i][2]).grid(row=i, column=3)
        Button(self.multi_cond_window, text="Finish", command=self.set_multiple_conditions).grid(row=0, column=4)

    def set_multiple_conditions(self):
        self.has_multiple_conditions = True
        data_page = self.controller.get_page("SelectChannelPage")
        self.channel_dict = data_page.channel_dict
        self.data = self.channel_dict['data']
        self.times = self.channel_dict['times']
        self.sr = self.channel_dict['sampling rate']

        for key in self.multiple_conditions_entry:
            _condition, _start, _stop = self.multiple_conditions_entry[key]
            condition = _condition.get()
            start = int(_start.get())
            stop = int(_stop.get())
        self.multi_cond_window.destroy()


class DataEntry(tk.Frame):
    """

    """
    __attrs__ = ('channel_dict', 'data', 'times', 'sr', 'channel', 'spikes_df', 'bursts_df',
                 'cid_remove', 'cid_add')
    def __init__(self, parent, controller):
        """

        :param parent:
        :param controller:
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.channel_dict = None
        self.data = None
        self.times = None
        self.sr = None
        self.channel = None
        self.spikes_df = None
        self.bursts_df = None
        self.toggle_add_spike_button = False
        self.toggle_del_spike_button = False
        self.cid_remove = None
        self.cid_add = None
        self.load_file = controller.load_file
        self.spike_sc = None

    def set_data(self):
        data_page = self.controller.get_page("SelectChannelPage")
        self.channel_dict = data_page.channel_dict
        self.data = self.channel_dict['data']
        self.times = self.channel_dict['times']
        self.sr = self.channel_dict['sampling rate']
        self.channel = data_page.channel

    def __detect_spikes(self):
        self.detect_spikes()


    def detect_spikes(self): # TODO: This really shouldn't be here
        #TODO: If a 'burst' only has 1 spike just remove that detected spike automatically
        data_page = self.controller.get_page("SelectChannelPage")
        data_page.select_channel()
        self.set_data()
        page = self.controller.get_page("ParameterEntryPage")
        minimum_isi = float(page.analysis_parameters['Required ISI (defaults at .01s)'].get())
        minimum_peak = float(page.analysis_parameters['Minimum Threshold (Required)'].get())
        try:
            maximum_peak = float(page.analysis_parameters['Maximum Threshold (Optional)'].get())
        except ValueError:
            if str(page.analysis_parameters['Maximum Threshold (Optional)'].get()).lower() == 'none':
                maximum_peak = None
        zscore_data = page.analysis_parameters_booleans['Use Z-score (defaults as False)'].get()
        find_troughs = page.analysis_parameters_booleans['Find Troughs (defaults as False)'].get()
        try:
            start_time = float(page.analysis_parameters['Start Time (Optional)'].get())
        except ValueError:
            if str(page.analysis_parameters['Start Time (Optional)'].get()).lower() == 'none':
                start_time = None
        try:
            end_time = float(page.analysis_parameters['End Time (Optional)'].get())
        except ValueError:
            if str(page.analysis_parameters['End Time (Optional)'].get()).lower() == 'none':
                end_time = None

        self.spikes_indices = find_spike_indices(data_dict=self.channel_dict, minimum_isi=minimum_isi,
                                                 minimum_peak=minimum_peak, maximum_peak=maximum_peak,
                                                 zscore_data=zscore_data, find_troughs=find_troughs,
                                                 start_time=start_time, end_time=end_time)

    def plot_detected_spikes(self):
        # This needs to be moved
        page = self.controller.get_page("TimeseriesPage")
        self.spike_sc = page.fig.axes[0].scatter(self.times[self.spikes_indices],
                                                 self.data[self.spikes_indices], color="#9b59b6", zorder=3)
        page.fig.canvas.draw()
        self.annot = page.fig.axes[0].annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                                      bbox=dict(boxstyle="round", fc="w"),
                                      arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)
        cid1 = page.fig.canvas.mpl_connect("motion_notify_event", self.hover)

    def plot_detected_bursts(self):
        # TODO: FIX ME
        page = self.controller.get_page("TimeseriesPage")
        for index, burst in self.bursts_df.iterrows():
            if burst['Burst Duration (s)'] == 0:
                continue
            start_of_burst = burst['Start of Burst (s)']
            end_of_burst = start_of_burst + burst['Burst Duration (s)']
            page.fig.axes[0].hlines(y=0, xmin=start_of_burst, xmax=end_of_burst, color='k', zorder=3)

        page.fig.canvas.draw_idle()
        print('Bursts should show up now', flush=True)

    def update_annot(self, ind):
        pos = self.spike_sc.get_offsets()[ind["ind"][0]]
        self.annot.xy = pos
        text = 'Spike {}'.format(" ".join(list(map(str, ind["ind"]))))
        self.annot.set_text(text)
        # annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
        self.annot.get_bbox_patch().set_alpha(0.4)

    def hover(self, event):
        page = self.controller.get_page("TimeseriesPage")
        vis = self.annot.get_visible()
        if event.inaxes != page.fig.axes[0]:
            return

        contained, index = self.spike_sc.contains(event)

        if contained:
            self.update_annot(index)
            self.annot.set_visible(True)
            page.fig.canvas.draw_idle()

        elif vis:
            self.annot.set_visible(False)
            page.fig.canvas.draw_idle()

    def save_pandas(self):
        # Save both the spikes df and the bursts df
        try:
            base_dir = '/Users/loganfickling/Downloads/' # This will throw an error for other users
            # TODO: This should probably ask where they want it saved
            #save_to = base_dir + self.load_file.split('/')[-2] + os.path.basename(self.load_file) + '/_{}_spikes_df.csv'

            save_to = base_dir + os.path.basename(self.load_file).split('.')[0] + '_{}_{}_spikes_df.csv'
            try: # TODO: FIX BELOW!!!
                neuron = self.spikes_df['Neuron'].iloc[0]
            except KeyError:
                neuron = 'LG'
                try:
                    print(self.spikes_df['Neuron'].loc[0], flush=True)
                except:
                    pass
            # TODO: Make sure the neuron is included in it... and do a check to make sure you don't over-write something that's already there
            # Maybe have it prompt a user dialog too
            save_to = save_to.replace('_export.smr', '').format(self.channel, neuron)

            if os.path.exists(save_to):
                print('Seems like there is already a file with this name, please choose a different name', flush=True)
                save_to = asksaveasfilename()

            self.spikes_df.to_csv(save_to, index=False)
            print('Made file {}'.format(save_to), flush=True)
            self.bursts_df = self.spikes_to_bursts()

            if os.path.exists(save_to.replace('_spikes_df', '_bursts_df')):
                print('Seems like there is already a file with this name, please choose a different name', flush=True)
                save_to = asksaveasfilename()

            self.bursts_df.to_csv(save_to.replace('_spikes_df', '_bursts_df'), index=False)
            print('Made file {}'.format(save_to.replace('_spikes_df', '_bursts_df')), flush=True)

        except AttributeError as e:
            self.create_pandas_df()
            self.save_pandas()

    def create_pandas_df(self):
        print('Creating pandas dataframes [line 895]')
        sr = self.channel_dict['sampling rate']
        page = self.controller.get_page("ParameterEntryPage")
        btw_brst_tol = float(page.analysis_parameters['Burst Tolerance (defaults at 2s)'].get())
        if self.spikes_indices is None:
            self.detect_spikes()
        #self.detect_spikes()
        # ---------> Make dataframe
        # Renaming variables for more clarity in code
        time_of_spike = self.times[self.spikes_indices]
        index_of_spike_in_samples = self.spikes_indices
        signal_value = self.data[self.spikes_indices]
        start_time = float(page.analysis_parameters['Start Time (Optional)'].get())  # Will initially be a str
        end_time = float(page.analysis_parameters['End Time (Optional)'].get())  # Will initially be a str

        print('This is the end time: ', end_time, flush=True)

        # Handling if they need the data spliced by start and end or not
        if (start_time == 'None' or start_time is None):
            start_time = self.times[0]
        else:
            print('type of times', type(self.times))
            print('type of start times: ', type(start_time))
            start_time = find_nearest(self.times, start_time, return_index_not_value=True)
            needs_slice = True
        if ((end_time == 'None') or (end_time is None)):
            end_time = self.times[-1]
        else:
            end_time = find_nearest(self.times, start_time, return_index_not_value=True)

        # Ordering of spike in each burst
        number_spike_in_each_burst = [len(x) for x in find_close_data(time_of_spike, btw_brst_tol)]
        # Ordering of burst number, relative order within a burst, # of spikes in burst
        bursts_num, spike_order_in_burst, spikes_in_burst = [], [], []
        for index, value in enumerate(number_spike_in_each_burst):
            bursts_num.append([index] * value)
            spike_order_in_burst.append(np.arange(value))
            spikes_in_burst.append([value] * value)
        bursts_num = np.concatenate(bursts_num)

        print('Printing burst number here?')
        print(bursts_num)

        x = np.arange(len(bursts_num))
        print('Printing x number here?')
        print(x)
        spike_order_in_burst = np.concatenate(spike_order_in_burst)
        spikes_in_burst = np.concatenate(spikes_in_burst)

        condition = [page.analysis_parameters['Condition (Optional)'].get()] * len(self.spikes_indices)
        # Check if the user has inputted multiple different conditions, if they have then ensure that the conditions
        # Match the corresponding time points
        page = self.controller.get_page("ParameterEntryPage")
        if page.has_multiple_conditions:
            _conds = []
            for key in page.multiple_conditions_entry:
                __condition, __start, __stop = page.multiple_conditions_entry[key]
                _condition = __condition.get()
                start = int(__start.get())
                stop = int(__stop.get())
                locs_valid = np.where((time_of_spike <= stop) & (time_of_spike >= start))[0]
                _conds.append([_condition for x in locs_valid])
            condition = np.concatenate(_conds)

        notebook = [page.analysis_parameters['Notebook (Required)'].get()] * len(self.spikes_indices)
        path = os.path.basename(self.load_file)
        isi = np.append(0, np.diff(time_of_spike))  # Interspike interval
        mask = np.where(np.append(0, np.diff(bursts_num))!=0)
        isi[mask] = np.nan # Set ISI from last spike of burst A to first spike of burst B as nan

        stim_kind = [page.analysis_parameters['Stimulation Kind (Required)'].get()] * len(self.spikes_indices)
        stim = [page.analysis_parameters['Stimulation (Required)'].get()] * len(self.spikes_indices)
        date = [page.analysis_parameters['Date (Required)'].get()] * len(self.spikes_indices)
        neuron = [page.analysis_parameters['Neuron (Required)'].get()] * len(self.spikes_indices)

        df = {"time": time_of_spike,
              "samples": index_of_spike_in_samples,
              "signal": signal_value,
              "isi": isi,  # put a nan or something at last spike in each burst
              "spike_number": spike_order_in_burst,
              "burst_order": bursts_num, # FIX HERE?
              "spikes_in_burst": spikes_in_burst,
              "path": [path] * len(self.spikes_indices),
              "stimulation_kind": stim_kind,
              'stimulation': stim,
              "stim_start": [start_time] * len(self.spikes_indices),
              "stim_end": [end_time] * len(self.spikes_indices),
              'date': date,
              "neuron": neuron,
              "condition": condition,
              "notebook" : notebook
              }

        try:
            self.spikes_df = pd.DataFrame(df)
        except ValueError as e:
            for x in df:
                print(x, len(df[x]))
        self.spikes_df['norm_spikes_in_burst'] = self.spikes_df['spike_number'] / self.spikes_df['spikes_in_burst']
        self.spikes_df = self.spikes_df[self.spikes_df['spikes_in_burst']>1]
        # Create the bursts df
        self.bursts_df = self.spikes_to_bursts()
        #self.plot_detected_bursts()
        return

    def show_burst_df(self):
        f = tk.Toplevel(self.master)
        f.grid()
        self.burst_table = pt = Table(f, dataframe=self.bursts_df, showtoolbar=True, showstatusbar=True)
        f.title('STG gui: Burst by Burst analysis')
        pt.show()

    def show_spike_df(self):
        f2 = tk.Toplevel(self.master)
        f2.grid()
        f2.title('STG gui: Spike by Spike analysis')
        self.spike_table = pt = Table(f2, dataframe=self.spikes_df, showtoolbar=True, showstatusbar=True)
        pt.show()

    def spikes_to_bursts(self):
        """

        :return:
        """
        # TODO: Make sure that this iterates correctly over the number of bursts
        spike_freqs, burst_durs, start_time = [], [], []

        for index, (burst_num, data) in enumerate(self.spikes_df.groupby('burst_order')):
            start_time.append(data.time.iloc[0])
            burst_duration = data.time.iloc[-1] - data.time.iloc[0]
            burst_durs.append(burst_duration)
            spike_freq = (data['spikes_in_burst'].iloc[0] - 1) / burst_duration # RuntimeWarning: invalid value encountered in true_divide
            spike_freqs.append(spike_freq)

        spike_numbers_per_burst = np.array(self.spikes_df.groupby('burst_order')['spikes_in_burst'].mean()) - 1
        cycle_periods = np.append(np.diff(start_time), np.nan)
        spike_freqs = np.array(spike_freqs)
        burst_durs = np.array(burst_durs)
        duty_cycle = (burst_durs / cycle_periods) * 100
        burst_orders = self.spikes_df['burst_order'].unique()
        print('Printing burst order in spikes_to_bursts line 1035')
        print(burst_orders)
        condition = np.array([self.spikes_df['condition'].unique()[0]] * len(burst_durs))
        date = np.array([self.spikes_df['date'].unique()[0]] * len(burst_durs))
        neuron = np.array([self.spikes_df['neuron'].unique()[0]] * len(burst_durs))
        path_arr = np.array([self.spikes_df['path'].iloc[0]] * len(burst_durs))
        times = np.array(self.spikes_df[self.spikes_df['spike_number']==0]['time'])
        dictionary = {'Burst Order': burst_orders,
                      'Burst Duration (s)': burst_durs,
                      '# of Spikes': spike_numbers_per_burst,
                      'Spike Frequency': spike_freqs,
                      'Cycle Period': cycle_periods,
                      'Duty Cycle': duty_cycle,
                      'Neuron': neuron,
                      'Condition': condition,
                      'Start of Burst (s)': times,
                      'path': path_arr,
                      'date': date}
        df = pd.DataFrame.from_dict(dictionary)
        df = df[df['Burst Duration (s)']>0]
        return df


class SpikeDetectionGUI(tk.Tk):
    """An object used to create a gui for Spike Analysis (in the Cancer Borealis Stomatagastric Nervous System)

    """

    # Frames to loop over
    _frames = (SelectChannelPage, TimeseriesPage, ParameterEntryPage, DataEntry)

    instance = None

    def __init__(self, provided_path = None, *args, **kwargs):
        """Creates an instance of the App for spike detection and analysis

        :param provided_path: optional, used to directly set a path rather than needing to click for it,  defaults None
        :param args: optional, used for __init__ tk.TK()
        :param kwargs: optional, used for __init__ tk.TK()
        """
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tk.font.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title('STG gui')
        # the container is where we'll stack a bunch of frames on top of each other, then the one we want visible
        # will be raised above the others
        self.container = tk.Frame(self, width=800, height=600)#width=1600, height=1600)
        self.container.grid(row=0, column=0)
        # Open the provided path if its given
        if provided_path is not None:
            if os.path.exists(provided_path):
                self.load_file = provided_path
            else:
                print('Path provided manually does not seem to be valid', flush=True)
                self.open_file()
        else:
            self.open_file()
        # Create a dictionary to hold the different pages for the gui
        self.frames = {}
        for F in SpikeDetectionGUI._frames:
            page_name = F.__name__
            frame = F(parent=self.container, controller=self) # This is initializing each relevant object
            self.frames[page_name] = frame
            # put all of the pages in the same location the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        if type(self).instance is None: # This stuff is used for when you want to do the loop through all the files
            type(self).instance = self # Initialization
        else:
            #raise RuntimeError("Only one instance of 'gui' can exist at a time")
            print('RuntimeError("Only one instance of gui can exist at a time")')
        self.show_frame("SelectChannelPage")

    @classmethod
    def reset(cls, provided_path=None, root=None):
        cls.instance = None  # First clear Foo.instance so that __init__ does not fail
        if root is None:
            root = Tk()
        cls.instance = SpikeDetectionGUI(provided_path=provided_path) # Foo
        return cls.instance

    def show_frame(self, page_name):
        """Show a frame for the given page name

        :param page_name:
        :return:
        """
        try:
            frame = self.frames[page_name]
            frame.tkraise()
        except KeyError: # If the frame hasn't been added it can't be shown, so add it it here
            self.add_frame(new_frame=str_to_class(page_name))
            self.show_frame(page_name=page_name)

    def add_frame(self, new_frame):
        """

        :param new_frame: Tk.Frame
        :return:
        """
        page_name = new_frame.__name__
        frame = new_frame(parent=self.container, controller=self)
        self.frames[page_name] = frame

    def get_page(self, page_class):
        try: # Try to return the frame
            return self.frames[page_class]

        except KeyError: # If it doesn't exist as a key, try to add it
            self.add_frame(new_frame=str_to_class(page_class))
            return self.frames[page_class]

    def open_file(self):
        """Launch a new window and prompt user to pick a file"""
        self.load_file = askopenfilename(initialdir="/Users/loganfickling/Downloads/",
                                         # That should still work even if the above folder doesn't work
                                         title="Please select your data file",
                                         filetypes=(("Spike2 files", "*.smr"), ("all files", "*.*"))
                                         )
        print('Loading file {}...'.format(self.load_file))
        return

if __name__ == "__main__": # The code below will only be run if the script is ran locally and not imported from
    #dir_name = '/Users/loganfickling/Downloads/Lingli_Data_Transferred/Data/05-22-07/'
    #f_name = 'b0p057-cond 2LPG killed-ions stim 3_6V 14hz-cogs off-LG PD LP_export.smr'
    dir_name = '/Users/loganfickling/Downloads/Actinonin/'
    f_name = '7_21_20_LF_b.smr'
    app = SpikeDetectionGUI(provided_path=dir_name + f_name)
    app.mainloop()
