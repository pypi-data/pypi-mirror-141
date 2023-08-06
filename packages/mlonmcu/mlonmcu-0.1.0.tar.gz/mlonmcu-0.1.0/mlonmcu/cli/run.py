"""Command line subcommand for the run process."""

import multiprocessing
import concurrent
import copy
import itertools

import mlonmcu
from mlonmcu.cli.common import (
    add_common_options,
    add_context_options,
    add_flow_options,
    kickoff_runs,
)
from mlonmcu.flow import SUPPORTED_FRAMEWORKS, SUPPORTED_FRAMEWORK_BACKENDS
from mlonmcu.cli.compile import (
    handle as handle_compile,
    add_compile_options,
)
from mlonmcu.flow.backend import Backend
from mlonmcu.flow.framework import Framework
from mlonmcu.session.run import RunStage

# rom mlonmcu.flow.tflite.framework import TFLiteFramework
# from mlonmcu.flow.tvm.framework import TVMFramework
# from mlonmcu.cli.compile import handle as handle_compile


def add_run_options(parser):
    add_compile_options(parser)
    run_parser = parser.add_argument_group("run options")


def get_parser(subparsers):
    """ "Define and return a subparser for the run subcommand."""
    parser = subparsers.add_parser(
        "run",
        description="Run model using ML on MCU flow. This is meant to reproduce the bahavior of the original `run.py` script in older versions of mlonmcu.",
    )
    parser.set_defaults(flow_func=handle)
    add_run_options(parser)
    return parser


def check_args(context, args):
    # print("CHECK ARGS")
    pass


def get_results(context):
    assert len(context.sessions) > 0
    session = context.sessions[-1]
    results = [run.result for run in session.runs]


def handle(args):
    with mlonmcu.context.MlonMcuContext(path=args.home, lock=True) as context:
        check_args(context, args)
        handle_compile(args, context)
        kickoff_runs(args, RunStage.RUN, context)
        results = get_results(context)
