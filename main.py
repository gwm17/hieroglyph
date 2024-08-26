from hieroglyph.create import create_input
from hieroglyph.parse import (
    parse_elastic_differential_cross_section,
    parse_dwba_differential_cross_section,
)
from pathlib import Path
import click


@click.group()
def cli():
    """Hieroglyph is a tool to create and parse PTOLEMY files"""


@cli.command()
@click.argument("config", type=click.Path(exists=True))
def create(config: str):
    """Create a PTOLEMY input file given a JSON configuration

    CONFIG is the JSON configuration file
    """
    click.echo("------- Hieroglyph: The PTOLEMY translator -------")
    click.echo(f"Generating a PTOLEMY input file from configuration: {config}")
    create_input(Path(config))
    click.echo("-------------------------------------------------")


@cli.command()
@click.argument("ptolemy_path", type=click.Path(exists=True))
@click.argument("parsed_path", type=click.Path())
def parse_elastic(ptolemy_path: str, parsed_path: str):
    """Parse the PTOLEMY output from an elastic calculation

    \b
    PTOLEMY_PATH is the path to the PTOLEMY output
    PARSED_PATH is the path to which the parsed result will be written
    """
    click.echo("------- Hieroglyph: The PTOLEMY translator -------")
    click.echo(f"Parsing the PTOLEMY elastic scattering output file {ptolemy_path}")
    click.echo(f"Output will be written to {parsed_path}")
    parse_elastic_differential_cross_section(Path(ptolemy_path), Path(parsed_path))
    click.echo("-------------------------------------------------")


@cli.command()
@click.argument("ptolemy_path", type=click.Path(exists=True))
@click.argument("parsed_path", type=click.Path())
def parse_dwba(ptolemy_path: str, parsed_path: str):
    """Parse the PTOLEMY output from a DWBA calculation

    \b
    PTOLEMY_PATH is the path to the PTOLEMY output
    PARSED_PATH is the path to which the parsed result will be written
    """
    click.echo("------- Hieroglyph: The PTOLEMY translator -------")
    click.echo(f"Parsing the PTOLEMY DWBA scattering output file {ptolemy_path}")
    click.echo(f"Output will be written to {parsed_path}")
    parse_dwba_differential_cross_section(Path(ptolemy_path), Path(parsed_path))
    click.echo("-------------------------------------------------")


if __name__ == "__main__":
    cli()
