@echo off
echo ========================================
echo FL Studio Clone - Build Script
echo ========================================
echo.

echo [1/3] Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)
echo Python dependencies installed successfully.
echo.

echo [2/3] Compiling C++ Audio Engine...
where g++ >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: g++ not found. Skipping C++ compilation.
    echo To compile C++ code, install MinGW or MSYS2.
) else (
    g++ -std=c++17 -O2 -shared -fPIC audio_engine.cpp -o audio_engine.dll -lpthread
    if %errorlevel% neq 0 (
        echo ERROR: Failed to compile C++ audio engine
        pause
        exit /b 1
    )
    echo C++ audio engine compiled successfully.
)
echo.

echo [3/3] Compiling C# MIDI Controller...
where csc >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: csc (C# compiler) not found. Skipping C# compilation.
    echo To compile C# code, install .NET SDK or Visual Studio.
) else (
    csc /target:library /out:MidiController.dll MidiController.cs
    if %errorlevel% neq 0 (
        echo ERROR: Failed to compile C# MIDI controller
        pause
        exit /b 1
    )
    echo C# MIDI controller compiled successfully.
)
echo.

echo ========================================
echo Build Complete!
echo ========================================
echo.
echo To run the application:
echo   python main.py
echo.
pause