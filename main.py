from hieroglyph.create import create_input
from hieroglyph.parse import (
    parse_elastic_differential_cross_section,
    parse_dwba_differential_cross_section,
)
from pathlib import Path
import click


@click.group()
def cli():
    click.echo("------- Hieroglph: The PTOLEMY translator -------")


@cli.command()
@click.argument("config", type=click.Path(exists=True))
def create(config: str):
    click.echo(f"Generating a PTOLEMY input file from configuration: {config}")
    create_input(Path(config))
    click.echo("-------------------------------------------------")


@cli.command()
@click.argument("ptolemy_path", type=click.Path(exists=True))
@click.argument("parsed_path", type=click.Path())
def parse_elastic(ptolemy_path: str, parsed_path: str):
    click.echo(f"Parsing the PTOLEMY elastic scattering output file {ptolemy_path}")
    click.echo(f"Output will be written to {parsed_path}")
    parse_elastic_differential_cross_section(Path(ptolemy_path), Path(parsed_path))
    click.echo("-------------------------------------------------")


@cli.command()
@click.argument("ptolemy_path", type=click.Path(exists=True))
@click.argument("parsed_path", type=click.Path())
def parse_dwba(ptolemy_path: str, parsed_path: str):
    click.echo(f"Parsing the PTOLEMY DWBA scattering output file {ptolemy_path}")
    click.echo(f"Output will be written to {parsed_path}")
    parse_dwba_differential_cross_section(Path(ptolemy_path), Path(parsed_path))
    click.echo("-------------------------------------------------")


if __name__ == "__main__":
    cli()
