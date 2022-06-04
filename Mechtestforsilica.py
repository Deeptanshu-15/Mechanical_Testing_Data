"""
Created on Fri Dec 14 09:00:38 2018

@author: sid
"""
import matplotlib
import pandas as pd
import numpy as np
import os
import plotly.graph_objs as go
import plotly.offline as po
import plotly.io as pio
from random import randint
f=[]

mypath = (r"C:\Users\sid\Desktop\Side projects\Romain paper\200213")
print ("\n Present path is",mypath,"\t Change ? y/n")
Choice = input ("r\t \t Choice: ") #'C:\PhD_Oct\Data' #Filepath for all data files
if (Choice == "y"):
    mypath = input("\n Choose new path:")
os.chdir(mypath)
for (dirpath, dirnames, filenames) in os.walk(mypath):
    f.extend(filenames) #Stores filenames into a list
    break
book = {} #dictionary array
Pr = input("\n Input the dataset to print: ") #raw_input for input of digits and characters
Pr_print = str(Pr) + ' % P750 Compression Test'
for i in range(len(f)):
    if (Pr in f[i]):
        book[i] = pd.read_csv(f[i], sep = ';') #assigning
L = np.zeros(len(book))
for i in range(len(book)):
    L[i] = len(book[i].index)
    
#Comp = pd.read_excel(r'C:\Users\sid\Desktop\Silica aerogel mech test paper\Compiled silica data.xlsx', sheet_name = 'Reader')
##Indexer = Comp.loc[Comp['Corrected']==int(Pr)].index.values #sorted indexing function for chosen column with values of indexes
#Area = np.zeros((len(Comp)), dtype=float) #for stress and youngs mod
#for i in range(len(Comp)):
#    Area[i] = (22*Comp.diameter[i]*Comp.diameter[i])/(7*400)
#
#data_str = pd.read_excel('C:\PhD_Dec18\Mech test\Mech test.xlsx', sheet_name = 'Data analysis')
#data_ind = data_str.loc[data_str['Compression']==int(Pr)].index.values
#fin_str = np.zeros((len(data_ind)), dtype=float)
#for i in range(len(data_ind)):
#    fin_str[i] = data_str.loc[data_ind[i], 'Final Strain']
#    fin_str[i] = fin_str[i]*100

N_str = np.zeros((len(L), int(max(L)))) #assigning proper array lengths
Disp = np.zeros((len(L), int(max(L))))
Per_disp = np.zeros((len(L), int(max(L))))
deh = np.zeros((len(L), int(max(L))))
Pos = np.zeros((len(L), int(max(L))), dtype = int)
Sigma = np.zeros((len(L), int(max(L)))) #not required since exported data` is already in Sigma and not force, it is normal stress
Young = np.zeros((len(L), int(max(L))))
Sig10 = np.zeros((len(L), int(max(L))))
Sig30 = np.zeros((len(L), int(max(L))))
Sig50 = np.zeros((len(L), int(max(L))))
Sig80 = np.zeros((len(L), int(max(L))))
sorted_N_comp = np.empty((len(L), int(max(L)))) #compression only
sorted_Per_comp = np.empty((len(L), int(max(L)))) #compression only
sorted_N_comp_nan = np.empty((len(L), int(max(L)))) #compression only
sorted_Per_comp_nan = np.empty((len(L), int(max(L)))) #compression only
Sig__10 = np.zeros(len(L))
Sig__30 = np.zeros(len(L))
Sig__50 = np.zeros(len(L))
Sig__80 = np.zeros(len(L))
Sigma_max = np.zeros(len(L))
Strain_end = np.zeros(len(L))
Str_end = np.zeros(len(L))
Col_names = book[0].columns.tolist()
#Starting initialization phase
#print ("\n  Available columns to plot graph:", Col_names)
#X_axis = input('\n Choose digit for X axis: ')
#Y_axis = input('\n Choose digit for Y axis: ') '''required later for the sigma vs graphs
for i in range(len(L)):
    for j in range(int(L[i])):
        N_str[i][j] = book[i].loc[j,Col_names[0]] #normalstress
        Disp[i][j] = book[i].loc[j,Col_names[1]] #Displacement
        deh[i][j] = book[i].loc[j,Col_names[2]] #Dehling nominale
        Pos[i][j] = book[i].loc[j,Col_names[3]] #Position
        Per_disp[i][j] = (deh[i][j]*100)/Pos[i][3] # % displacement
