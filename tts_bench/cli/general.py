import click
from tts_bench.cli import MultipleArgsOption

@click.group()
def cli():
    """tts-bench CLI tool."""
    pass

@cli.command()
def version():
    """Show version."""
    click.echo("tts-bench-v0.1.0")


@cli.command()

@click.option("--models", '-m', cls=MultipleArgsOption, help="The list of tts models for evaluation.")

@click.option("--metrics", '-M', cls=MultipleArgsOption, help="The list of metric for evaluation of the tts models.")

@click.option("--input", '-i', default=None, help="The path to the file containing the text intended to test the tts models. *Ignored if a suit is selected.")

@click.option("--suit", '-s', cls=MultipleArgsOption, help="The preset of test cases for evaluation of TTS models")

@click.option("--output", '-o', default='output.html', help="The path to the output file")

@click.argument('remaining_args', nargs=-1)

def run(models, metrics, input, suit, output, remaining_args):
    click.echo(f'{(models)} models will be tested')
    click.echo(f'{(metrics)} metrics will be used to the test the models')
    print(remaining_args)
    if suit:
        click.echo(f'The test will use the {suit} suit')
    elif input: 
        click.echo(f'The test will use the input from {input}')
    else: 
        raise click.BadParameter('Either a suit or an input text file should be used for testing')
    
    


def main():
    cli()