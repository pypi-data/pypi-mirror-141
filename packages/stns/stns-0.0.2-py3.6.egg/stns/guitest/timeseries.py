from tkinter import StringVar, OptionMenu, IntVar
import tkinter as tk
from tkinter.ttk import Button, Entry, Label, OptionMenu
import numpy as np
from matplotlib.figure import Figure
from scipy.stats import zscore
from matplotlib.widgets import Slider, RectangleSelector
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from copy import deepcopy
import seaborn as sns
from functools import partial

"""TODO: change it so that the indexing of each burst resets"""


__all__ = ['TimeseriesPage']


class TimeseriesPage(tk.Frame):
    """
    """

    def __init__(self, parent, controller):
        """

        :param parent:
        :param controller:
        """
        tk.Frame.__init__(self, parent)
        # self.create_adjust_y_axis_window = None
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
        self.data = None
        self._data = None
        self.x_axis_step = IntVar(value=50)
        self.y_axis_entry = {v: StringVar() for v in ['maximum y', 'minimum y']}
        self.canvas = None
        self.y_mins = {}
        self.y_maxs = {}
        self.x_axis_n_ticks = IntVar(value=5)
        self.y_axis_n_ticks = IntVar(value=5)
        self._added_lines = []

    def apply_zscore(self):  # Move
        #if not hasattr(self, 'data'):
            #self.set_data()
        if self.data is None:
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
        try:
            self.add_plot()
        except AttributeError as e:
            print(e)

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
        if not hasattr(self, 'data'):  # TODO: Under which conditions does this need to be done?
            print('Setting data....')
            self.set_data()
        n_ticks = self.x_axis_n_ticks.get()

        for i, ax in enumerate(self.fig.axes):
            if i + 1 == len(self.fig.axes):
                break
            start, end = ax.get_xlim()
            if start - end != self.x_axis_step.get():
                # TODO: Need to change this so that the slider doesn't limit the x-range
                # Change the xaxis in the matplotlib figure
                ax.set_xlim(start, start + self.x_axis_step.get())
                ax.xaxis.set_ticks(np.arange(start, start + self.x_axis_step.get(), self.x_axis_step.get() / n_ticks))
        self.fig.canvas.draw()
        self.x_axis_window.destroy()

    def create_adjust_y_axis_window(self):
        """Creates a new window to adjust the y-axis"""
        self.y_axis_window = tk.Toplevel(self.master)
        for k, v in enumerate(self.y_axis_entry):
            Label(self.y_axis_window, text="{} =".format(v)).grid(row=k, column=0)
            Entry(self.y_axis_window, textvariable=self.y_axis_entry[v]).grid(row=k, column=1)
        Button(self.y_axis_window, text="Update", command=self.update_y_axis).grid(row=3, column=1)

        # Make sure you know for which channel
        page = self.controller.get_page("SelectChannelPage")
        # channels_available = page.get_channel_names()
        Label(self.y_axis_window, text='Change number of ticks').grid(row=2, column=0)
        Entry(self.y_axis_window, textvariable=self.y_axis_n_ticks).grid(row=2, column=1)
        self.yaxis_channel_drop_down = StringVar(master=self.y_axis_window, value="Select A Channel")
        # self.yaxis_channel_section = OptionMenu(self.y_axis_window, self.yaxis_channel_drop_down, *channels_available)

        self.yaxis_channel_section = OptionMenu(self.y_axis_window, self.yaxis_channel_drop_down,
                                                *page.visible_channels)
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
        index = [i for i, channel in enumerate(page.visible_channels) if channel == yaxis_ch_selection][0]
        # TODO: This will fail if user inputs multiple of same channel
        self.fig.axes[index].set_ylim(y_min, y_max)
        # self.fig.axes[index].yaxis.set_ticks(np.arange(y_min, y_max, (y_max-y_min) / self.y_axis_n_ticks.get()))
        self.fig.axes[index].yaxis.set_ticks(
            np.arange(y_min, y_max, (y_max - y_min) / float(self.y_axis_n_ticks.get())))
        self.fig.canvas.draw()
        self.y_axis_window.destroy()
        return

    def set_data(self):
        page = self.controller.get_page("SelectChannelPage")
        self.channel = page.channel
        self.data = page.data
        self.times = page.times

    def add_channel(self):
        """TODO Move to selectchannel.py?"""
        self.add_ch_window = tk.Toplevel(self.master)
        page = self.controller.get_page("SelectChannelPage")
        channels_available = page.channels_available
        self.channel_drop_down = StringVar(master=self.add_ch_window, value="Select A Channel")
        # Create drop down menu for loading channels and buttons to click for plotting and analysis parameter entry
        # The *self.channels_available means extract elements of this list (self.channels_available being the list)
        self.second_ch_selection = OptionMenu(self.add_ch_window, self.channel_drop_down, *channels_available)
        self.second_ch_selection.grid(row=1, column=0, sticky='nswe')
        Button(self.add_ch_window, text="Add Channel", command=self._add_plot).grid(row=2, column=0)

    def make_plot_buttons(self):
        # Buttons for various changing of view for graph
        b0 = Button(self.master, text="Reset Slider", command=self.reset_slider)
        b0.grid(row=1, column=1, sticky='nsew')
        b1 = Button(self.master, text="Adjust y-axis", command=self.create_adjust_y_axis_window)
        b1.grid(row=2, column=1, sticky='nsew')
        b2 = Button(self.master, text="Adjust x-axis", command=self.create_adjust_x_axis_window)
        b2.grid(row=3, column=1, sticky='nsew')
        b3 = Button(self.master, text="Z-score Data", command=self.apply_zscore)
        b3.grid(row=4, column=1, sticky='nsew')
        # TODO: Burst analysis as b9
        b4 = Button(self.master, text="Toggle Add Spikes With Right Click", command=self.toggle_add_spike)
        b4.grid(row=2, column=2, sticky='nsew')
        b5 = Button(self.master, text="Add Another Channel", command=self.add_channel)
        b5.grid(row=4, column=0, sticky='nsew')
        #b6 = Button(self.master, text="Toggle Add Spikes With Right Click", command=self.toggle_add_spike)
        #b6.grid(row=2, column=2, sticky='nsew')
        b7 = Button(self.master, text='Toggle Remove Spikes with Right Click', command=self.toggle_remove_spike)
        b7.grid(row=3, column=2, sticky='nsew')
        b8 = Button(self.master, text='Toggle Remove Spikes Hold and Drag', command=self.toggle_rect)
        b8.grid(row=4, column=2, sticky='nsew')
        #Button(self.master, text='Toggle Add Burst Duration Hold and Drag', command=self.rectangle_add_line).grid(
            #row=5, column=2, sticky='nsew')

    def rectangle_add_line(self, eclick, erelease):
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        if x2 <= x1:
            return
        #print("Added line (%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
        #print("The button you used were: %s %s" % (eclick.button, erelease.button))
        if ((eclick.inaxes != self.fig.axes[0]) or (eclick.button != 3)):
            return #  Ensures that they right click within the figure's axis

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
            return # TODO WHy do this way???
        print("Removed Spikes between %3.2f--> %3.2f" % (x1, x2))
        #print(" The button you used were: %s %s" % (eclick.button, erelease.button))
        if ((eclick.inaxes != self.fig.axes[0]) or (eclick.button != 3)):
            return

        page = self.controller.get_page("DataEntry")
        try:
            offsets = page.spike_sc.get_offsets()
        except AttributeError:  # If click before spikes are detected
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
        # TODO This is badly named change it
        channel = self.channel_drop_down.get()
        page = self.controller.get_page("SelectChannelPage")
        if channel not in page.visible_channels:
            print('channel {} not in the visible channels {} appending'.format(channel, page.visible_channels))
            page.visible_channels.append(channel)
        #assert(channel in page.visible_channels)
        self.add_plot()

    def add_plot(self):
        self.destroy_canvas()
        page = self.controller.get_page("SelectChannelPage")
        self.make_plot_buttons()

        self.fig = Figure(figsize=(10, 5), dpi=100)
        colors = sns.color_palette("colorblind", n_colors=len(page.visible_channels))
        print('in add plot: visible channels: ', page.visible_channels)

        for i, ch in enumerate(page.visible_channels):
            page.set_channel_data(channel_name=ch)
            self.axes = self.fig.add_subplot(len(page.visible_channels), 1, i + 1)  # row, col, index; mpl syntax
            self.axes.plot(page.times, page.data, color=colors[i]) # Plot the waveform

            if i == len(page.visible_channels) - 1: # Only need this on the bottom graph
                self.axes.set_xlabel('Time (s)', fontsize=16)

            self.axes.set_ylabel('{}\nVoltage (μV)'.format(ch), fontsize=16)
            self.axes.tick_params(axis='y', which='both', labelsize=12)
            # TODO: Make it check that this isn't already set?
            self.y_mins[ch] = np.min(page.data)
            self.y_maxs[ch] = np.max(page.data)
            self.axes.axis([page.times[0], page.times[0] + int(self.x_axis_step.get()),
                            float(self.y_mins[ch]), float(self.y_maxs[ch])])  # [xmin, xmax, ymin, ymax]
            self.axes.yaxis.set_ticks(np.arange(self.y_mins[ch],
                                                self.y_maxs[ch],
                                                (self.y_maxs[ch] - self.y_mins[ch]) / self.y_axis_n_ticks.get()))
            command_w_args = partial(self.delete_channel, ch)  # partial() is done to insert an arg to a function
            b1 = Button(self.master, text="Delete Channel", command=command_w_args)
            b1.grid(row=i, column=4, sticky='nw')

        # This needs to be done in order to set the first plot done as the active one
        #print('TS line280: ', page.visible_channels)
        page.set_channel_data(channel_name=page.visible_channels[0])

        self.canvas = FigureCanvasTkAgg(self.fig, self.master)
        self.canvas.draw()
        # Create Slider object to change time value  [Left Bottom width height]
        self.axpos = self.fig.add_axes([0.12, 0.1, 0.75, 0.05], facecolor="#3498db")  # '#00A08A')
        self.spos = Slider(ax=self.axpos, label='', valmin=page.times[0],
                           valmax=page.times[-1] - int(self.x_axis_step.get()))  # , color="#FF0000")

        def update_xaxis(val):
            """Throw-away function that updates when the slider is moved"""
            pos = self.spos.val
            for i, ax in enumerate(self.fig.axes):
                _channel = page.visible_channels[i]
                self.fig.axes[i].axis([pos, pos + int(self.x_axis_step.get()),
                                       float(self.y_mins[_channel]), float(self.y_maxs[_channel])])
                self.fig.axes[i].xaxis.set_ticks(np.arange(pos, pos + self.x_axis_step.get(),
                                                           self.x_axis_step.get() / self.x_axis_n_ticks.get()))
                if i == (len(
                        self.fig.axes) - 2):  # Should have n plots + 1 axes, the +1 being from the self.axpos slider
                    break  # Want it to end after finishing the second to last axis and not include the slider
            self.fig.canvas.draw_idle()

        self.spos.on_changed(update_xaxis)  #  Whenever the position of the slider changes make it update
        self.canvas.draw_idle()
        self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=4, sticky='nesw')

        data_page = self.controller.get_page("DataEntry")

        if data_page.spike_sc is not None:  # This way we skip this part when initially plotting the signal
            data_page.plot_detected_spikes()

    def delete_channel(self, channel):
        page = self.controller.get_page("SelectChannelPage")
        print('User Pressed Delete Channel {}'.format(channel))
        page.visible_channels.remove(channel)
        self.add_plot()

    def add_spike_onclick(self, event):
        if (event.inaxes != self.fig.axes[0]) or (event.button != 3):
            return
        page = self.controller.get_page("DataEntry")
        try:
            offsets = page.spike_sc.get_offsets()
        except AttributeError:
            # This is when the use tries to click it before the data is set
            print('Please detect spikes first')
            return

        new_xydata = np.insert(offsets, 0, [event.xdata, event.ydata], axis=0) # Insert clicked point
        new_xydata = new_xydata[np.argsort(new_xydata[:, 0])]  # Sort based on x-axis values
        page.spike_sc.set_offsets(new_xydata)  # Add x and y data
        self.fig.canvas.draw_idle()
        return

    def remove_spike_onclick(self, event):
        if ((event.inaxes != self.fig.axes[0]) or (event.button != 3)):
            return
        page = self.controller.get_page("DataEntry")
        try:
            offsets = page.spike_sc.get_offsets()
        except AttributeError:
            # This is when the use tries to click it before the data is set
            print('Please detect spikes first', flush=True)
            return
        xdata = offsets[:, 0]
        xdata_click = event.xdata  # X position in values for mouse click
        xdata_nearest_index = (np.abs(xdata - xdata_click)).argmin()  # Closest index value to mouse click
        new_xydata = np.delete(offsets, np.where(xdata == xdata[xdata_nearest_index]), axis=0)  # Remove xdata
        print('timeseries.py line 348: old offsets of dataentry', len(page.spike_sc.get_offsets()))

        page.spike_sc.set_offsets(new_xydata)  # update scatter plot
        print('timeseries.py line 351: new offsets of dataentry', len(page.spike_sc.get_offsets()))
        self.fig.canvas.draw_idle()
        print('Spike removed')
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
        self.RS = RectangleSelector(ax=self.fig.axes[0],  # onselect=self.rectangle_add_line,
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

    def toggle_add_spike(self):
        self.disconnect_remove_spike() # Done so you can't add + remove at the same time

        if self.toggle_add_spike_button:
            self.connect_add_spike()
            print('Right Click to Add a Spike', flush=True)
            self.toggle_add_spike_button = False

        else:
            self.disconnect_add_spike()
            print('Stopped Adding Spikes', flush=True)
            self.toggle_add_spike_button = True

    def connect_add_spike(self):
        self.cid_add = self.fig.canvas.mpl_connect('button_press_event', self.add_spike_onclick)

    def disconnect_add_spike(self):
        if self.cid_add is None:
            return
        self.fig.canvas.mpl_disconnect(self.cid_add)

    def toggle_remove_spike(self):
        if self.toggle_del_spike_button:
            self.connect_remove_spike()
            print('Right Click to Remove a Spike', flush=True)
            self.toggle_del_spike_button = False
        else:
            self.disconnect_remove_spike()
            print('Removing Spikes Disabled', flush=True)
            self.toggle_del_spike_button = True

    def connect_remove_spike(self):
        self.cid_remove = self.fig.canvas.mpl_connect('button_press_event', self.remove_spike_onclick)

    def disconnect_remove_spike(self):
        if self.cid_remove is None:
            return
        self.fig.canvas.mpl_disconnect(self.cid_remove)

    """
    def plot_detected_bursts(self):
        # TODO This obviously should be in the timeseriespage
        page = self.controller.get_page("TimeseriesPage")
        for index, burst in self.bursts_df.iterrows():
            if burst['Burst Duration (s)'] == 0:
                continue
            start_of_burst = burst['Start of Burst (s)']
            end_of_burst = start_of_burst + burst['Burst Duration (s)']
            # Plot bursts by adjusting local maxima by 20%
            value = self.find_local_maxima(start=start_of_burst, end=end_of_burst)
            if value < 0:
                value *= .8
            elif value >= 0:
                value *= 1.2

            page.fig.axes[0].hlines(y=value, xmin=start_of_burst, xmax=end_of_burst, color='k', zorder=3, lw=4)
            page.fig.axes[0].text(end_of_burst, value, 'Burst #{}'.format(index), ha='left', va='center_baseline',
                                  zorder=4, color='#0339f8', size=12)

        page.fig.canvas.draw_idle()
        print('Bursts should show up now', flush=True)
        
        
        
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
        """