#        Sigma[i][j] = N_str[i][j]*1000/Area[i] #sigma calculation
        Young[i][j] = N_str[i][j]*100/Per_disp[i][j] #Youngs mod calculation
       
Per_disp[np.isnan(Per_disp)] = 0 #setting nan values (0/0) to 0 to avoid errors while compute
#end of initialization phase for dataframes
#Processing for Excel sheet data

P_val = {}
Sigg = {}
Per_name = []
colors = []

Per_max = np.zeros(len(L), dtype=int)
Per_max_float = np.zeros(len(L), dtype=float)
N_str_max = np.zeros(len(L), dtype=float)
for i in range(int(len(L))):
    Per_max[i] = np.amax(Per_disp[i])
    N_str_max[i] = np.amax(N_str[i]) #maximum calculation and storage into another array
    Per_max_float[i] = np.amax(Per_disp[i])
#Sorting and Calculation Start
arrsort = Per_max.argsort() # argumented for ordering ascending compression, +1 for descending
sorted_Per_max = Per_max[arrsort[::1]]
sorted_Per_max_float = Per_max_float[arrsort[::1]]
sorted_N_str_max = N_str_max[arrsort[::1]]
sorted_N_str = N_str[arrsort[::1]]
sorted_Disp = Disp[arrsort[::1]]
sorted_deh = deh[arrsort[::1]]
sorted_Pos = Pos[arrsort[::1]]
sorted_Per_disp = Per_disp[arrsort[::1]] #multiline sorted based on argumented sort from the maximum of compression, basically for labelling and displaying properly
#sorted_Area = Area[arrsort[::1]]
#sorted_Area = Area[arrsort[::1]]
sorted_Sigma = Sigma[arrsort[::1]]
sorted_Young = Young[arrsort[::1]]
#sorted_fin_str = fin_str[arrsort[::1]] #sorted final strain for the correct order
for i in range(len(L)):
    Sigma_max[i] = np.amax(sorted_N_str[i])
    for j in range(int(L[i])):
        if (int(sorted_Per_disp[i][j]) == 10):
            Sig10[i][j] = sorted_N_str[i][j]
        if (int(sorted_Per_disp[i][j]) == 30):
            Sig30[i][j] = sorted_N_str[i][j]
        if (int(sorted_Per_disp[i][j]) == 50):
            Sig50[i][j] = sorted_N_str[i][j]
        if (int(sorted_Per_disp[i][j]) == 80):
            Sig80[i][j] = sorted_N_str[i][j]
        if (Per_disp[-i][j]!=0.00):
            Strain_end[i] = sorted_Per_disp[i][j]
#Different Sigma10,30 etc  calculation
i = j = 0
Sig_Check = c1 = c3 = c5 = c8 = St = cc = 0
for i in range(len(L)):
    for j in range(int(L[i])):
        Sig_Check = int(sorted_Per_disp[i][j]*100)/100
        if (Sig_Check == 10.00 and c1 == i):
            Sig__10[i] = sorted_N_str[i][j]
            c1+=1
    if (c1 == i):
            c1+=1
        
for i in range(len(L)):
    for j in range(int(L[i])):
        Sig_Check = int(sorted_Per_disp[i][j]*100)/100
        if (Sig_Check == 30.00 and c3 == i):
                Sig__30[i] = sorted_N_str[i][j]
                c3+=1
    if (c3 == i):
            c3+=1

for i in range(len(L)):
    for j in range(int(L[i])):
        Sig_Check = int(sorted_Per_disp[i][j]*100)/100
        if (Sig_Check == 50.00 and c5 == i):
                Sig__50[i] = sorted_N_str[i][j]
                c5+=1
    if (c5 == i):
        c5+=1
        
for i in range(len(L)):
    for j in range(int(L[i])):
        Sig_Check = int(sorted_Per_disp[i][j]*100)/100
        if (Sig_Check == 80.00 and c5 == i):
                Sig__80[i] = sorted_N_str[i][j]
                c8+=1
    if (c8 == i):
        c8+=1
