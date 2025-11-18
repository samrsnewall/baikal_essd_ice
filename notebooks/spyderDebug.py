#import the necessary data tools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
plt.rcParams.update({'font.size': 10})
cm = 1/2.54

#Input the names of all the cores we have data for into 'allcores'.
allcores = ['18-B1','18-P2','287-K2','305-A5','307-A3','308-A3','316-P3','316-T3','331-P1','331-T1','333-P2',\
            '333-T2','339-B2','339-P2','339-T2','340-B1','340-P1','340-T1','342-B1','342-P1','342-T1',\
            'BAIK13-1C','BAIK13-4F',\
            'BDP93-1','BDP93-2','BDP96-1','BDP96-2','BDP97-1','BDP98-1',\
            'BSS06-G2','323-PC1', 'BarguzinCore18',\
            'CON01-603-5','CON01-605-3','CON01-605-5','CON01-606-3',\
            'Ver.99 G-6','Ver93-2 St.4-PC','Ver94-5 St.16-PC','Ver94-5 St.16-Pilot','Ver94-5 St.19-PC',\
            'Ver94-5 St.22-GC','Ver96-2 St.3-GC','Ver96-2 St.7-Pilot','Ver96-2 St.7-PC', 'Ver97-1 St.6',\
            'VER93-2 St.24GC','VER98-1 St.5PC','VER98-1 St.5GC','VER98-1 St.6GC','VER99G12']
    
# Path to the PANGAEA export (tab-delimited text)
datafile = "../data/Baikal_14C_data_updated17Nov25_copy.txt"  # or whatever relative path in your repo

# Read the data section of the PANGAEA file
# (skip the metadata block; the table header starts after line 95)
raw = pd.read_csv(datafile, sep="\t", skiprows=95)

# Name columns
raw.columns = [
    "Event", "Core Name", "Lab Code", "Sec_label",
    "", "Depth_bot_m",
    "Middle Depth", "Corrected Depth", "Thick_cm",
    "Material",
    "Value", "Error",
    "d13C_method",
    "d13C_permil", "d13C_error",
    "Carbon_content_percent", "Reference", "Comment"
]

# Filter to just the cores you care about
dfall = raw[raw["Core Name"].isin(allcores)].copy()

#Convert necessary columns to numerics
cols_to_convert = ["Middle Depth", "Corrected Depth", "Value", "Error"]
for c in cols_to_convert:
    dfall[c] = pd.to_numeric(dfall[c], errors="coerce")

#Here we will check for both negative and non-numeric age values.

#First, set up some empty vectors
dfall_age = pd.Series([], dtype='float64')
negvals = pd.Series([], dtype='float64')
negcodes = pd.Series([], dtype='str')
nonnums = pd.Series([], dtype='str')
nonnumcodes = pd.Series([], dtype='str')

#Run through checking for negative and string values for 'Value'.
for i in range(len(dfall['Lab Code'])):
    if not isinstance(dfall['Value'].iloc[i], str):
        if dfall['Value'].iloc[i] < 0:
            negvals = pd.concat([negvals, pd.Series([dfall['Value'].iloc[i]])], ignore_index=True)
            negcodes = pd.concat([negcodes, pd.Series([dfall['Lab Code'].iloc[i]])], ignore_index=True)
    else:
        nonnums = pd.concat([nonnums, pd.Series([dfall['Value'].iloc[i]])], ignore_index=True)
        nonnumcodes = pd.concat([nonnumcodes, pd.Series([dfall['Lab Code'].iloc[i]])], ignore_index=True)

#Set up a record of labcodes that should be kept out of future analyses
xcodes = pd.concat([negcodes, nonnumcodes], ignore_index=True)

#Let us here remove these dates from 'dfall' using their lab codes as stored in the variable 'xcodes'
dfall = dfall.loc[~dfall['Lab Code'].isin(xcodes)]


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

allcores = ['18-B1','18-P2','287-K2','305-A5','307-A3','308-A3','316-P3','316-T3','331-P1','331-T1','333-P2',\
            '333-T2','339-B2','339-P2','339-T2','340-B1','340-P1','340-T1','342-B1','342-P1','342-T1',\
            'BAIK13-1C','BAIK13-4F',\
            'BDP93-1','BDP93-2','BDP96-1','BDP96-2','BDP97-1','BDP98-1',\
            'BSS06-G2','323-PC1',\
            'CON01-603-5','CON01-605-3','CON01-605-5','CON01-606-3',\
            'Ver.99 G-6','Ver93-2 St.4-PC','Ver94-5 St.16-PC','Ver94-5 St.16-Pilot','Ver94-5 St.19-PC',\
            'Ver94-5 St.22-GC','Ver96-2 St.3-GC','Ver96-2 St.7-Pilot','Ver96-2 St.7-PC', 'Ver97-1 St.6',\
            'VER93-2 St.24GC','VER98-1 St.5PC','VER98-1 St.5GC','VER98-1 St.6GC','VER99G12']
 

youngcores = ['18-B1', '308-A3', 'BSS06-G2', '331-T1', '339-B2','340-B1', '342-B1',\
              '342-T1', 'BAIK13-1C', 'BAIK13-4F', '305-A5','316-T3', 'BDP97-1', \
              'CON01-603-5','CON01-605-3','CON01-605-5','CON01-606-3', 'Ver93-2 St.4-PC', \
              'Ver94-5 St.22-GC',  '339-T2','340-T1' ]
    
