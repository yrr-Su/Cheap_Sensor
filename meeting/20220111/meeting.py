
# plot
# tunnel 0 1 5 8

import pickle as pkl
from pathlib import PurePath as Path
import json as jsn
from os import listdir, mkdir
from os.path import join as pth, exists, dirname, realpath
from pandas import date_range, read_csv, DataFrame

# ENV parameter
PATH_DT = Path('data')

# read data
with open(PATH_DT/'meta.json','r') as f:
	meta = jsn.load(f)

with open(PATH_DT/'sensor_dt.pkl','rb') as f:
	sen = pkl.load(f)

with open(PATH_DT/'station_dt.pkl','rb') as f:
	sta = pkl.load(f)

with open(PATH_DT/'古亭_20211228_20220109.csv','r',encoding='utf-8',errors='ignore') as f:
	epa = read_csv(f,parse_dates=['Time']).set_index('Time').reindex(sta.index)

## parameter 
TimeIndex = sta.index
PlotBase_sen  = meta['sensor_setting']
PlotBase_sta  = meta['station_setting']
PlotBase_epa  = meta['epa_setting']

# plot time series
## sensor data and station CO, epa CO PM2.5 PM10
## one axes one compound
## one tunnel one color
"""
from matplotlib.pyplot import subplots, close, show

## parameter
PlotSet = meta['time_series']
PathFig = Path('picture')/'time_series'
mkdir(PathFig) if not exists(PathFig) else None

## function
def plot_dt(nam,suptitle,xmin=None,xmax=None,ymin=None,ymax=None,xlabel=None,ylabel=None,):
	print(f'plot {nam}')
	## parameter
	fs = 14.
	xtick = date_range(*TimeIndex[[0,-1]],freq='1d')
	xtick_label = xtick.strftime("%Y%n%m/%d")

	## plot
	fig, ax = subplots(figsize=(12,7),dpi=150.)

	for _tunnel_nam, _set in PlotBase_sen.items():
		_dt = sen[_tunnel_nam][nam] ## get tunnel and the data
		ax.plot(_dt,**_set,label=_tunnel_nam,zorder=3)

	if nam=='CO':
		ax.plot(sta['CO'],**PlotBase_sta)
		ax.plot(epa['CO (ppm)'],**PlotBase_epa)
	
	if nam in ['PM2.5','PM10']:
		ax.plot(epa[f'{nam} (μg/m3)'],**PlotBase_epa)

	ax.tick_params(which='major',direction='in',length=7,labelsize=fs-2.5)
	ax.tick_params(which='minor',direction='in',length=4.5)
	[ ax.spines[axis].set_visible(False) for axis in ['right','top'] ]
	ax.set(xlim=(xmin,xmax),ylim=(ymin,ymax))

	ax.set_xlabel(xlabel,fontsize=fs)
	ax.set_ylabel(ylabel,fontsize=fs)

	ax.set_xticks(xtick)
	ax.set_xticklabels(xtick_label,fontsize=fs)

	ax.legend(framealpha=0,fontsize=fs-1)

	ax.set_title(f"{TimeIndex[0].strftime('%Y-%m-%d')} to {TimeIndex[-1].strftime('%Y-%m-%d')} @NTU station",loc='right',fontsize=fs)
	fig.suptitle(f'Cheap Sensor Data : {suptitle}(1-hr average)',fontsize=fs+3.)
	fig.savefig(PathFig/f'{nam}.png')
	close()

## main
for _nam in ['Temperature','Humidity','CO','CO2','PM1','PM2.5','PM10',]:
	plot_dt(_nam,**PlotSet[_nam])

# """


# plot scatter
## PM : ntut8 and epa 
## CO : ntut8, epa, sta

# """
from scipy.optimize import curve_fit
from matplotlib.pyplot import subplots, close, show
import numpy as n

## parameter
PathFig = Path('picture')/'scatter'
mkdir(PathFig) if not exists(PathFig) else None

## function
def R_sq(func,opt,xdata,ydata):
	tss = n.sum((ydata-ydata.mean())**2.)  ## total sum of square
	rss = n.sum((ydata-func(xdata,*opt))**2.) ## residual sum of square
	return 1.-rss/tss
func = lambda _x, _sl, _intr: _sl*_x+_intr

## PM
## function
def scatter_epa_tun(tunnel_nam):
	print(f'plot epa v.s. {tunnel_nam}')
	for _nam in ['PM2.5','PM10']:
		print(f'\tplot scatter of {_nam}')

		## data
		_epa = epa[f'{_nam} (μg/m3)']
		_sen = sen[f'{tunnel_nam}'][_nam]

		## curve fit
		curve_df = DataFrame()
		curve_df['epa'] = _epa
		curve_df['sen'] = _sen
		curve_df = curve_df.dropna().copy()

		popt, pcov = curve_fit(func,curve_df.epa,curve_df.sen)

		## parameter
		fs = 13.

		## plot
		fig, ax = subplots(figsize=(8,6),dpi=150.)

		ax.scatter(_epa,_sen,fc='#73dcff',ec='#00b6f3',s=8,zorder=2)
		xlim, ylim = ax.get_xlim(), ax.get_ylim()
		ax.plot([-10,1000],[-10,1000],color='#000000',ls='--',lw=0.8,zorder=3)
		ax.plot(_epa,func(_epa,*popt),color='#ff3366',zorder=4)

		ax.tick_params(which='major',direction='in',length=7,labelsize=fs-2.5)
		ax.tick_params(which='minor',direction='in',length=4.5)
		[ ax.spines[axis].set_visible(False) for axis in ['right','top'] ]
		ax.set(xlim=xlim,ylim=ylim)

		ax.set_xlabel(f'EPA {_nam} ($\mu g/m^3$)',fontsize=fs)
		ax.set_ylabel(f'Cheap Sensor {_nam} ($\mu g/m^3$)',fontsize=fs)

		ax.set_title(f'y = {popt[0]:.2f}x {popt[-1]:+.2f}, R$^2$ = {R_sq(func,popt,curve_df.epa,curve_df.sen):.2f}',loc='right')
		fig.suptitle(f'{_nam} : EPA v.s. Cheap Sensor({tunnel_nam})',fontsize=fs+2.)	
		fig.savefig(Path(PathFig)/f'{_nam}_epa_{tunnel_nam}.png')
		close()

## main
for _tunnel_nam in PlotBase_sen.keys():
	scatter_epa_tun(_tunnel_nam)




# """