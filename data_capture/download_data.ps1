





## function box
## ---------------------------

## log file to record the data which has downloaded



## ---------------------------



# . SyncDateTime.exe



# scp pi@192.168.127.10 -22:log/
# scp pi@192.168.127.10:./.bashrc ./


# scp pi@192.168.127.10:  file 

#
$key_location = 'C:\Users\yrr\Desktop\yrr\education\NTU\reasearch\EE\my_work\Cheap_Sensor\data_capture\ntut3_private_key'
# scp -i $key_location pi@192.168.127.10: file download_location
scp -i $key_location pi@192.168.127.10:.bashrc C:\Users\yrr\Desktop\yrr\education\NTU\reasearch\EE\my_work\Cheap_Sensor\data_capture\