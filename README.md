# Cython Example

Use [Cython](https://cython.org/) to compile the [Python 3](https://www.python.org/) sources to C/C++ shared libraries and executables.

# Prerequisites

- Python/Conda
- Cython
- GCC/G++

# Get Started

See [setup-3.7.py](setup-3.7.py) or [setup-3.9.py](setup-3.9.py), and create a `set.py` to your python source folder. It will act as the `Makefile` for the build.

```shell
python3 setup.py build_ext --cython-c-in-temp -j 6
```

The build directory looks like the tree structure below.

```text
build/
├── lib.linux-x86_64-3.9
│   ├── fib.cpython-39-x86_64-linux-gnu.so
│   ├── hello.cpython-39-x86_64-linux-gnu.so
│   ├── logic.cpython-39-x86_64-linux-gnu.so
│   └── main
└── temp.linux-x86_64-3.9
    ├── build
    │   └── temp.linux-x86_64-3.9
    │       └── pyrex
    │           ├── fib.o
    │           ├── hello.o
    │           └── logic.o
    └── pyrex
        ├── fib.c
        ├── hello.c
        ├── logic.c
        └── main.c
```