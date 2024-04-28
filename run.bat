@echo off
rmdir /s /q output
mkdir .\output\temp

python3 ./src/main.py ./output/image.ppm || goto failed

:succeed
echo "===RUN SUCCESS==="
ffmpeg -loglevel quiet -y -i ./output/image.ppm ./output/image.bmp
ffmpeg -f image2 -r 20 -i "./output/temp/%%01d.ppm" ./output/image.gif
exit 0

:failed
echo "===RUN FAIL==="
exit 1