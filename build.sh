#!/bin/bash
echo "========================================"
echo "FL Studio Clone - Build Script"
echo "========================================"
echo ""

echo "[1/3] Installing Python dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install Python dependencies"
    exit 1
fi
echo "Python dependencies installed successfully."
echo ""

echo "[2/3] Compiling C++ Audio Engine..."
if command -v g++ &> /dev/null; then
    g++ -std=c++17 -O2 -shared -fPIC audio_engine.cpp -o audio_engine.so -lpthread
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to compile C++ audio engine"
        exit 1
    fi
    echo "C++ audio engine compiled successfully."
else
    echo "WARNING: g++ not found. Skipping C++ compilation."
    echo "To compile C++ code, install build-essential."
fi
echo ""

echo "[3/3] Compiling C# MIDI Controller..."
if command -v mcs &> /dev/null; then
    mcs -target:library -out:MidiController.dll MidiController.cs
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to compile C# MIDI controller"
        exit 1
    fi
    echo "C# MIDI controller compiled successfully."
else
    echo "WARNING: mcs (Mono C# compiler) not found. Skipping C# compilation."
    echo "To compile C# code, install mono-complete or dotnet SDK."
fi
echo ""

echo "========================================"
echo "Build Complete!"
echo "========================================"
echo ""
echo "To run the application:"
echo "  python3 main.py"
echo ""