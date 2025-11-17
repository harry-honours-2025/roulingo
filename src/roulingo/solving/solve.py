import clingcon
import clingo
import clingo.ast
import json
import pathlib
import threading
import time
import typing


encodings_directory = pathlib.Path(__file__).parent.resolve() / "encodings"


def construct_and_invoke_solver(
    instance_path: pathlib.Path,
    solution_path: pathlib.Path | None,
    statistics_path: pathlib.Path | None,
    solve_duration: int,
    iterative_solving: bool,
    require_loading: bool,
    include_quantities: bool,
    include_cost: bool,
    verbose: bool,
    configuration: list[str],
) -> None:
    control, theory = prepare_solver(
        instance_path,
        iterative_solving,
        include_quantities,
        configuration,
    )
    context = {"solution": None, "statistics": None, "result": clingo.SolveResult(0)}
    if not iterative_solving:
        to_ground = [("base", []), ("req" if require_loading else "opt", [])]
        if include_cost:
            to_ground.append(("cost", []))
        ground_and_handle_solving(
            control,
            context,
            theory,
            to_ground,
            solve_duration,
            verbose,
        )
    else:
        index = 0
        periods = 6
        should_continue = True
        while should_continue:
            to_ground = [
                ("base", []),
                ("inc", [clingo.Number(index)]),
                ("req" if require_loading else "opt", [clingo.Number(index)]),
            ]
            if include_cost:
                to_ground.append(("cost", [clingo.Number(index)]))
            ground_and_handle_solving(
                control, context, theory, to_ground, solve_duration / periods, verbose
            )
            should_continue = context["result"].satisfiable
            if should_continue:
                context[index] = context["statistics"]
                for predicate in context["solution"]:
                    control.assign_external(
                        clingo.Function("occurred", predicate.arguments), True
                    )
                index += 1
                should_continue = index < periods
        context["statistics"] = {}
        for index in range(periods):
            context["statistics"][index] = context[index]
            context.pop(index)
    output_results(
        context["solution"],
        solution_path,
        context["statistics"],
        statistics_path,
    )


def prepare_solver(
    instance_path: pathlib.Path,
    iterative_solving: bool,
    include_quantities: bool,
    configuration: list[str],
) -> tuple[clingo.Control, clingcon.ClingconTheory | None]:
    control = clingo.Control(configuration)
    theory = None
    if include_quantities:
        theory = clingcon.ClingconTheory()
        theory.register(control)
        with clingo.ast.ProgramBuilder(control) as builder:
            encoding_path = encodings_directory / (
                "inc_linear.lp" if iterative_solving else "base_linear.lp"
            )
            clingo.ast.parse_files(
                [str(instance_path), str(encoding_path)],
                lambda ast: theory.rewrite_ast(ast, builder.add),
            )
    else:
        encoding_path = encodings_directory / (
            "inc_enc.lp" if iterative_solving else "base_enc.lp"
        )
        control.load(str(instance_path))
        control.load(str(encoding_path))
    return control, theory


def ground_and_handle_solving(
    control: clingo.Control,
    context: dict[str, typing.Any],
    theory: clingcon.ClingconTheory | None,
    to_ground: list[tuple[str, list[clingo.Symbol]]],
    solve_duration: int,
    verbose: bool,
) -> None:
    print("Grounding…")
    control.ground(to_ground)
    if theory is not None:
        theory.prepare(control)
    solving = threading.Event()
    finished = threading.Event()
    thread = threading.Thread(
        target=solve_instance,
        args=(control, theory, context, solving, finished, verbose),
    )
    thread.start()
    solving.wait()
    thread.join(solve_duration)
    if thread.is_alive():
        context["handler"].cancel()
    finished.wait()
    context["statistics"] = control.statistics


def solve_instance(
    control: clingo.Control,
    theory: clingcon.ClingconTheory | None,
    context: dict[str, typing.Any],
    solving: threading.Event,
    finished: threading.Event,
    verbose: bool,
) -> None:
    def handle_solution(solution: clingo.Model) -> None:
        nonlocal start
        elapsed = time.time() - start
        cost = solution.cost
        if theory is not None:
            theory.on_model(solution)
            expense = 0
            revenue = theory.get_value(
                solution.thread_id,
                theory.lookup_symbol(clingo.Function("revenue", [])),
            )
            index = theory.lookup_symbol(clingo.Function("expense", []))
            if index is not None:
                expense = theory.get_value(solution.thread_id, index)
            cost.append(revenue - expense)
        context["objective"] = {"cost": cost, "elapsed": elapsed}
        context["solution"] = solution.symbols(shown=True)
        print(f"Model: {solution.number} ({elapsed:.3f}s)")
        if verbose:
            print(solution)
        if cost:
            print("Cost:", *cost)

    def update_statistics(
        step: clingo.StatisticsMap,
        accu: clingo.StatisticsMap,
    ) -> None:
        accu["result"] = context["objective"]
        context.pop("objective")

    print("Solving…")
    context["objective"] = {}
    with control.solve(
        async_=True,
        on_model=handle_solution,
        on_statistics=update_statistics,
    ) as handler:
        context["handler"] = handler
        solving.set()
        start = time.time()
        handler.wait()
        context["result"] = handler.get()
        print(context["result"])
    finished.set()


def output_results(
    solution: typing.Sequence[clingo.Symbol] | None,
    solution_path: pathlib.Path | None,
    statistics: clingo.StatisticsMap | dict[str, clingo.StatisticsMap] | None,
    statistics_path: pathlib.Path | None,
) -> None:
    if solution is not None and solution_path is not None:
        solution_path.parent.mkdir(parents=True, exist_ok=True)
        with open(solution_path, "w") as solution_file:
            for predicate in solution:
                solution_file.write(f"{predicate}.\n")
    if statistics is not None and statistics_path is not None:
        statistics_path.parent.mkdir(parents=True, exist_ok=True)
        with open(statistics_path, "w") as output_file:
            output_file.write(json.dumps(statistics, sort_keys=True, indent=4))
