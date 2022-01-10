

# main function of get data

from datetime import datetime as dtm
from datetime import timedelta as dtmdt
from sensor.dt_handle 

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
	













#=============================================================================
if __name__=='__main__':

	run()











