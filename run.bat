@echo off
set fname=image

:parse_opts
if "%~1"=="" goto end_parse_opts
if "%~1"=="-o" (
    shift
    set fname=%~1
    shift
    goto parse_opts
)
shift
goto parse_opts
:end_parse_opts

if not exist ".\output\" (
    mkdir ".\output\"
)

if exist ".\output\%fname%" (
    rmdir /s /q ".\output\%fname%"
)

mkdir ".\output\%fname%"
mkdir ".\output\%fname%\temp"
mkdir ".\output\%fname%\energy"

pypy3 .\src\main.py %*

if %errorlevel% equ 0 (
    echo ===RUN SUCCESS===
    if exist ".\output\%fname%\%fname%.ppm" (
        ffmpeg -loglevel quiet -y -i ".\output\%fname%\%fname%.ppm" ".\output\%fname%\%fname%.bmp"
        if exist ".\output\%fname%\temp\0.ppm" (
            ffmpeg -loglevel quiet -f image2 -r 20 -i ".\output\%fname%\temp\%%01d.ppm" ".\output\%fname%\%fname%.gif"
            ffmpeg -loglevel quiet -f image2 -r 20 -i ".\output\%fname%\energy\%%01d.ppm" ".\output\%fname%\%fname%_energymap.gif"
        )
    ) else (
        if exist ".\output\%fname%\temp\0.jpg" (
            ffmpeg -loglevel quiet -f image2 -r 20 -i ".\output\%fname%\temp\%%01d.jpg" ".\output\%fname%\%fname%.gif"
        )
    )
    start ".\output\%fname%\%fname%.bmp"
) else (
    echo ===RUN FAIL===
    exit /b 1
)