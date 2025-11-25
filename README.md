# Roulingo

Hello!
Roulingo is a preprocessing and solving system for the
**transit-constraint recurring pickup and delivery problem** (TCRPDP)
based on **answer set programming** (ASP).

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

- `node/2`
- `vehicle/2`
- `availability/3`
- `arc/5`
- `month/3`
- `demand/8`

<!-- - `node(X,T)` -->
<!-- - `vehicle(V,C)` -->
<!-- - `availability(V,B,E)` -->
<!-- - `arc(X,Y,V,C,D)` -->
<!-- - `month(M,B,E)` -->
<!-- - `demand(I,X,Y,M,Q,R,F,T)` -->

#### CSV Conversion

…

#### Preprocessing

…

### Solver Invocation

…
