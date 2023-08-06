from collections.abc import Sequence
from matplotlib import pyplot as plt
import seaborn as sns
import matplotlib as mpl
from matplotlib import rc
import pandas as pd
import numpy as np

__all__ = ['condition_line_plot', 'condition_violin_plot', 'elapsed_time_scatter_plot',
           'paired_plots', 'max_burst_number', "condition_scatter_plot", "condition_plot"]

# TODO: This needs to be documented
__default_y = ['Burst Duration (sec)',
              '# of Spikes',
              'Spike Frequency (Hz)',
              'Instantaneous Period (sec)',
              'Interburst Duration (s)',#'Instantaneous Frequency (Hz)',
              'Duty Cycle']


def condition_line_plot(dataframe, cols=None, Neuron='LG', title=''):
    """Return a condition line plot for the dataframe

    :param dataframe: pd.Dataframe, must have a column Condition
    :param cols: list of str, relevant columns in the data frame
    :param Neuron: str,
    :param title: str,
    :return:
    """
   # if type(cols)==list:
       #cols = cols

    if cols is None:
        cols = __default_y

    fig, axis = plt.subplots(nrows=2, ncols=len(cols)//2, figsize=(16,8))

    if not isinstance(cols, Sequence):
        raise TypeError('cols must be a sequence (either a list or an array)')

    
    if Neuron.lower() != 'all':
        try:
            dataframe = dataframe[dataframe['Neuron']==Neuron]

        except KeyError:
            print('key error happens')
            pass
        except IndexError:
            print('index error happens')
            pass

    for index, ax in enumerate(axis.ravel()):
        # Make the plot
        g = sns.pointplot(x="Condition", 
                          y=cols[index],
                          hue="Neuron",
                          capsize=.2, 
                          palette="YlGnBu_d", 
                          kind="point", 
                          data=dataframe, 
                          ax=ax)
        
        # Set Title, y-axis, x-axis values
        ax.set_title(title, fontsize=20)
        ax.set_ylabel(cols[index], fontsize=16)
        ax.set_xlabel("Condition", fontsize=16)
    
    # Make it look pretty
    rc('ytick', labelsize=16) # matplotlib
    rc('xtick', labelsize=16)
    plt.tight_layout()
    plt.subplots_adjust(hspace=.6)
    plt.show()
    return fig, ax

def condition_violin_plot(dataframe, cols=None, Neuron='all', title='', scale='area'):

    if cols is None:
        cols = __default_y

    fig, axis = plt.subplots(nrows=2, ncols=len(cols)//2, figsize=(16,8))


    if not isinstance(cols, Sequence):
        raise TypeError('cols must be a sequence (either a list or an array)')
    
    if Neuron.lower() != 'all':
        dataframe = dataframe[dataframe['Neuron']==Neuron]

    for index, ax in enumerate(axis.ravel()):
        # Make the plot
        g = sns.violinplot(x='Condition',
                           y=cols[index],
                           data=dataframe,
                           hue='Neuron',
                           scale_hue=False,
                           inner='quartile',
                           scale=scale,
                           split=False,
                           ax=ax,
                           bw='scott',
                           palette='husl',
                           cut=0)

        # Set Title, y-axis, x-axis values
        ax.set_title(title, fontsize=20)
        ax.set_ylabel(cols[index], fontsize=16)
        ax.set_xlabel("Condition", fontsize=16)

    # Make it look pretty
    rc('ytick', labelsize=16)
    rc('xtick', labelsize=16)
    plt.tight_layout()
    #plt.subplots_adjust(hspace=.6)
    #plt.show()
    return fig, ax


def elapsed_time_scatter_plot(dataframe, cols=None, Neuron='LG', title=''):

    if cols is None:
        cols = __default_y
    fig, axis = plt.subplots(nrows=2, ncols=len(cols) // 2, figsize=(16, 8))

    if not isinstance(cols, Sequence):
        raise TypeError('cols must be a sequence (either a list or an array)')
        
    if Neuron != 'all':
        dataframe = dataframe[dataframe['Neuron']==Neuron]

    
    for index, ax in enumerate(axis.ravel()):
        for condition in dataframe['Condition'].unique():
            data = dataframe[dataframe['Condition']==condition]
            plot = ax.scatter(x=data['Burst#'], 
                              y=data[cols[index]],
                              label='{} {} Neuron'.format(condition, Neuron),
                              alpha=.5)

        y_label = ax.set_ylabel(cols[index],fontsize=16)
        x_label = ax.set_xlabel('Burst #',fontsize=16)
        ax.set_title(title,fontsize=20)
        
    plt.legend()
    plt.tight_layout()
    return fig, ax

def paired_plots(dataframe, condition='Pre'):

    sns.set(style="ticks", palette="husl")
    data = dataframe[dataframe['Condition']==condition]
    g = sns.PairGrid(data=data, hue="Neuron", height=4, aspect=1)
    g = g.map_diag(plt.hist, histtype="step", linewidth=3)
    g = g.map_offdiag(plt.scatter, alpha=.25)
    g = g.add_legend()

    # There has to be a better way
    # TODO: Fix below, there has to be a better way than this to make the plot
    xlabels,ylabels = [],[]

    for ax in g.axes[-1,:]:
        xlabel = ax.xaxis.get_label_text()
        xlabels.append(xlabel)

    for ax in g.axes[:,0]:
        ylabel = ax.yaxis.get_label_text()
        ylabels.append(ylabel)

    for i in range(len(xlabels)):
        for j in range(len(ylabels)):
            g.axes[j,i].xaxis.set_label_text(xlabels[i], fontsize=16)
            g.axes[j,i].yaxis.set_label_text(ylabels[j], fontsize=16)

    for ax in g.axes.flat:
        # labelleft refers to yticklabels on the left side of each subplot
        ax.tick_params(axis='y', labelleft=True) # method 1
        ax.tick_params(axis='x', labelbottom=True) # method 1

    plt.tight_layout()
    plt.show()
    
def max_burst_number(dataframe, Neuron=None):
    """Returns a the figure and axises of a plot of the maximum burst number per condition

    :param dataframe: pd.Dataframe
    :param Neuron: str, optional to restrict the neuron
    :return:
    """
    if Neuron is not None:
        dataframe=dataframe[dataframe.Neuron==Neuron]
    # Get Max number of Bursts for each conditon
    x_ = [dataframe[dataframe['Condition']==condition]['Burst#'].max() 
          for condition in dataframe['Condition'].unique()] # TODO: .groupby instead
    # Put it into a dataframe to use seaborn
    burst_num = dict(zip(dataframe['Condition'].unique(), x_))
    burst_num = pd.DataFrame.from_dict(burst_num, orient='index', columns=['Burst#'])
    burst_num['Condition'] = burst_num.index

    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(data=burst_num,x='Condition', y='Burst#',ax=ax)
    ax.set_ylabel('Total Bursts', fontsize=16)
    ax.set_xlabel('Condition', fontsize=16)
    title = plt.title('Number of Bursts', fontsize=20)
    return fig, ax

def condition_plot(dataframe, cols, Neuron='all', title='', kind='line', figsize=(16, 8),
                   palette=None, **kwargs):
    """Makes plots for viewing differences in conditions
    :param dataframe: pd.Dataframe, must have a column Condition
    :param cols: list of str, relevant columns in the data frame
    :param Neuron: str or sequence, name of neuron(s) to analyze, defaults as all neurons with 'all'
                    for multiple neurons enter a sequence (list, array, etc.) with each neuron as a
                    str.
    :param title: str, title of the plot
    :param kind: str, the kind of condition plot to generate
                 acceptable arguments are line, violin or scatter
    :param figsize: tuble, figure size
    :param palette: str, argument for plot color, defaults as colorblind
    :return:
    """

    #if cols is None:  # Default params
        #cols = __default_y

    fig, axis = plt.subplots(nrows=len(cols) // 2, ncols=2, figsize=figsize)

    if not isinstance(cols, Sequence):
        raise TypeError('cols must be a sequence (either a list or an array)')

    if Neuron != 'all':
        dataframe = dataframe[dataframe['Neuron'] == Neuron]
        dataframe = dataframe[dataframe.Neuron.isin(Neuron)]

    pal = palette
    if pal is None:
        pal = 'colorblind'
    sns.set_palette(pal)
    for index, ax in enumerate(axis.ravel()):
        for condition in dataframe['Condition'].unique():
            data = dataframe[dataframe['Condition'] == condition]

            if kind == 'line':
                g = sns.pointplot(x="Condition",
                                  y=cols[index],
                                  hue="Neuron",
                                  capsize=.2,
                                  #palette=pal,
                                  kind="point",
                                  data=dataframe,
                                  ax=ax)

            elif kind =='scatter':
                g = ax.scatter(x=data['Burst#'],
                                  y=data[cols[index]],
                                  label='{} {} Neuron'.format(condition, Neuron),
                                  alpha=.5)

                #ax = sns.scatterplot(data=data,
                                     #x="Burst#",
                                     #y=data[cols[index]],
                                     #hue="Condition",
                                     #style='Neuron',
                                     #ax=ax)

            elif kind == 'violin':
                g = sns.violinplot(x='Condition',
                                   y=cols[index],
                                   data=dataframe,
                                   hue='Neuron',
                                   scale_hue=False,
                                   inner='stick',
                                   scale='width',
                                   split=False,
                                   ax=ax,
                                   bw='scott',
                                   cut=0)
                                   #palette=pal



        y_label = ax.set_ylabel(cols[index], fontsize=16)
        x_label = ax.set_xlabel('Burst #', fontsize=16)

        if index == 0:
            if kind == 'scatter':
                continue
            ax.set_title(title, fontsize=20)
            legend_without_duplicate_labels(ax)

        if kind != 'scatter':
            if index > 0:
                ax.get_legend().remove()

    ax.set_title(title, fontsize=20)
    legend_without_duplicate_labels(ax)
    plt.tight_layout()
    return fig, ax

def condition_scatter_plot(dataframe, y_vals='all', Neuron='LG', 
                           title=''):

    fig, axis = plt.subplots(ncols=3, nrows=2, figsize=(20,10))

    if y_vals.lower() == 'all': # Default params
            y_vals = ['Burst Duration (sec)', 
                      '# of Spikes', 
                      'Spike Frequency (Hz)', 
                      'Instantaneous Period (sec)', 
                      'Instantaneous Frequency (Hz)', 
                      'Duty Cycle']
            
    else:
        raise NotImplementedError("Non-default behavior is currently not implemented")
        
        
    if Neuron.lower() != 'all':
        dataframe = dataframe[dataframe['Neuron']==Neuron]
        


    for index, ax in enumerate(axis.ravel()):
            # Make the plot
            g = sns.stripplot(x='Condition', 
                              y=y_vals[index], 
                               data=dataframe, 
                               hue='Date', 
                               
                               ax=ax, 
                               palette='viridis', alpha=.25)
            g = sns.pointplot(x='Condition', 
                       y=y_vals[index], 
                       data=dataframe, 
                       hue='Date', 
                       estimator=np.median,
                       ax=ax, 
                       palette='viridis', scale=1.2)

            # Set Title, y-axis, x-axis values
            ax.set_title(title, fontsize=20)
            ax.set_ylabel(y_vals[index], fontsize=16)
            ax.set_xlabel("Condition", fontsize=16)

    # Make it look pretty
    mpl.rc('ytick', labelsize=16) 
    mpl.rc('xtick', labelsize=16) 
    plt.tight_layout()
    #plt.subplots_adjust(hspace=.6)
    #plt.show()
    return fig, ax

def legend_without_duplicate_labels(ax, **kwargs):
    """Pass in an axis from matplotlib, will return a legend without duplicates"""
    handles, labels = ax.get_legend_handles_labels()
    unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
    ax.legend(*zip(*unique), **kwargs)