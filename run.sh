cd ./output
rm -r *
cd ../
mkdir ./output/image
mkdir ./output/image/temp

# python3 ./src/main.py ./output/image.ppm
pypy3 ./src/main.py image

if [ $? -eq 0 ]; then
	echo "===RUN SUCCESS==="
	if [ -e "./output/image/image.ppm" ]; then
		ffmpeg -loglevel quiet -y -i ./output/image/image.ppm ./output/image/image.bmp
		if [ -e "./output/image/temp/0.ppm" ]; then
			ffmpeg -loglevel quiet -f image2 -r 20 -i ./output/image/temp/%01d.ppm ./output/image/image.gif
		fi
	else
		if [ -e "./output/image/temp/0.jpg" ]; then
			ffmpeg -loglevel quiet -f image2 -r 20 -i ./output/image/temp/%01d.jpg ./output/image/image.gif
		fi
	fi
	display ./output/image/image.bmp
else
	echo "===RUN FAIL==="
	exit 1
fi
