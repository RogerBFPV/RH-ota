rm index* > /dev/null 2>&1
[ "$(ping -c 1 8.8.8.8 | grep '100% packet loss' )" != "" ]
wget www.google.com
sleep 2
exit