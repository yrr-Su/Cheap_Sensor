

# main function of get data

from datetime import datetime as dtm
from datetime import timedelta as dtmdt
from pathlib import PurePath as Path
import sensor.dt_handle as sensor
import station.dt_handle as station
import pickle as pkl

## time decorater
def __timer(func):
	def __wrap(*arg,**kwarg):
		print(f'\nPROGRAM : {__file__}\n')
		__st = dtm.now()

		## main function
		__out = func(*arg,**kwarg)

		__fn = dtm.now()
		__run = (__fn-__st).seconds

		print(f'\nProgram done\nrunning time = {__run//60:3d} min {__run%60:6.3f} s')
		return __out

	return __wrap


@__timer
def run():

	# parameter
	PATH_SENSOR  = Path('..')/'data'/'sensor'
	PATH_STATION = Path('..')/'data'/'station'
	

	
	# data collection
	## sensor 2021-12-28 to 2022-01-07
	'''
	## parameter
	ST_TIME = dtm(2021,12,29)
	ED_TIME = dtm(2022,1,8)

	## collect
	dic_collect = {}
	for _num in range(9): dic_collect[f'ntut{_num}'] = _num

	process_num = [0,1,5,8]
	for _num in process_num:
		ntut_num = sensor.reader(ST_TIME,ED_TIME,PATH_SENSOR,tunnel_num=_num)
		dic_collect[f'ntut{_num}'] = ntut_num.get_data()

	PATH_SAVE = Path('..')/'..'/'meeting'/'20220111'/'data'
	with open(PATH_SAVE/'sensor_dt.pkl','wb') as f:
		pkl.dump(dic_collect,f,protocol=pkl.HIGHEST_PROTOCOL)
	# '''

	## station_gas 2021-12-28 to 2022-01-07
	'''
	## parameter
	ST_TIME = dtm(2021,12,28)
	ED_TIME = dtm(2022,1,8)

	## collect
	gas = station.reader(ST_TIME,ED_TIME,PATH_STATION)
	dt = gas.get_data(mean_freq='10T')

	PATH_SAVE = Path('..')/'..'/'meeting'/'20220111'/'data'
	with open(PATH_SAVE/'station_dt.pkl','wb') as f:
		pkl.dump(dt,f,protocol=pkl.HIGHEST_PROTOCOL)
	# '''



	return dt











#=============================================================================
if __name__=='__main__':

	dt = run()











