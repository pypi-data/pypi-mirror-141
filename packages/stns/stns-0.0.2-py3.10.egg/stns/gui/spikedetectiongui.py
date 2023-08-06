"""
BUG: Unclear how this exactly happens but when adjusting the x-axis to a smaller value then readjusting it back up
the data can appear to be clipped

TODONE: Need to make some button to allow for user to refresh the burst calculation after they've manually removed and added spikes
TODONE: Add in burst line finish to some kind of output
TODONE: Have a check to ensure that the burst lines will be included inside the view, often times it's outside of it.
TODO: Make buttons appear pressed in or something and auto-toggle so only one remove/add spikes method is on at a time
TODO: For the parameter entry thing it really should just be a drop-down to pick which neuron it wants
TODO: Increase the figure sie if more than 2 channels are plotted, try to keep the same dimensions as shown w/ 2 chs
TODO: Make it so that y-axis "state" is remembered and assigned w/ each ch. (change visible_channels to a dict?)
TODO: Allow a user to define a total unit length parameter?

TODO: make it so when a spike is removed, check if there's a burst and if all the spikes in the burst are gone, remove it
TODO BUG: x-axis crash when decimal <.5
File "/Users/loganfickling/stns/stns/gui/timeseries.py", line 103, in update_x_axis
    ax.xaxis.set_ticks(np.arange(start, start + self.x_axis_step.get(), self.x_axis_step.get() / n_ticks))
ValueError: arange: cannot compute length

"""

from tkinter import Tk
import tkinter as tk
import os
from tkinter.filedialog import askopenfilename
from stns.gui import (SelectChannelPage, TimeseriesPage, ParameterEntryPage, DataEntry)
from matplotlib import rcParams, use
import seaborn as sns
import sys

# Matplotlib
use("TkAgg")
rcParams['agg.path.chunksize'] = 10000 #  Fixes OverflowError: In draw_path: Exceeded cell block limit
sns.set(context='paper', style='darkgrid', palette='colorblind')
LARGE_FONT= ("Verdana", 12)

__all__ = ['SpikeDetectionGUI', 'str_to_class']

# Utility functions
def str_to_class(classname):
    """Returns the given object in namespace when given a string input of the obect's name

    :param classname: str, object.__main__, e.g. 'Cat' -> class Cat
    :return:
    """
    return getattr(sys.modules[__name__], classname)

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
            print('RuntimeError("Only one instance of gui can exist at a time")')
            #self.reset()

    @classmethod
    def reset(cls, provided_path=None, root=None):
        cls.instance = None  # First clear Foo.instance so that __init__ does not fail
        if root is None:
            root = Tk()
        cls.instance = SpikeDetectionGUI(provided_path=provided_path, master=root) # Foo
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


if __name__ == '__main__':
    from glob import glob
    import gc
    #file_names = sorted(glob('/Users/loganfickling/Desktop/Nusbaum Lab/*/Lingli exported data/05-12*/*.smr'))
    #for file_name in file_names:
    file_names = sorted(glob('/Users/loganfickling/Downloads/Hemo*/11-23*/incub*/*.smr'))#[0]
    for file_name in file_names:
        print('Starting file {}'.format(file_name), flush=True)
        app = SpikeDetectionGUI(provided_path=file_name)
        app.mainloop()
        #del app
        #gc.collect()
        #print('hello')

