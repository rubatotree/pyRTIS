@echo off
rmdir /s /q output
mkdir .\output\image
mkdir .\output\image\temp

pypy3 ./src/main.py image || goto failed

:succeed
echo "===RUN SUCCESS==="
if exist ".\output\image\image.ppm" (
    ffmpeg -loglevel quiet -y -i ./output/image/image.ppm ./output/image/image.bmp
    if exist ".\output\image\temp\0.ppm" (
        ffmpeg -f image2 -r 20 -i "./output/image/temp/%%01d.ppm" ./output/image/image.gif
    )
) else (
    if exist ".\output\image\temp\0.jpg" (
        ffmpeg -f image2 -r 20 -i "./output/image/temp/%%01d.jpg" ./output/image/image.gif
    )
)
exit 0

:failed
echo "===RUN FAIL==="
exit 1
