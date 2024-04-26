python3 ./src/main.py ./output/image.ppm

if [ $? -eq 0 ]; then
	echo "===RUN SUCCESS==="
	display ./output/image.ppm
else
	echo "===RUN FAIL==="
	exit 1
fi
