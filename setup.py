import sys
from cx_Freeze import setup, Executable
import argparse
import os
import queue
import sounddevice as sd
import vosk
import sys

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
icon = "ico.ico"


#if sys.platform == "win32":
    #base = "Win32GUI"

setup(  name = "ChessVoiceCommands",
        version = "12.0",
        description = "ChessVoiceCommands!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("chess.py", base=base, icon=icon)])