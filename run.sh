fname="image"

while getopts ":o:" opt; do
	case $opt in
	o)
		fname="$OPTARG"
		;;
	esac
done

if ! [ -d "./output/" ]; then
	mkdir "./output/"
fi

if [ -d "./output/$fname" ]; then
	rm -rf "./output/$fname"
fi

mkdir  "./output/$fname"
mkdir  "./output/$fname/temp"
mkdir  "./output/$fname/energy"

pypy3 ./src/main.py "$@"

if [ $? -eq 0 ]; then
	echo "===RUN SUCCESS==="
	if [ -e "./output/$fname/$fname.ppm" ]; then
		ffmpeg -loglevel quiet -y -i "./output/$fname/$fname.ppm" "./output/$fname/$fname.bmp"
		if [ -e "./output/$fname/temp/0.ppm" ]; then
			ffmpeg -loglevel quiet -f image2 -r 20 -i "./output/$fname/temp/%01d.ppm" "./output/$fname/$fname.gif"
			ffmpeg -loglevel quiet -f image2 -r 20 -i "./output/$fname/energy/%01d.ppm" "./output/$fname/${fname}_energymap.gif"
		fi
	else
		if [ -e "./output/$fname/temp/0.jpg" ]; then
			ffmpeg -loglevel quiet -f image2 -r 20 -i "./output/$fname/temp/%01d.jpg" "./output/$fname/$fname.gif"
		fi
	fi
	display "./output/$fname/$fname.bmp"
else
	echo "===RUN FAIL==="
	exit 1
fi
