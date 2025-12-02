import argparse
import itertools
import pathlib
import typing
import roulingo.conversion
import roulingo.processing
import roulingo.solving


def invoke_roulingo() -> None:
    match construct_and_parse_args():
        case {"sub": "convert", **convert_args}:
            roulingo.conversion.convert_instance_csvs(**convert_args)
        case {"sub": "process", **process_args}:
                roulingo.processing.preprocess_and_output_instance(**process_args)
        case {"sub": "solve", **solve_args}:
            roulingo.solving.construct_and_invoke_solver(**solve_args)


def construct_and_parse_args() -> dict[str, int | str | pathlib.Path]:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="sub")
    construct_conversion_args(
        subparsers.add_parser(
            "convert",
            help="convert `.csv` files into an unprocessed `.lp` instance",
        )
    )
    construct_processing_args(
        subparsers.add_parser(
            "process",
            help="preprocess an `.lp` instance",
        )
    )
    construct_solving_args(
        subparsers.add_parser(
            "solve",
            help="solve a preprocessed `.lp` instance",
        )
    )
    args, extras = parser.parse_known_args()
    if args.sub == "solve":  # Pass Clingo options to solver.
        args.configuration = extras
    return vars(args)


def construct_conversion_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "csv_directory",
        type=resolve_optional_path,
        help="path to the directory containing all input `.csv` files",
    )
    parser.add_argument(
        "output_instance",
        type=resolve_optional_path,
        help="output `.lp` file path for the converted unprocessed instance",
    )
    parser.add_argument(
        "--duration-factor",
        default=10,
        type=int,
        help="specify operand for converting floating-point duration values into integers",
    )
    parser.add_argument(
        "--currency-factor",
        default=100,
        type=int,
        help="supply currency value operand for integer conversion",
    )


def construct_processing_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "input_instance",
        type=resolve_optional_path,
        help="path to the input `.lp` database",
    )
    parser.add_argument(
        "output_instance",
        type=resolve_optional_path,
        help="output `.lp` file path for the generated instance",
    )
    parser.add_argument(
        "--config",
        nargs="?",
        const=pathlib.Path(__file__).parent
        / "processing"
        / "encodings"
        / "config.lp",
        default=None,
        type=resolve_optional_path,
        help="supply a configuration `.lp` file for extracting subset instances",
        dest="config_encoding",
        metavar="ENCODING",
    )
    parser.add_argument(
        "--duplicate",
        default=1,
        type=int,
        help="generate isolated duplicate subgraphs in instance",
        dest="duplicate_count",
        metavar="COUNT",
    )
    parser.add_argument(
        "--bounds",
        nargs=2,
        default=[7, 12],
        type=int,
        dest="range_bounds",
        metavar=("LOWER", "UPPER"),
        help="closed range to extract",
    )


def construct_solving_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "instance_path",
        type=resolve_optional_path,
        help="path to input `.lp` instance file",
        metavar="instance",
    )
    parser.add_argument(
        "--solution",
        default=None,
        type=resolve_optional_path,
        help="optional path to `.lp` solution output file",
        metavar="FILE",
        dest="solution_path",
    )
    parser.add_argument(
        "--results",
        default=None,
        type=resolve_optional_path,
        help="optional path to `.json` statistics output file",
        metavar="FILE",
        dest="statistics_path",
    )
    parser.add_argument(
        "--include-quantities",
        action="store_true",
        help="include linear constraints for quantities and vehicle capacities",
    )
    parser.add_argument(
        "--iterative-solving",
        action="store_true",
        help="solve instance by iteratively extending sub-solutions",
    )
    parser.add_argument(
        "--require-loading",
        action="store_true",
        help="require that vehicles either load or drop at every node",
    )
    parser.add_argument(
        "--include-cost",
        action="store_true",
        help="include arc traversal costs in objective",
    )
    parser.add_argument(
        "--duration",
        default=300,
        type=int,
        help="specify an upper bound on solving duration",
        dest="solve_duration",
        metavar="SECONDS",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="print solutions to standard output",
    )


def resolve_optional_path(input_path: typing.Optional[str]) -> pathlib.Path:
    if input_path is not None:
        return pathlib.Path(input_path).resolve()


if __name__ == "__main__":
    invoke_roulingo()
