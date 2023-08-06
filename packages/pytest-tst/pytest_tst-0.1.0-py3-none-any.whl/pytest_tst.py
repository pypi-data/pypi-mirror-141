import os
import sys

import pytest
from pytest import ExitCode

@pytest.hookimpl(tryfirst=True)
def pytest_load_initial_conftests(args):
    if '--tst' in args:
        if not os.path.exists(args[-1]):
            raise pytest.UsageError("error: argument --tst expected one argument")

        args.pop() # remove module under test

    if '--full' not in args:
        args.append("--quiet")
        args.append("--no-summary")
        args.append("--color=no")
        args.append("-o console_output_style=none")
        #args.append("-s") 
        args.append("--capture=no") # --capture=no is the same as -s


def pytest_addoption(parser):
    opts = parser.getgroup('tst')
    opts.addoption('--tst',
        action='store_true',
        default=False,
        help='Customize output to run from tst.'
    )

    opts.addoption('--full',
        action='store_true',
        default=False,
        help='Don´t omit output in tst mode.'
    )


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    if session.config.getoption('--tst'):
        if exitstatus == ExitCode.TESTS_FAILED: # or exitstatus == ExitCode.NO_TESTS_COLLECTED:
            session.exitstatus = ExitCode.OK