longcores = ['18-P2','287-K2','307-A3','316-P3','331-P1','333-P2',\
            '333-T2','339-P2','340-P1','342-P1',\
            'BarguzinCore18','BDP96-1','BDP96-2','323-PC1',\
            'Ver96-2 St.7-PC','Ver.99 G-6','Ver94-5 St.16-PC','Ver94-5 St.16-Pilot','Ver94-5 St.19-PC',\
            'Ver96-2 St.7-Pilot','Ver96-2 St.3-GC', 'Ver97-1 St.6',\
            'VER93-2 St.24GC','VER98-1 St.5PC','VER98-1 St.5GC','VER98-1 St.6GC','BDP98-1','VER99G12','BDP93-1','BDP93-2']
    
    
AR_ASAcores = ['Ver94-5 St.16-PC', '333-P2', '333-T2', '331-T1', '340-P1', '340-T1',\
            'Ver96-2 St.3-GC', 'VER98-1 St.6GC', 'VER98-1 St.5GC', 'Ver97-1 St.6', 'BDP98-1']  

BS_nonASAcores = ['BDP93-1', '339-P2', '316-P3']

BS_ASAcores = ['316-T3', 'BSS06-G2', '339-T2', '339-B2', 'BDP93-2', '305-A5', 'VER93-2 St.24GC', 'VER99G12']

# '.' for dot; 'o' for circle, 'v' for trinagle down, '+' for plus
plotstyles1 = ['ok', '*r', '+r', 'ok', 'ok', '+r', '+r', '+r', '+r']

def allplots(core_names, plotstyles, plotrows, plotcolumns, dfall):
    fig, axs = plt.subplots(plotrows, plotcolumns)
    fig.set_figheight(15)
    fig.set_figwidth(10)
    
    materials = [
        'TOC', 'Pollen Concentrate', 'Total Lipids', 'POM', 'FOM',
        'Wood', 'Lipid fraction', 'Bulk Silty Clay'
    ]
    
    for j, core in enumerate(core_names):
        fig_a, fig_b = divmod(j, plotcolumns)
        ax = axs[fig_a, fig_b]
        
        # subset to this core once
        rdata_core = dfall[dfall['Core Name'] == core].copy()
        if rdata_core.empty:
            ax.set_title(core + " (no data)")
            continue
        
        for i, mat in enumerate(materials):
            rd_toc = rdata_core[rdata_core['Material'] == mat].copy()
            if rd_toc.empty:
                continue
            
            # keep only rows with numeric Value and Error
            rd_toc = rd_toc[rd_toc['Value'].notna() & rd_toc['Error'].notna()]
            if rd_toc.empty:
                continue
            
            # choose depth column: prefer Corrected Depth if any numeric values exist
            use_corrected = rd_toc['Corrected Depth'].notna().any()
            if use_corrected:
                x = rd_toc['Corrected Depth']
            else:
                x = rd_toc['Middle Depth']
            
            y = rd_toc['Value']   # already in 14C kyr BP
            yerror = rd_toc['Error']  # kyr
            
            if x.empty or y.empty:
                continue
            
            fmt = plotstyles[i] if i < len(plotstyles) else '.'
            ax.errorbar(x, y, yerr=yerror, fmt=fmt)
        
        # young vs long cores layout logic (now in kyr)
        youngAxes = fig_a in [0, 1, 2, 3, 4, 5, 6]
        if youngAxes:
            ylims = [0, 25]   # 0–25 kyr instead of 0–25000 yr
            ax.set_ylim(ylims)
            ax.text(3.75, ylims[1]*0.7, core, horizontalalignment="center")
        else:
            ylims = [0, 55]   # 0–55 kyr instead of 0–55000 yr
            ax.set_ylim(ylims)
            ax.text(3.75, ylims[1]*0.7, core, horizontalalignment="center")
        
        # y-ticks now in kyr
        if fig_b == 0 and youngAxes:
            ax.set_yticks([10, 20], ["10", "20"])
        elif fig_b != 0 and youngAxes:
            ax.set_yticks([10, 20], [" ", " "])
        elif fig_b == 0 and not youngAxes:
            ax.set_yticks([20, 40], ["20", "40"])
        elif fig_b != 0 and not youngAxes:
            ax.set_yticks([20, 40], [" ", " "])
        
        # x-ticks and x-label
        if fig_a == 16:
            ax.set_xticks(
                [0, 1, 2, 3, 4, 5, 6, 7],
                ["0", "1", "2", "3", "4", "5", "6", "7"]
            )
        else:
            ax.set_xticks(
                [0, 1, 2, 3, 4, 5, 6, 7],
                ["", "", "", "", "", "", "", ""]
            )
        
        if fig_b == 0 and fig_a == 8:
            ax.set_ylabel('Age ($^{14}$C kyr BP)', fontweight='bold')
        
        if fig_b == 1 and fig_a == 16:
            ax.set_xlabel('Depth (m)', fontweight='bold')
        
        ax.set_xlim([0, 7.5])
        ax.axhline(13, color='0.4', linestyle='--')
    
    plt.tight_layout()



allplots(youngcores+longcores, plotstyles1, 17, 3, dfall)