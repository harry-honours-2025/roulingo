import clingo
import pathlib
import string
import typing


class PreprocessingContext:
    def append_letter(
        self,
        arg: clingo.Number,
        index: clingo.Number,
        dup: clingo.Number,
    ) -> clingo.Symbol:
        if dup.number <= 1:
            return arg
        # Todo: test!
        return clingo.Function(string.ascii_lowercase[index.number - 1] + str(arg.number), [])


def preprocess_and_output_instance(
    input_instance: pathlib.Path,
    output_instance: pathlib.Path,
    config_encoding: pathlib.Path | None,
    duplicate_count: int,
    range_bounds: list[int],
) -> None:
    def output_processed_instance(solution):
        predicates = [
            predicate.arguments[0] for predicate in sorted(solution.symbols(shown=True))
        ]
        horizon = max(
            predicate.arguments[2].number
            for predicate in predicates
            if predicate.name == "month"
        )
        with open(output_instance, "w+") as output_file:
            indentation = " " * 3
            output_file.write("%*\n")
            output_file.write(indentation + f"#const dup = {duplicate_count}.\n")
            if config_encoding is not None:  # Preference supplied config encoding.
                with open(config_encoding) as config_file:
                    output_file.write("\n")
                    output_file.writelines(
                        indentation + line for line in config_file.readlines()
                    )
            else:
                output_file.write(indentation + f"#const first = {bound_1}.\n")
                output_file.write(indentation + f"#const last = {bound_2}.\n")
            output_file.write("*%\n")
            output_file.write(f"#const horizon={horizon}.\n")
            output_file.writelines(f"{predicate}.\n" for predicate in predicates)

    output_instance.parent.mkdir(parents=True, exist_ok=True)
    bound_1, bound_2 = range_bounds
    control = clingo.Control(
        [
            "-c",
            f"dup={duplicate_count}",
            "-c",
            f"first={bound_1}",
            "-c",
            f"last={bound_2}",
        ]
    )
    control.load(
        str(pathlib.Path(__file__).parent / "encodings" / "preprocess.lp")
    )
    control.load(str(input_instance))
    if config_encoding is not None:  # Preference supplied config encoding.
        control.load(str(config_encoding))
    else:
        control.add("""
        drop(month(M,B,E)) :-
           data(month(M,B,E)),
           M < first.

        drop(month(M,B,E)) :-
           data(month(M,B,E)),
           M > last.
        """)
    control.ground(context=PreprocessingContext())
    control.solve(on_last=output_processed_instance)
