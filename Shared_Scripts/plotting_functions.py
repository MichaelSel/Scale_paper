import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from Shared_Scripts import stat_funcs

#Helper function for plot annotation
def annotate(ax, data, x, y, type='pearson'):
    # slope, intercept, rvalue, pvalue, stderr = scipy.stats.linregress(x=data[x], y=data[y])
    if(type=='pearson'):
        r,p = stat_funcs.permtest_corr_pearson(data[x],data[y],10000,False)
    elif(type=='spearman'):
        r, p = stat_funcs.permtest_corr(data[x], data[y], 10000)
    ax.text(.02, .9, f'r2={r ** 2:.2f}, p={p:.2g}', transform=ax.transAxes)

def bin_by_feature_bars (dataset,x,y="rate shifted - rate swapped (NN)", bins=3,diatonic="include",normalize=True,figsize=(6,6),ylim=None, show_data_points=True):
    temp = dataset #loading dataset
    temp = temp.groupby("set").mean().reset_index() #collapsing subject by set
    if(diatonic=="exclude"): temp = temp[temp['subset_of_diatonic']==False]
    elif(diatonic=="only"): temp = temp[temp['subset_of_diatonic']==True]

    if(normalize):
        min = temp[x].min()
        max = temp[x].max()
        temp[x] = (temp[x]-min)/(max-min)

    temp[x] = pd.qcut(temp[x],bins,precision=2,duplicates="drop") # cut the data into bins

    #plot the data
    fig, ax = plt.subplots(figsize=figsize)
    sns.set_style("ticks")
    sns.set_context("talk")
    sns.barplot(x=x, y=y, data=temp, ax=ax, color=".9")
    if(show_data_points): sns.stripplot(x=x, y=y, data=temp, ax=ax, dodge=True, size=13, marker=".", edgecolor="gray", alpha=.8)
    if(ylim):plt.ylim(ylim)

def distribution(dataset, x,collapse_sets=False):
    temp = dataset #loading dataset
    if(collapse_sets):
        temp = temp.groupby("set").mean().reset_index() #collapsing subject by set
    sns.displot(x=x,data=temp)

def bin_by_feature_correlation (dataset, x,y="rate shifted - rate swapped (NN)",bins=3,diatonic="include",normalize=True, figsize=(6,6)):
    temp = dataset #loading dataset
    temp = temp.groupby("set").mean().reset_index() #collapsing subject by set
    if(diatonic=="exclude"): temp = temp[temp['subset_of_diatonic']==False]
    elif(diatonic=="only"): temp = temp[temp['subset_of_diatonic']==True]

    if(normalize):
        min = temp[x].min()
        max = temp[x].max()
        temp[x] = (temp[x]-min)/(max-min)

    temp[x+"_binned"] = pd.qcut(temp[x],bins,precision=2,duplicates="drop") # cut the data into bins

    temp = temp.groupby(x+"_binned").mean().reset_index()

    temp = temp.dropna(subset=[x])
    #plot the data


    fig, ax = plt.subplots(figsize=figsize)

    sns.regplot(x=x, y=y, data=temp, ax=ax)
    annotate(ax,x=x, y=y, data=temp)
    plt.show()

def correlation (dataset, x,y="rate shifted - rate swapped (NN)",diatonic="include", normalize=True, figsize=(6,6), type='pearson'):
    temp = dataset #loading dataset
    temp = temp.groupby("set").mean().reset_index() #collapsing subject by set
    if(diatonic=="exclude"): temp = temp[temp['subset_of_diatonic']==False]
    elif(diatonic=="only"): temp = temp[temp['subset_of_diatonic']==True]

    if(normalize):
        min = temp[x].min()
        max = temp[x].max()
        temp[x] = (temp[x]-min)/(max-min)

    fig, ax = plt.subplots(figsize=figsize)

    #plot the data

    sns.regplot(x=x, y=y, data=temp, ax=ax)
    annotate(ax,x=x, y=y, data=temp, type=type)
    plt.show()