import click
from click.testing import CliRunner

from graphql_codegen.cli import gen


def test_tool():
    runner = click.testing.CliRunner()

    result = runner.invoke(gen, ['-u', 'http://localhost:5051/graphql', '-o', 'output'])
    print(result.output.strip())
    assert result.exit_code == 0
    assert result.output.strip()
