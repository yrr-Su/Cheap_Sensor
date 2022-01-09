
# ----------------------------
# TClab_cheap_sensor
#	- wifi_profile (connect wi-fi auto)
#		- ntu0
#		- ntu1
#		- ...
#		- ntu9
#	- ssh_keys (ssh without password)
# ----------------------------

# Parameter
## input
$tunnel_nam = Read-Host "Please enter tunnel number"
$tunnel_nam = "ntut$tunnel_nam"

## enviroment 
$PATH_token   = "C:\Users\$env:Username\TClab_cheap_sensor"
$PATH_profile = "$PATH_token\wifi_profile"
$FILE_profile = "$PATH_profile\$tunnel_nam.xml"
$PATH_sshkey  = "$PATH_token\ssh_keys"

# check out the folder
foreach ($_path in $PATH_profile,$PATH_sshkey) {
	if ( -not( Test-Path $_path ) ) {
		mkdir $_path > $null
	}
}

# create network profile
## create profile and change name
if ( -not( Test-Path $FILE_profile ) ){
	netsh wlan export profile name=$tunnel_nam folder=$PATH_profile
	Rename-Item -Path "$PATH_profile\*$tunnel_nam.xml" -NewName "$tunnel_nam.xml"

	## add to network profile
	netsh wlan add profile filename="$PATH_profile\$tunnel_nam.xml" > $null
}

## connection test
netsh wlan connect name=$tunnel_nam > $null

if ( $? ){
	echo "connect to $tunnel_nam successfully !!!"
	echo ""
}
else {
	echo "$tunnel_nam connection failed QQ"
	echo "shutdown this script and figure out the problem"
	echo ""
	exit
}


# Syncro time
## 目前仍有問題 試試看可不可以在 pi 裡面使用
# . $PATH_token\SyncDateTime.exe

# ssh pi@192.168.127.10 -22
