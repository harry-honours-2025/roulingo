# Roulingo

Hello!
Roulingo is a preprocessing and solving system for the
**transit-constraint recurring pickup and delivery problem** (TCRPDP)
based on [**answer set programming**](https://potassco.org) (ASP).

<!--
    - [Installation](#installation)
    - [Usage](#usage)
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

…

> [!TIP]
> Run `roulingo --help` for an overview of available sub-commands.

### Instance Construction

An **instance** is defined by the following facts:

- **Nodes** `node(X,T)` where:
    - `X` is a unique node identifier,
    - `T` is the transshipment cost per unit of demand.

- **Vehicles** `vehicle(V,C)` where:
    - `V` is a unique vehicle identifier,
    - `C` is the vehicle's capacity.

- **Availability periods** `availability(V,B,E)` where:
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

The facts outlined above can be optionally generated using CSV files.
Example CSV files are included in the [`data/csv`](https://github.com/harry-honours-2025/harry-thesis-software/tree/main/data/csv) directory.
These examples have been used to populate the [`instances`](https://github.com/harry-honours-2025/harry-thesis-software/tree/main/instances) directory.

The `roulingo convert` command generates an ASP instance from these CSV files.
For example:

```console
$ roulingo convert data/csv data/test.lp
```

> [!IMPORTANT]
> The CSV file names and column headings must correspond **exactly** to the
> [examples provided](https://github.com/harry-honours-2025/harry-thesis-software/tree/main/data/csv).

This command generates the [`data/tiny.lp`](https://github.com/harry-honours-2025/harry-thesis-software/blob/main/data/tiny.lp)
file using the CSV files included in the [`data/csv`](https://github.com/harry-honours-2025/harry-thesis-software/tree/main/data/csv) directory.
Note that converted facts are wrapped by the `data/1` atom;
these must be [preprocessed](#preprocessing) before solving can occur.

Because ASP only supports integers,
two options are available for the `roulingo convert` command.
These define constant multipliers for converting real numbers into integers:


- `--duration-factor` is 10 by default, and applies to all **temporal values**:
    - Arc traversal durations
    - Minimum pickup frequencies
    - Maximum transit durations

- `--currency-factor` is 100 by default, and applies to:
    - Arc traversal costs
    - Revenues per unit

> [!TIP]
> Run `roulingo convert --help` for an breakdown of CSV conversion arguments.

#### Preprocessing

…

### Solver Invocation

…
