


import pickle as pkl
from pathlib import PurePath as Path
from matplotlib.pyplot import subplots, close, show
import json as jsn

# parameter
PATH_DT = Path('data')

# read data
with open(PATH_DT/'meta.json')

with open(PATH_DT/'sensor_dt.pkl','rb') as f:
	sen = pkl.load(f)

with open(PATH_DT/'station_dt.pkl','rb') as f:
	sta = pkl.load(f)


# plot
## time series
## one axes one compound

## Temperature

## Humidity

