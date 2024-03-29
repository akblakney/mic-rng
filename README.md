# mic-rng

## Synopsis

`mic-rng` is a program that reads raw data from the microphone and uses that data to generate random numbers in real time. Random data is output to `stdout` in raw bytes by default, but can also be output in printable ASCII characters, hexadecimal characters, alpha-numeric characters, and decimal digits. 

## Installation and Dependencies

For basic functionality of the program, the only requirements are: 

1. that Python3 is installed, and 
2. that the python library pyaudio is installed.

And for the additional plotting functionality, which allows the user to see the plot of the raw microphone data used to generate the random output, there is an additional dependency of the matplotlib library for python. This is only necessary when running the program with the `-p` flag.

Once these are satisfied, the program can be run with `python3 rng.py [OPTIONS]`. (And of course, you must have a microphone connected!). For Debian-based systems, I've provided a script, `install.sh`, that instsalls pyaudio, generates a convenient run script, and places a symbolic link to it in `/usr/local/bin`. After using the install script, users should be able to run the program with `mic-rng [OPTIONS]` (as long as `/usr/local/bin` is in your PATH, which it usually is by default).

If you install Python3 and pyaudio yourself, it is not necessary to use the install script. The install script will just put a link to an executable in your PATH so that running it will be more convenient, but you can of course do this yourself if you like.

A few notes about the install script and how to set up this program on non-Debian based systems: First, the pyaudio library likes to give verbose output errors, even when the module is working correctly. For that reason, in the run script that the install script generates, I've output all errors to `/dev/null`. If there are bugs in the program, this would prevent you from seeing the error log so keep in mind that you can always comment out the `2> /dev/null` portion of the run script to undo that. Conversely, if you do not use the install script, you may want to figure out how to suppress errors so you don't have to see them every time you run the program. (Just to be clear, these are often not actually "errors" but rather warnings that pyaudio raises. As long as you are getting output from regular usage, you should not have to worry about them).

To use the install script:

```
# make executable
chmod u+x install.sh

# run install script
./install.sh
```

For other non-Debian Linux systems, the install script should still work; the only thing you need to do is replace the `apt install` portion with your package manager.

## Usage

To get an in-depth explanation of how to use the program, as well as examples, run `python3 rng.py -h` (or alternatively `mic-rng -h` if you used the install script). Briefly, a good place to start is:

`python3 rng.py -f ascii`

OR

`mic-rng -f ascii`

which will output 64 random bytes in the form of printable ASCII characters to `stdout`.

**If the program just stalls and nothing is output:** try unplugging and re-plugging in your mic. This has happened to me before, and it is because for some reason pyaudio isn't getting your audio so the program stalls waiting for input.

## Intuition and Technical Details

Another project of mine, an [implementation](https://github.com/akblakney/Von-Neumann-randomness-extractor) of the Von Neumann extractor in C, gives a good overview of random number generators (RNGs) and the "extraction" step in them. Briefly, to make a RNG, we need two things: an entropy source, and an extraction method. The entropy source needs to be something unpredictable, like atmospheric noise or electrical noise. And the extraction method needs to take that entropy and transform it into [independent and identically distributed](https://en.wikipedia.org/wiki/Independent_and_identically_distributed_random_variables), or i.i.d., random variables. 

In this project, the entropy source will be the user's microphone, which should have enough entroypy to generate random numbers. For randomness extraction, I implement two different methods: the [Von Neumann](https://en.wikipedia.org/wiki/Randomness_extractor#Von_Neumann_extractor) randomness extractor, and a hash-based extractor. The former is more theoretical, while being less efficient; while the latter is more efficient, and the most common method of extracting randomness from noise. (The Linux kernel and many other critical cryptographic software implementations, for example, use hash-based extraction methods).

You can see yourself that running the program with the hash extraction method (with `mic-rng --hash`) is *much* faster than the default Von Neumann extractor. But I chose to keep the Von Neumann method as default because it is more theoretically interesting, and so easy to implement that you can do it yourself (whereas implementing a hash function yourself may be a bit more tiresome).

My main motivation for making this project in addition to my [previous](https://github.com/akblakney/Von-Neumann-randomness-extractor) Von Neumann extractor project mentioned above, is that the previous one is implemented in C which makes interfacing with libraries and external hardware (microphone) a bit more complicated. I think this project is cleaner in terms of functionality: Once everything is setup, there is no need to pre-record a `.wav` file to generate random numbers; in fact as long as you have a mic connected you can get output immediately with `mic-rng -f ascii` (prints random ascii characters).

Another convenient thing about Python is that they have hash functions built in, so I can include a hash extraction option out of the box, without requiring users to go install a separate hash library. The hash extraction option is a good one to have because it is far more efficient than Von Neumann extraction.

### Plotting Functionality

Any true random number generator (TRNG), as opposed to a pseudo-random number generator (PRNG), needs a physical source of entropy. This introduces a point-of-failure in the hardware. For example, in this project we use microphone input as the source of our entropy, therefoore making the assumtion that the microphone output will have enough electrical noise to prduce a random output. But suppose that our microphone is not behaving in a manner that produces a lot of entropy. Suppose it cycles through a predictable set of values—or even worse, repeats the same value (such as 0) all the time. It is important to detect this type of situation; otherwise, you will end up using predictable, potentially deterministic values assuming they are random. 

By allowing the user to visualize the raw data coming from the microphone, they can easily check that one of these scenarios is not happening. Hence the plotting functionality: with the `-p` flag, a plot of the raw waveform using `matplotlib` is plotted and shown to the user. There is no set formula to determining whether the output is entropic enough for use as the input to a RNG. The user must use some common sense: plots which look unpredictable are probably fine, while plots that have a cyclical or otherwise predictable pattern to them are probably not good.

## Examples with Output

Output 1,000 bytes (1KB) to a file:

```
$ mic-rng -n 1000 > random_data
```

Output 10,000 bytes (10KB) to a file, using hash extraction (this would take a very long time with the Von Neumann extraction mode, even with a small `byte_interval` value, but with hash extraction it takes around 11 seconds):

```
$ mic-rng -n 10000 --hash > random_data
```

Output 32 bytes worth of alpha-numeric characters:

```
$ mic-rng -f alpha-numeric -n 32
ptmjwwgw8xfnu80ea4swz6cbil7oioaq
```

Generate 64 bytes worth of printable ASCII characters, and use the plotting functionality to verify that the microphone input was entropic enough for us to reasonably consider our output random:

```
$ mic-rng -f ascii -p
xoD@qn^QOi~z^|NA:dwRE~+5EezaLbL:(jvhOH{
```

And the full plot of the microphone input:

![h](figures/full_plot.png)

And a zoomed in plot of around 1,000 values (around 0.02 seconds worth of input):

![h](figures/zoomed_in.png)

As you can see, the zoomed out version looks unpredictable overall. But what is more important is that within small areas, there is enough noise: in the zoomed in plot, the values fluctuate unpredictably due to electrical noise, which is what we want.
