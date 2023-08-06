# `create_brandon` Overview

This is a small **command line application** to help with the creation of directories for experiments or data science use.

By calling `create_brandon` in the command line, the user will be prompted to answer a few questions. `brandon` will create a directory named accordingly based on the answers to the questions. The directory will be named based on the date and time of running `create_brandon` and
will contain `data/` and `scripts/` folders as well as a jupyter notebook. If the user calls `create_brandon -v` they will meet Brandon and be welcomed to the matrix.

The application is intened for those who work with quantum devies in dilution refridgerators. Hence the questions such as _Name of the device_ and _Name of the fridge_, users can leave these blank by just hitting the <ENTER/Return> key.

## Installation

```bash
$ pip install create_brandon
```

## Usage

Enter in the command line/terminal:

```bash
$ create_brandon
```

To have a conversation with `brandon`, pass the arguments `-v` or `-verbose`, for example:

```bash
$ create_brandon -v
```

or similarly

```bash
$ create_brandon -verbose
```

Commands also work with `create-brandon` using a dash instead of an underscore.

## Output

For Example:

```
$ create_brandon

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

### Developing `create_brandon`

To install `create_brandon`, along with the tools you need to develop and run tests, run the following in your virtual env:

```bash
$ pip install -e.[dev]
```

Main requirment is `pytest==6.2.5`
