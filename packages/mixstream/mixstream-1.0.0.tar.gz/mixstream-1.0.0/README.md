# MixStream

[![Build Status](https://travis-ci.org/fofix/python-mixstream.svg?branch=master)](https://travis-ci.org/fofix/python-mixstream)
[![Tests](https://github.com/fofix/python-mixstream/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/fofix/python-mixstream/actions/workflows/tests.yml)


MixStream is a C-extension in Python to combine [SoundTouch](https://www.surina.net/soundtouch/) and [SDL_mixer](https://www.libsdl.org/projects/SDL_mixer/).


## History

- 2019/07/25: Replace the Python StreamingOggSound class with the OggStreamer module
(See: https://github.com/fofix/fofix/commit/e4d9f3209af1d350237c4baddba3cfbd5e576d8f).


## Setup

### Dependencies

You'll need those packages:

* `glib`
* `libogg`
* `libtheora`
* `libvorbisfile`
* `sdl 1.2`
* `sdl_mixer 1.2`
* `soundtouch`.


### Native modules

Build the extension:

    python setup.py build_ext --inplace --force
