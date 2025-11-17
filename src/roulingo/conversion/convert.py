import clingo
import datetime
import pandas
import pathlib
import typing


def convert_instance_csvs(
    csv_directory: pathlib.Path,
    output_instance: pathlib.Path,
    duration_factor: int,
    currency_factor: int,
) -> None:
    converted = []
    nodes = construct_nodes(
        pandas.read_csv(csv_directory / "nodes.csv"),
        currency_factor,
    )
    converted.extend(nodes)
    arcs = construct_arcs(
        pandas.read_csv(csv_directory / "arcs.csv"),
        duration_factor,
        currency_factor,
    )
    converted.extend(arcs)
    demands = construct_demands(
        pandas.read_csv(csv_directory / "demands.csv"),
        duration_factor,
        currency_factor,
    )
    converted.extend(demands)
    months, start_ordinal = construct_months(
        pandas.read_csv(csv_directory / "months.csv"),
        duration_factor,
    )
    converted.extend(months)
    vehicles = construct_vehicles(pandas.read_csv(csv_directory / "vehicles.csv"))
    converted.extend(vehicles)
    availabilities = construct_availabilities(
        pandas.read_csv(csv_directory / "availabilities.csv"),
        duration_factor,
        start_ordinal,
    )
    converted.extend(availabilities)
    output_converted_instance(converted, output_instance)


def output_converted_instance(
    predicates: list[clingo.Symbol],
    output_instance: pathlib.Path,
) -> None:
    output_instance.parent.mkdir(parents=True, exist_ok=True)
    with open(output_instance, "w+") as output_file:
        output_file.writelines(
            str(clingo.Function("data", [predicate])) + ".\n"
            for predicate in sorted(predicates)
        )


def construct_nodes(
    data: pandas.DataFrame,
    currency_factor: int,
) -> list[clingo.Function]:
    data["ID"] = data["ID"].apply(convert_id)
    data.loc[data["Cost"].notna(), "Cost"] *= currency_factor
    data = data.replace({float("nan"): None})
    return convert_into_predicates(data, "node")


def construct_arcs(
    data: pandas.DataFrame,
    duration_factor: int,
    currency_factor: int,
) -> list[clingo.Function]:
    data["Origin ID"] = data["Origin ID"].apply(convert_id)
    data["Destination ID"] = data["Destination ID"].apply(convert_id)
    data["Vehicle ID"] = data["Vehicle ID"].apply(convert_id)
    data["Cost"] *= currency_factor
    data["Duration (Days)"] *= duration_factor
    return convert_into_predicates(data, "arc")


def construct_demands(
    data: pandas.DataFrame,
    duration_factor: int,
    currency_factor: int,
) -> list[clingo.Function]:
    data.reset_index(inplace=True, names="Index")
    data["Origin ID"] = data["Origin ID"].apply(convert_id)
    data["Destination ID"] = data["Destination ID"].apply(convert_id)
    data["Month"] = data["Month"].apply(convert_month_to_ordinal)
    data["Revenue Per Unit"] *= currency_factor
    data["Min Frequency (Days)"] *= duration_factor
    data["Max Transit (Days)"] *= duration_factor
    return convert_into_predicates(data, "demand")


def construct_months(
    data: pandas.DataFrame,
    duration_factor: int,
) -> tuple[list[clingo.Function], int]:
    data["Month"] = data["Month"].apply(convert_month_to_ordinal)
    data["Start"] = data["Start"].apply(convert_date_to_ordinal)
    data["End"] = data["End"].apply(convert_date_to_ordinal)
    start_ordinal = data["Start"].min()
    data["Start"] = (data["Start"] - start_ordinal) * duration_factor
    data["End"] = (data["End"] - start_ordinal) * duration_factor
    return convert_into_predicates(data, "month"), start_ordinal


def construct_vehicles(data: pandas.DataFrame) -> list[clingo.Function]:
    data["ID"] = data["ID"].apply(convert_id)
    return convert_into_predicates(data, "vehicle")


def construct_availabilities(
    data: pandas.DataFrame,
    duration_factor: int,
    start_ordinal: int,
) -> list[clingo.Function]:
    data["Vehicle ID"] = data["Vehicle ID"].apply(convert_id)
    data["Start"] = data["Start"].apply(convert_date_to_ordinal)
    data["End"] = data["End"].apply(convert_date_to_ordinal)
    data["Start"] = (data["Start"] - start_ordinal) * duration_factor
    data["End"] = (data["End"] - start_ordinal) * duration_factor
    return convert_into_predicates(data, "available")


def convert_id(id: str) -> int:
    try:
        return int(id[1:])
    except ValueError:
        return id


def convert_month_to_ordinal(month: str) -> int:
    return datetime.datetime.strptime(month, "%B").month


def convert_date_to_ordinal(iso_date: str) -> int:
    return datetime.date.fromisoformat(iso_date).toordinal()


def convert_into_predicates(
    data: pandas.DataFrame,
    functor: str,
) -> list[clingo.Symbol]:
    def derive_clingo_arg_notation(value: typing.Any):
        try:
            return clingo.Number(int(value))
        except (ValueError, TypeError):
            if value is None:
                return clingo.Function("none", [])
            return clingo.String(str(value))

    return (
        data.map(derive_clingo_arg_notation)
        .apply(lambda row: clingo.Function(functor, row.to_list()), axis=1)
        .to_list()
    )
