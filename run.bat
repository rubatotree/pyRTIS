@echo off
set "fname=image"

:parse_args
if "%~1" == "" goto start_process
if "%~1" == "-o" (
    set "fname=%~2"
    shift
    shift
    goto parse_args
)
goto start_process

:start_process
if not exist ".\output\" (
    mkdir ".\output\"
)

if exist ".\output\%fname%\" (
    rd /s /q ".\output\%fname%"
)

mkdir ".\output\%fname%"
mkdir ".\output\%fname%\temp"

pypy3 .\src\main.py %*

if %errorlevel% equ 0 (
    echo ===RUN SUCCESS===
    if exist ".\output\%fname%\%fname%.ppm" (
        ffmpeg -loglevel quiet -y -i ".\output\%fname%\%fname%.ppm" ".\output\%fname%\%fname%.bmp"
        if exist ".\output\%fname%\temp\0.ppm" (
            ffmpeg -loglevel quiet -f image2 -r 20 -i ".\output\%fname%\temp\%%01d.ppm" ".\output\%fname%\%fname%.gif"
        )
    ) else (
        if exist ".\output\%fname%\temp\0.jpg" (
            ffmpeg -loglevel quiet -f image2 -r 20 -i ".\output\%fname%\temp\%%01d.jpg" ".\output\%fname%\%fname%.gif"
        )
    )
) else (
    echo ===RUN FAIL===
    exit /b 1
)
