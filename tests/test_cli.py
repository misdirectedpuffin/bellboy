"""Tests related to the cli entrypont."""

from click.testing import CliRunner
from bellboy.cli import entrypoint


def test_cli_output():
    """It returns the CLI description."""
    runner = CliRunner()
    runner.invoke(entrypoint)
    assert 'Entrypoint to your CLI.'
