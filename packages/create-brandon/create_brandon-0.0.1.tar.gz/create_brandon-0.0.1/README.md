# `create-brandon` Overview

> Documentation can be found [here](https://create-brandon-project.readthedocs.io/).

This is a small **command line application** to help with the creation of directories for experiments or data science use.

By calling `create-brandon` in the command line, the user will be prompted to answer a few questions. `brandon` will create a directory named accordingly based on the answers to the questions. The directory will be named based on the date and time of running `create-brandon` and
will contain `data/` and `scripts/` folders as well as a jupyter notebook. If the user calls `create-brandon -v` they will meet Brandon and be welcomed to the matrix.

The application is intened for those who work with quantum devies in dilution refridgerators. Hence the questions such as _Name of the device_ and _Name of the fridge_, users can leave these blank by just hitting the <ENTER/Return> key.

## Installation

```bash
$ pip install create-brandon
```

## Usage

Enter in the command line/terminal:

```bash
$ create-brandon
```

To have a conversation with `brandon`, pass the arguments `-v` or `-verbose`, for example:

```bash
$ create-brandon -v
```

or similarly

```bash
$ create-brandon -verbose
```

**N.B.** Commands also work with `create_brandon` using an underscore instead of a dash. The package name is `create_brandon`.

## Output

For Example:

```
$ create-brandon

Name of the fridge: triton1
Name of the device: sige_heterostructure 1
Name of the experiment: fine_tuning
Creating directories...
Experiment directory made at: 20220308_154655_triton1_sige_heterostructure_1_fine_tuning
```

Directory structure is as follows:

```
20220308_154655_triton1_sige_heterostructure_1_fine_tuning/
├── 20220308_154655_triton1_sige_heterostructure_1_fine_tuning.ipynb
├── data
└── scripts
```

## Contributions

MIT license, so feel free to fork submit PRs and contribute, inluding help with docs 😎.

### Developing `create-brandon`

To install `create-brandon`, along with the tools you need to develop and run tests, run the following in your virtual env:

```bash
$ pip install -e.[dev]
```

Main requirment is `pytest==6.2.5`
