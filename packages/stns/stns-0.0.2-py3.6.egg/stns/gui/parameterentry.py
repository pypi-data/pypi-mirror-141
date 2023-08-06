from tkinter import StringVar, IntVar, BooleanVar
import tkinter as tk
from tkinter.ttk import Button, Checkbutton, Entry, Label
import numpy as np
import re

__all__ =['ParameterEntryPage']


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
        page.add_buttons()
        self.analysis_parameter_window.destroy()

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
        self.multiple_conditions_entry[row] = [StringVar(), IntVar(), IntVar()]
        Entry(self.multi_cond_window, textvariable=self.multiple_conditions_entry[row][0]).grid(row=row, column=1)
        Entry(self.multi_cond_window, textvariable=self.multiple_conditions_entry[row][1]).grid(row=row, column=2)
        Entry(self.multi_cond_window, textvariable=self.multiple_conditions_entry[row][2]).grid(row=row, column=3)

    def multiple_conditions(self):
        self.multi_cond_window = tk.Toplevel(self.master)
        Button(self.multi_cond_window, text="Add More", command=self.add_more_condition_entries).grid(row=0, column=0)
        Label(self.multi_cond_window, text="Condition Label").grid(row=0, column=1, sticky='nsew')
        Label(self.multi_cond_window, text="Start Time").grid(row=0, column=2, sticky='nsew')
        Label(self.multi_cond_window, text="End Time").grid(row=0, column=3, sticky='nsew')
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
            start = int(_start.get()) # TODO: Change so that ValueError: invalid literal for int() with base 10: ''
            stop = int(_stop.get())
        self.multi_cond_window.destroy()