##                      Checker for the End_Strain                  ##
for i in range(len(L)):
    End_N = np.flipud(sorted_N_str[i])
    End_disp = np.flipud(sorted_Per_disp[i])
    for j in range(int(L[i])):
        St = int(End_N[j]*1000)/1000
        if (St == 0.001 and cc == i):
            Str_end[i] = End_disp[j]
            cc = cc+1
            
stop = 0

for i in range(len(L)):
    for j in range(int(L[i])):
        if (j <= sorted_N_str[i].argmax()):
            sorted_N_comp[i][j] = sorted_N_str[i][j]
            sorted_Per_comp[i][j] = sorted_Per_disp[i][j]  #for the compression only 
            
# sorted_Per_comp[i][sorted_Per_comp[i]!=0]
        
#for i in range(len(Indexer)): #color coding and control of plotted text with related colors
#    Sigma_max[i] = sorted_N_str_max[i]*1000/sorted_Area[i]
#    colors.append('%06X' % randint(0, 0xFFFFFF)) 

#colors = ['#' + color for color in colors]    
    
for i in range(int(len(L))):
    Per_name.append(str(sorted_Per_max[i]) + '% Compression')
    
Fin_plot_x = np.zeros((len(L),2)) #plotter for final strain
Fin_plot_y = np.zeros((len(L),2))

for i in range(len(L)): #ordering needs to be proper remember that!!
    Fin_plot_x[i][0] = sorted_Per_max_float[i]
#    Fin_plot_x[i][1] = sorted_fin_str[i]
    Fin_plot_y[i][0] = Sigma_max[i]

final_strain_20 = [2.75, 8.51, 3.21, 0.0, 14.50]
final_strain_50 = [30.97, 1.1, 3.55, 40.70, 44.47]
Color_string = ['#FF0000','#F6A600','#9ACD32','#006400','#00aeff','#00008b','#ff00ff']
Color_6_2h = ['#008080']
Name_String_20 = []
Name_String_50 = ['20%: 0.073 g/cc', '30%: 0.104 g/cc','25% : 0.089 g/cc','15% : 0.065 g/cc','13% : 0.060 g/cc']

part_mean = np.zeros(len(L))
av_calc = len(L)*255000
Avg_Young = np.zeros((av_calc))
ctr = 0
for i in range(len(L)):
    holder = []
    for j in range(int(L[i])):
        if 3<sorted_Per_disp[i][j]<5: #Youngs modulus calculation range
            Avg_Young[ctr] = sorted_Young[i][j] #truth value to be determined #counter to put exact amount of elements into the array
            holder.append(Avg_Young[ctr])
            ctr +=1
        holder_arr = np.array(holder)    
        part_mean[i] = np.mean(holder_arr)
            
#average Youngs calculation
Men = Avg_Young[np.nonzero(Avg_Young)]
Mean = np.mean(Men)
Std_dev = np.std(Men)
Print_Mean = 'Mean: ' + str("%.2f" % Mean)
Print_Std = 'Standard Deviation: ±' + str("%.2f" % Std_dev)
        
for i in range(len(book)):
    P_val[i] = {
                  "x": [j for j in sorted_Per_disp[i]], # sorted_Per_comp[i][sorted_Per_comp[i]!=0]
                  "y": [j for j in sorted_N_str[i]],  # sorted_Per_comp[i][sorted_Per_comp[i]!=0]
                   "name" : Per_name[i],##Took me 3 hours to solve this bullshit, Very fucking easy but forgot basic stuff
                  "marker" : {
                      'color': '#ff00ff'
                          },
                  "mode": "lines", 
                  "type": "scatter", 
                     } # GGWP assigning of dictionaries with required print values

Final_strain = {
        "x" : [i for i in final_strain_50],
        "y" : [0.0008 for i in final_strain_50],
        "marker" : { 
                "color" : Color_string,
                "size" : 8,
              "symbol" : 201,
              },
        "line":{"width":2},
        "mode" : "markers",
        "type" : "scatter",
        "name" : "Final Strain (%) after 1 month",
        "showlegend": False,
        }
    
# for i in range(len(L)):
#     Sigg[i] = {
#                 "x" : [j for j in Fin_plot_x[i]],
#                 "y" : [j for j in Fin_plot_y[i]],
# #                "name" : "Final Strain plot",
# #                "marker": {"color" : colors[i]},
#                 "line" : {
#                         "shape" : "spline",
#                         "dash" : "dashdot"
#                         },
#                 "mode" : "lines",
#                 "type" : "scatter",
#                 "showlegend" : False
#                 }
       
