import tkinter as tk
import numpy as np
import pandas as pd
import os
from stns.detect import find_close_data, find_spike_indices, find_nearest
from tkinter.filedialog import asksaveasfilename
from pandastable import Table
from tkinter.ttk import Button

__all__ = ['DataEntry']

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
        self.spikes_have_been_plotted = False

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
        # LOGAN EDITTING HERE 2-17-22

        #if self.spike_sc is None:
        self.spikes_indices = find_spike_indices(data_dict=self.channel_dict, minimum_isi=minimum_isi,
                                                 minimum_peak=minimum_peak, maximum_peak=maximum_peak,
                                                 zscore_data=zscore_data, find_troughs=find_troughs,
                                                 start_time=start_time, end_time=end_time)

        #else:
        #    self.spikes_indices = self.spike_sc.get_offsets()[:,0]


    def add_buttons(self):
        b0 = Button(self.master, text='Make DataFrames', command=self.create_pandas_df)
        b0.grid(row=2, column=3, sticky='nsew')
        b1 = Button(self.master, text='Save DataFrames', command=self.save_pandas)
        b1.grid(row=3, column=3, sticky='nsew')
        b2 = Button(self.master, text='Show Data by Bursts', command=self.show_burst_df)
        b2.grid(row=4, column=3, sticky='nsew')
        b3 = Button(self.master, text='Show Data by Spikes', command=self.show_spike_df)
        b3.grid(row=5, column=3, sticky='nsew')

    def plot_detected_spikes(self):
        # This needs to be moved
        page = self.controller.get_page("TimeseriesPage")
        if self.spike_sc is not None:
            print('Spikes have already been detected!')
            # Need to erase previous spikes here
            #self.spike_sc.set_offsets(new_xydata)  # update scatter plot
            self.spike_sc.remove()
            page.fig.canvas.draw_idle()

        self.spike_sc = page.fig.axes[0].scatter(self.times[self.spikes_indices],
                                                 self.data[self.spikes_indices],
                                                 color="#9b59b6", zorder=3, marker="2", s=150)
        page.fig.canvas.draw()
        self.annot = page.fig.axes[0].annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                                      bbox=dict(boxstyle="round", fc="w"),
                                      arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)
        cid1 = page.fig.canvas.mpl_connect("motion_notify_event", self.hover)

    def find_local_maxima(self, start, end):
        section = self.data[(self.times>start) & (self.times<end)]
        return np.max(section)

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

            # Create horizontal lines at each determined burst, label the righthand side with the burst number
            page.fig.axes[0].hlines(y=value, xmin=start_of_burst, xmax=end_of_burst, color='k', zorder=3, lw=4)
            page.fig.axes[0].text(end_of_burst, value, 'Burst #{}'.format(index), ha='left', va='center_baseline',
                                  zorder=4, color='#0339f8', size=12) #  bbox = dict(boxstyle="round", fc="b")
        page.fig.canvas.draw_idle()  # Update figure
        print('Bursts should show up now', flush=True)

    def update_spike_annot(self, ind):
        # ex variable ind:  {'ind': array([20, 21, 22, 23, 24], dtype=int32)}
        index = ind["ind"]
        relative_spike_number = self.spikes_df['spike_number'].iloc[index[-1]]

        position = self.spike_sc.get_offsets()[ind["ind"][0]]
        self.annot.xy = position
        text = f"Spike {relative_spike_number} in burst, \nSpike {index[-1]} total "
        self.annot.set_text(text)
        self.annot.get_bbox_patch().set_alpha(0.4)


    def hover(self, event):
        page = self.controller.get_page("TimeseriesPage")
        vis = self.annot.get_visible()
        if event.inaxes != page.fig.axes[0]:
            return
        contained, index = self.spike_sc.contains(event)

        if contained:
            self.update_spike_annot(index)
            self.annot.set_visible(True)
        elif vis:
            self.annot.set_visible(False)

        page.fig.canvas.draw_idle()

    def save_pandas(self):
        # Save both the spikes df and the bursts df
        try:
            base_dir = '/Users/loganfickling/Downloads/' # This will throw an error for other users, maybe default to cwd
            # TODO: This should probably ask where they want it saved
            save_to = base_dir + os.path.basename(self.load_file).split('.')[0] + '_{}_{}_spikes_df.csv'
            page = self.controller.get_page("ParameterEntryPage")
            neuron = page.analysis_parameters['Neuron (Required)']
            # TODO: Make sure the neuron is included in it... and do a check to make sure you don't over-write something that's already there
            # Maybe have it prompt a user dialog too
            save_to = save_to.replace('_export.smr', '').format(self.channel, neuron)

            if os.path.exists(save_to):
                print('Seems like there is already a file with this name, please choose a different name', flush=True)
                save_to = asksaveasfilename()

            self.spikes_df.to_csv(save_to, index=False)
            print('Made file {}'.format(save_to), flush=True)
            #self.bursts_df = self.spikes_to_bursts() # REMOVING

            if os.path.exists(save_to.replace('_spikes_df', '_bursts_df')):
                print('Seems like there is already a file with this name, please choose a different name', flush=True)
                save_to = asksaveasfilename()

            self.bursts_df.to_csv(save_to.replace('_spikes_df', '_bursts_df'), index=False)
            print('Made file {}'.format(save_to.replace('_spikes_df', '_bursts_df')), flush=True)

        except AttributeError as e:
            print(e)
            self.create_pandas_df()
            self.save_pandas()

    def create_pandas_df(self):
        print('Creating pandas dataframes dataentry.py line 201')
        page = self.controller.get_page("ParameterEntryPage")
        btw_brst_tol = float(page.analysis_parameters['Burst Tolerance (defaults at 2s)'].get())
        if self.spikes_indices is None:
            print('No spike indicies, detecting spikes')
            self.detect_spikes()

        # ---------> Make dataframe
        # Renaming variables for more clarity in code
        try:
            time_of_spike = self.times[self.spike_sc.get_offsets()[:,0]]
        except Exception as e:
            print(e)
            time_of_spike = self.spike_sc.get_offsets()[:,0]
        index_of_spike_in_samples = self.spike_sc.get_offsets()[:,0]
        signal_value = self.spike_sc.get_offsets()[:,1]

        try:
            start_time = float(page.analysis_parameters['Start Time (Optional)'].get())  # Will initially be a str
            end_time = float(page.analysis_parameters['End Time (Optional)'].get())  # Will initially be a str
        except ValueError: # If it has a value of None then the string to float conversion will fail with this error
            start_time = self.times[0]
            end_time = self.times[-1]

        # Ordering of spike in each burst
        number_spike_in_each_burst = [len(x) for x in find_close_data(time_of_spike, btw_brst_tol)]
        # Ordering of burst number, relative order within a burst, # of spikes in burst
        bursts_num, spike_order_in_burst, spikes_in_burst = [], [], []
        for index, value in enumerate(number_spike_in_each_burst):
            bursts_num.append([index] * value)
            spike_order_in_burst.append(np.arange(value))
            spikes_in_burst.append([value] * value)
        bursts_num = np.concatenate(bursts_num)
        spike_order_in_burst = np.concatenate(spike_order_in_burst)
        spikes_in_burst = np.concatenate(spikes_in_burst)

        condition = [page.analysis_parameters['Condition (Optional)'].get()] * len(time_of_spike)
        # Check if user inputted multiple different conditions, if they have then ensure they match the time points
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

        notebook = [page.analysis_parameters['Notebook (Required)'].get()] * len(time_of_spike)
        path = os.path.basename(self.load_file)
        isi = np.append(0, np.diff(time_of_spike))  # Interspike interval
        mask = np.where(np.append(0, np.diff(bursts_num))!=0)
        isi[mask] = np.nan # Set ISI from last spike of burst A to first spike of burst B as nan
        stim_kind = [page.analysis_parameters['Stimulation Kind (Required)'].get()] * len(time_of_spike)
        stim = [page.analysis_parameters['Stimulation (Required)'].get()] * len(time_of_spike)
        date = [page.analysis_parameters['Date (Required)'].get()] * len(time_of_spike)
        neuron = [page.analysis_parameters['Neuron (Required)'].get()] * len(time_of_spike)

        df = {"time": time_of_spike, "samples": index_of_spike_in_samples, "signal": signal_value, "isi": isi,
              "spike_number": spike_order_in_burst, "burst_order": bursts_num, "spikes_in_burst": spikes_in_burst,
              "path": [path] * len(time_of_spike),
              "stimulation_kind": stim_kind, 'stimulation': stim,
              "stim_start": [start_time] * len(time_of_spike),
              "stim_end": [end_time] * len(time_of_spike),
              'date': date, "neuron": neuron, "condition": condition, "notebook" : notebook }
        try:
            self.spikes_df = pd.DataFrame(df)

        except ValueError as e:
            for x in df:
                print(x, len(df[x]))
            print(e)

        self.spikes_df['norm_spikes_in_burst'] = self.spikes_df['spike_number'] / self.spikes_df['spikes_in_burst']
        self.spikes_df = self.spikes_df[self.spikes_df['spikes_in_burst']>1]
        # Create the bursts df
        self.bursts_df = self.spikes_to_bursts()

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
        spike_freqs, burst_durs, start_time = [], [], []

        for index, (burst_num, data) in enumerate(self.spikes_df.groupby('burst_order')):
            start_time.append(data.time.iloc[0])
            burst_duration = data.time.iloc[-1] - data.time.iloc[0]
            burst_durs.append(burst_duration)
            spike_freq = (data['spikes_in_burst'].iloc[0] - 1) / burst_duration # RuntimeWarning: invalid value encountered in true_divide
            spike_freqs.append(spike_freq)

        # Create variables to store various excel column values
        spike_numbers_per_burst = np.array(self.spikes_df.groupby('burst_order')['spikes_in_burst'].mean()) - 1
        cycle_periods = np.append(np.diff(start_time), np.nan)
        spike_freqs = np.array(spike_freqs)
        burst_durs = np.array(burst_durs)
        duty_cycle = (burst_durs / cycle_periods) * 100
        burst_orders = self.spikes_df['burst_order'].unique()
        condition = np.array([self.spikes_df['condition'].unique()[0]] * len(burst_durs))
        date = np.array([self.spikes_df['date'].unique()[0]] * len(burst_durs))
        neuron = np.array([self.spikes_df['neuron'].unique()[0]] * len(burst_durs))
        path_arr = np.array([self.spikes_df['path'].iloc[0]] * len(burst_durs))
        times = np.array(self.spikes_df[self.spikes_df['spike_number']==0]['time'])
        dictionary = {'Burst Order': np.arange(len(burst_orders)),
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
        #print(df['Burst Order'])
        return df