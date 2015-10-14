#!/usr/bin/env bash

# this scirpt monitors network connection state and speeks out when it changes
# Requires : espeak
# How to use:
# start  it in a terminal : ./probenet.sh
# to exit : press CTRL+C

espeak --version > /dev/null
if [ $? -ne 0 ]; then
    echo "ERROR:espeak not found; Please install it and run again"
    exit 1
fi

inet_host="google.com"
probe_delay=2 #seconds
speak=true
timeout=3 #sec

state_now='true'
state_old='true'


function probe_connection {
    state_old="$state_now"
    ping -c 1 -W $timeout $inet_host > /dev/null
    [[ $? -eq 0 ]] && state_now='true' || state_now='false'
}


function message {
    msg="$1"
    echo "`date` :: $msg"
    espeak "$msg"
}

message "Started monitoring network connection state."

while :
do
    probe_connection
    #echo $inet_host old $state_old now $state_now
    if [ "$state_now" != "$state_old" ]; then
	#state got changed
	if [ "$state_now" = 'false' ]; then
	    message "Attention, net connection went down"
	elif [ "$state_now" = 'true' ];	then
	    message "Good news, net connection is back and up"
	fi
    elif [ "$state_now" = 'false' ]; then
	#state remained false
	message "Net is down"
    fi
    sleep $probe_delay
done

echo "Exited.."
