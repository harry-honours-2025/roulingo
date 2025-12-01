# Roulingo

Hello!
Roulingo is a preprocessing and solving system for the
**transit-constraint recurring pickup and delivery problem** (TCRPDP)
based on [**answer set programming**](https://potassco.org) (ASP).

- [Installation](#installation)
- [Usage](#usage)
    - [Instance Construction](#instance-construction)
        - [CSV Conversion](#csv-conversion)
        - [Preprocessing](#preprocessing)
    - [Solver Invocation](#solver-invocation)

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
> Invoke `roulingo --help` for an overview of available sub-commands.

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

The facts …

#### Preprocessing

…

### Solver Invocation

…
