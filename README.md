# Roulingo

Hello!
Roulingo is a preprocessing and solving system for the
**transit-constraint recurring pickup and delivery problem** (TCRPDP)
based on [**answer set programming**](https://potassco.org) (ASP).

- [Installation](#installation)
- [Usage](#usage)

<!--
        - [Instance Construction](#instance-construction)
            - [CSV Conversion](#csv-conversion)
            - [Preprocessing](#preprocessing)
        - [Solver Invocation](#solver-invocation)
-->

## Installation

The Roulingo package should be installed locally after cloning this repository.
It requires **Python 3.10** or above.
Once the repository has been cloned,
navigate to the directory and run:

```console
$ pip install .
```

> [!NOTE]
> You may need to use `python3` and `pip3` instead of `python` and `pip`,
> depending on your system.

To install Roulingo into a virtual environment, and avoid modifying your system-wide Python installation:

```console
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install .
```

> [!NOTE]
> Refer to [this table](https://docs.python.org/3/library/venv.html#how-venvs-work) for the correct `source` command on your system.

Finally, to verify your installation:

```console
$ roulingo --help
```

## Usage

Roulingo provides three subcommands:

1. [`convert`](#csv-conversion) generates an instance from input data
2. [`process`](#preprocessing) preprocesses the instance
3. [`solve`](#solver-invocation) runs the solver on a preprocessed instance

> [!TIP]
> Run `roulingo --help` to view all available subcommands and their options.

### Instance Construction

An **instance** is defined by the following facts:

- **Nodes** `node(X,T)` where:
    - `X` is a unique node identifier,
    - `T` is the transshipment cost per unit of demand.

- **Vehicles** `vehicle(V,C)` where:
    - `V` is a unique vehicle identifier,
    - `C` is the vehicle's capacity.

- **Availability periods** `available(V,B,E)` where:
    - `V` is a vehicle identifier,
    - `B` is the start date of the availability period,
    - `E` is the end date of the availability period.

- **Arcs** `arc(X,Y,V,C,D)` where:
    - `X` is the origin node,
    - `Y` is the destination node,
    - `V` is the vehicle identifier,
    - `C` is the travel cost of the arc,
    - `D` is the travel duration.

- **Months** `month(M,B,E)` where:
    - `M` is a month identifier,
    - `B` is the date the month begins,
    - `E` is the date the month ends.

- **Demands** `demand(I,X,Y,M,Q,R,F,T)` where:
    - `I` is a unique demand identifier,
    - `X` is the origin node,
    - `Y` is the destination node,
    - `M` is the month of availability,
    - `Q` is the total quantity demanded,
    - `R` is the revenue per unit delivered,
    - `F` is the minimum pickup frequency,
    - `T` is the maximum transit time.

> [!NOTE]
> Transshipment is not currently supported,
> and transshipment costs `T` for each node `node(X,T)` are ignored.

Example instances are provided in the [`instances`](https://github.com/harry-honours-2025/harry-thesis-software/tree/main/instances) directory.

#### CSV Conversion

The facts described above can also be generated from CSV files.
Example CSVs are provided in the [`data/csv`](https://github.com/harry-honours-2025/harry-thesis-software/tree/main/data/csv) directory,
and these have been used to create the instances in [`instances`](https://github.com/harry-honours-2025/harry-thesis-software/tree/main/instances).

Use `roulingo convert` to build an ASP instance from a directory of CSV files. For example:

```console
$ roulingo convert data/csv data/test.lp
```

> [!IMPORTANT]
> CSV file names and column headings must match the
> [provided examples](https://github.com/harry-honours-2025/harry-thesis-software/tree/main/data/csv) exactly.

Running this command generates [`data/tiny.lp`](https://github.com/harry-honours-2025/harry-thesis-software/blob/main/data/tiny.lp).
All generated facts are wrapped in the `data/1` atom; these must be [preprocessed](#preprocessing) before solving.

Because ASP does not support real numbers,
two additional options for `roulingo convert` define multipliers for converting them into integers:

- The `--duration-factor` (default: 10) applies to:
    - Arc traversal durations
    - Minimum pickup frequencies
    - Maximum transit durations

- The `--currency-factor` (default: 100) applies to:
    - Arc traversal costs
    - Revenues per unit

For example, `--duration-factor 100` will convert an arc duration of 3.84 into 384.

> [!TIP]
> Run `roulingo convert --help` for a breakdown of the `convert` subcommand.

#### Preprocessing

Once an instance has been generated using `roulingo convert`,
it should be preprocessed using `roulingo process` to eliminate redundancies in the input data.
The `process` subcommand also supports several auxiliary operations:

- [Duplicating instances](#duplicating-instances)
- [Extracting sub-instances](#extracting-sub-instances)

> [!TIP]
> Run `roulingo process --help` for a breakdown of the `process` subcommand.

##### Duplicating Instances

Independent duplicates of an instance's underlying network can be generated using the `--duplicate` option.
For example, `--duplicate 2` produces a single instance containing two identical, disconnected copies of all nodes,
vehicles, arcs, and demands from the original instance.

The following command preprocesses `input.lp`, duplicating the instance twice:

```console
$ roulingo process input.lp output.lp --duplicate 2
```

Given the following unprocessed `input.lp` instance:

```answer-set-programming
data(node(1,none)).
data(node(2,none)).
data(vehicle(1,10)).
data(available(1,1,31)).
data(arc(1,2,1,0,2)).
data(arc(2,1,1,0,2)).
data(month(0,1,31)).
data(demand(0,1,2,0,100,4,10,5)).
```

Preprocessing produces the following `output.lp` instance.
All nodes, vehicles, availabilities, arcs, and demands have been duplicated and renamed,
with a prefix indicating the sub-network to which each copy belongs:

```answer-set-programming
node(a1).
node(a2).
node(b1).
node(b2).
vehicle(a1,10).
vehicle(b1,10).
available(a1,0,30).
available(b1,0,30).
month(0,0,30).
arc(a1,a2,a1,0,2).
arc(a2,a1,a1,0,2).
arc(b1,b2,b1,0,2).
arc(b2,b1,b1,0,2).
demand(a0,a1,a2,0,100,4,10,5).
demand(b0,b1,b2,0,100,4,10,5).
```

> [!NOTE]
> All preprocessing configuration options are recorded at the top of the generated output file.

This feature is primarily intended for the generation of benchmarking instances.

##### Extracting Sub-instances

…

### Solver Invocation

…
