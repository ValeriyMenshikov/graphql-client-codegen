import sys
import click
from graphql_codegen.runner import run


@click.group()
def main():
    """
    GraphQL Codegen
    """
    pass


@main.command(
    context_settings=dict(
        ignore_unknown_options=True,
    )
)
@click.option(
    "-u",
    "--url",
    required=True,
    help="url"
)
@click.option(
    "-o",
    "--output_dir",
    default="generated_schemas",
    required=False,
    help="Target directory name for GraphQL schema",
)
@click.option(
    "-s",
    "--service_name",
    default="api",
    required=False,
    help="module and class name for you graphql api",
)
@click.option(
    "-m",
    "--make_tests",
    default=False,
    required=False,
    help="Target directory name for GraphQL schema",
)
# @click.argument("settings", nargs=-1, type=click.UNPROCESSED)
def gen(*args, **kwargs):
    """
    Generate GraphQL client

    Command examples:
        graphql_codegen gen -u http://localhost:5051/graphql
    """
    return run(*args, **kwargs)


if __name__ == "__main__":
    _args = sys.argv
    if "--help" in _args or len(_args) == 1:
        print("GraphQL Codegen")
    main()
