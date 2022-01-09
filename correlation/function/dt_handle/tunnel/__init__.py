# initial function 
# version : 

# target : 
# 1. read data and process

from datetime import datetime as dtm
from os import listdir, mkdir
from os.path import join as pth, exists, dirname, realpath
import pickle as pkl
from numpy import array, nan
from pandas import date_range, concat
import json as jsn

## bugs box
"""




# """


__all__ = [
		'get_data',
	]


# parameter
cur_file_path = dirname(realpath(__file__))
with open(pth(cur_file_path,'metadata.json'),'r') as f:
	meta_dt = jsn.load(f)

# class
## parant class (read file)
## list the file in the path and 
## read pickle file if it exisits, else read raw data and dump the pickle file
class reader:
	
	nam = None

	## initial setting
	## input : file path, 
	## 		   start time,
	## 		   final time,
	## 		   instrument name,
	## 		   reset switch
	## 
	## because the pickle file will be generated after read raw data first time,
	## if want to re-read the rawdata, please set 'reser=True'

	def __init__(self,_path,_sta,_fin,_reset=False):
		print(f'\n{self.nam}')
		print('='*65)
		print(f"Reading file and process data")

		## class parameter
		self.index = lambda _freq: date_range(_sta,_fin,freq=_freq)
		self.path  = _path
		self.reset = _reset
		self.meta_read = meta_dt[self.nam]['read']
		self.meta_plot = meta_dt[self.nam]['plot']
		self.pkl_nam = f'{self.nam.lower()}.pkl'
		self.__time  = (_sta,_fin)
		
		print(f" from {_sta.strftime('%Y-%m-%d %X')} to {_fin.strftime('%Y-%m-%d %X')}")
		print('='*65)
		print(f"{dtm.now().strftime('%m/%d %X')}")

	def __raw_reader(self,_file):
		## customize each instrument
		## read one filess
		return None

	def __raw_process(self,_df,_freq):
		## customize each instrument
		# breakpoint()
		out = _df.resample(_freq).mean().reindex(self.index(_freq))
		return out

	## read raw data
	def __reader(self):

		## read pickle if pickle file exisits and 'reset=False' or process raw data
		if (self.pkl_nam in listdir(self.path))&(~self.reset):
			print(f"\n\t{dtm.now().strftime('%m/%d %X')} : Reading \033[96mPICKLE\033[0m file of {self.nam}")
			with open(pth(self.path,self.pkl_nam),'rb') as f:
				fout = pkl.load(f)
			return fout
		else: 
			print(f"\n\t{dtm.now().strftime('%m/%d %X')} : Reading \033[96mRAW DATA\033[0m of {self.nam} and process it")

		##=================================================================================================================
		## metadata parameter
		ext_nam, dt_freq = self.meta_read.values()

		## read raw data
		_df_con = None
		
		for file in listdir(self.path):
			if ext_nam not in file.lower(): continue
			print(f"\r\t\treading {file}",end='')

			_df = self.__raw_reader(file)

			if _df is not None:
				_df_con = concat([_df_con,_df]) if _df_con is not None else _df

		## concat the concated list
		df = self.__raw_process(_df_con,dt_freq)
		print()

		##=================================================================================================================
		## dump pickle file
		with open(pth(self.path,self.pkl_nam),'wb') as f:
			pkl.dump(fout,f,protocol=pkl.HIGHEST_PROTOCOL)

		return fout

	## get process data
	def get_data(self,start=None,final=None,mean_freq=None):

		## get dataframe data and process to wanted time range
		_freq = mean_freq if mean_freq is not None else self.meta['freq']
		_time = (start,final) if start is not None else self.__time

		return self.__reader().resample(_freq).mean().reindex(date_range(*_time,freq=_freq))

