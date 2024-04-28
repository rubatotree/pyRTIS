cd ./output
rm -r *
cd ../
mkdir ./output/temp

python3 ./src/main.py ./output/image.ppm

if [ $? -eq 0 ]; then
	echo "===RUN SUCCESS==="
	ffmpeg -loglevel quiet -y -i ./output/image.ppm ./output/image.bmp
	ffmpeg -loglevel quiet -f image2 -r 20 -i ./output/temp/%01d.ppm ./output/image.gif
	display ./output/image.ppm
else
	echo "===RUN FAIL==="
	exit 1
fi
