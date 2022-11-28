# mic-rng

## Synopsis

`mic-rng` is a program that reads raw data from the microphone and uses that data to generate random numbers in real time. Random data is output to `stdout` in raw bytes by default, but also in printable ASCII characters, hexadecimal characters, alpha-numeric characters, and decimal digits. 

## Installation and Dependencies

The only requirements are that Python3 is installed, and that the python library pyaudio is installed. Once these are installed, the program can be run with `python3 rng.py [OPTIONS]`. For Debian-based systems, I've provided a script, `install.sh`, that instsalls pyaudio, generates a convenient run script, and places a symbolic link to it in `/usr/local/bin`. After using the install script, users should be able to run the program with `mic-rng [OPTIONS]` (as long as `/usr/local/bin` is in your PATH, which it usually is by default).

**Therefore, for non-Debian based systems, run with `python3 rng.py [OPTIONS]`, and with those who use the install script on Debian-based systems, run with `mic-rng [OPTIONS]`.**

A few notes about the install script and how to set up this program on non-Debian based systems: First, the pyaudio library likes to give verbose output errors, even when the module is working correctly. For that reason, in the run script that the install script generates, I've output all errors to `/dev/null`. If there are bugs in the program, this would prevent you from seeing the error log so keep in mind that you can always comment out the `2> /dev/null` portion of the run script to undo that. Conversely, if you are not using a Debian-based system, you may want to figure out how to suppress errors so you don't have to see them every time you run the program. (Just to be clear, these are often not actually "errors" but rather warnings that pyaudio raises. As long as you are getting output from regular usage, you should not have to worry about them).

## Usage

To get an in-depth explanation of how to use the program, as well as examples, run `python3 rng.py -h` (or alternatively `mic-rng -h` if you used the install script). Briefly, a good place to start is:

`python3 rng.py -f ascii`

OR

`mic-rng -f ascii`

which will output 64 random bytes in the form of printable ASCII characters to `stdout`.

## Intuition and Technical Details















