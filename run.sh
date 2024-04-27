rm ./output/image.ppm
python3 ./src/main.py ./output/image.ppm

if [ $? -eq 0 ]; then
	echo "===RUN SUCCESS==="
	ffmpeg -loglevel quiet -y -i ./output/image.ppm ./output/image.bmp
	display ./output/image.ppm
else
	echo "===RUN FAIL==="
	exit 1
fi
