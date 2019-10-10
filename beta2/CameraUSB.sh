#！ /bin/sh
cd /home/pi/IntelligentAgriculture/mjpg-streamer/mjpg-streamer-experimental

ssh -fN -R 10005:localhost:8080 root@121.41.19.125

./mjpg_streamer -i "./input_uvc.so" -o "./output_http.so -w ./www"