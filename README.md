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

…


## Usage

…

> [!TIP]
> Invoke `roulingo --help` for an overview of available sub-commands.

### Instance Construction

An **instance** is defined by the following facts:

- **Nodes** `node(X,T)` where:
    - `X` is a unique identifier,
    - `T` denotes the transshipment cost per unit of demand.

- **Vehicles** `vehicle(V,C)` where:
    - `V` is a unique identifier,
    - `C` denotes the vehicle’s capacity.

- **Availability periods** `availability(V,B,E)` where:
    - `V` is a vehicle identifier,
    - `B` is the start date of the availability period,
    - `E` is the end date of the availability period.

- **Arcs** `arc(X,Y,V,C,D)` where:
    - `X` is the origin node,
    - `Y` is the destination node,
    - `V` is the vehicle identifier,
    - `C` is the travel cost on the arc,
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

#### CSV Conversion

The facts …

#### Preprocessing

…

### Solver Invocation

…