layout = {
  "template":"simple_white",
  "boxmode":"overlay",
  "autosize": False, 
  "height": 1100, 
  "width": 1100,
#  "font" : "Droid Serif",
  "hovermode": "closest", 
  #colorway:#1f77b4#ff7f0e#2ca02c#d62728#9467bd#8c564b#e377c2#7f7f7f#bcbd22#17becf ##default tracecolor
  "margin": {
    "r": 70, 
    "t": 50, 
    "b": 50, 
    "l": 65, 
    "pad": 1  }, 
  "showlegend": False,
  "legend":{
          "x" : 0.05,
          "y" : 0.98,
          "font": {
                  "size" : 25,
                  "family":"sans-serif",
                  "color" : "#FEF0DB"
                  },
        "traceorder":"normal",
        "bgcolor":"#000000",
        "bordercolor":"#FFFFFF",
        "borderwidth": 2,
          },
#  "title": "New cellulose Compression tests",
   # "title": {
   #      # 'text': "0.103 g/cm<sup>3</sup>: 2h aged",
   #      'y':0.9,
   #      'x':0.5,
   #      'xanchor': 'center',
   #      'yanchor': 'top'},
  "titlefont": {
    "color": "#000000", 
    "size": 40
  },  
  "xaxis": {
    # "title": "<b> Strain (%) <b>",
    "domain": [0.0, 1.0], 
    "mirror": "all", 
    "nticks": 0, 
    "ticklen":7.0,
    "titlefont": {
            "size": 28,
            },
    "autorange" : False,
    "range" : [0.0, 100.0],
    "showgrid": False, 
    "showline": True,
    "zeroline": True,
    "side": "bottom", 
    "linewidth":2.0,
    "tickwidth":3.0,
    "tickfont": {"size": 35.0, "family":"sans-serif"}, 
    "ticks": "outside", 
    "type": "linear",
    "visible": True,
    "showticklabels": False
  }, 
#  "xaxis2": {
#          "domain":[0.08, 0.53],
#          "anchor" : 'y2',
#          "title": "<b>Strain (%)</b>",
#          "mirror": "ticks", 
#          "nticks": 0, 
#          "titlefont": {
#            "size": 16,
#            },
#          "autorange" : True,
#          "showgrid": False, 
#          "showline": True,
#          "tickfont": {"size": 16}, 
#          "ticks": "inside", 
#          "type": "linear", 
#          "zeroline": True
#          },
#  "yaxis2": {
#          "domain":[0.15, 0.6],
#          "anchor" : 'x2',
#          "title": "<b>Sigma max. (σ<sub>max</sub>, MPa)</b>",
#          "mirror": "ticks", 
#          "nticks": 0, 
#          "titlefont": {
#            "size": 16,
#            },
#          "autorange" : True,
#          "showgrid": False, 
#          "showline": True,
#          "tickfont": {"size": 16}, 
#          "ticks": "inside", 
#          "type": "linear", 
##          "zeroline": True
#          },
  "yaxis": {
    "domain": [0.0, 0.0], 
    # "title": "<b> Normal Stress, σ<sub>N</sub> (MPa)</b>",
    "titlefont": {
            "size": 28,
            },
    "mirror": "all",
    "ticklen":7.0,
    "nticks": 0, 
    "range" : [0.0, 1.65],
    "showgrid": False, 
    "showline": True, 
    "side": "left", 
    "linewidth":2.0,
    "tickwidth":3.0,
    "tickfont": {"size": 15.0, "family":"sans-serif"}, 
    "ticks": "outside", 
    "type": "linear", 
    "zeroline": True,
    "visible": True,
    "showticklabels": False
  },
}  
new = ([P_val[j] for j in P_val.keys()]) #items gives index(keys) and values
new_Sig = ([Sigg[j] for j in Sigg.keys()])
# for i in range(len(new_Sig)):
#     new.append(new_Sig[i])
# new.append(Final_strain)
img_name = 'my-plot' #name of image file
dload = os.path.expanduser('~/Downloads') #storage location
save_dir = '/downloads'
po.plot({'data': new, 'layout': layout}, image='png', image_width =2400, image_height=1800, filename = 'Z_firsttry')
