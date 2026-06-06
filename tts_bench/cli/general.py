import click
from tts_bench.cli.multiple_args_option import MultipleArgsOption
from tts_bench.benchmark import Benchmark
from tts_bench.suites import load_suite
from tts_bench.report import generate_report


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
@click.option("--metrics", '-M', cls=MultipleArgsOption, help="The list of metrics for evaluation of the tts models.")
@click.option("--voice-sample", '-v', default=None, help="Path to a voice sample file for models that require one.")
@click.option("--kokoro-voice-identifier", '-kv', default='af_heart', help="Identifier for Kokoro Voice.")
@click.option("--vits-speaker", '-vts', default='p225', help="Identifier for Kokoro Voice.")
@click.option("--input", '-i', default=None, help="Path to a text file to use as input. Ignored if a suite is selected.")
@click.option("--suit", '-s', default=None, help="Name of a built-in test suite.")
@click.option("--output", '-o', default='output.html', help="Path to the output report file.")
@click.option("--demo-output", '-d', default=None, metavar="DIR", help="Save raw audio output under DIR/<model>/<text>.wav for demo comparison.")
@click.argument('remaining_args', nargs=-1)
def run(models, metrics, voice_sample, kokoro_voice_identifier, vits_speaker, input, suit, output, demo_output, remaining_args):
    if suit:
        texts = load_suite(suit)
    elif input:
        with open(input) as f:
            texts = [line for line in f.read().splitlines() if line.strip()]
    else:
        raise click.BadParameter("Either --suit or --input must be provided.")

    try:
        bench = Benchmark(
                model_names=list(models), 
                metric_names=list(metrics), 
                voice_sample=voice_sample,
                kokoro_voice_identifier=kokoro_voice_identifier,
                demo_output_dir=demo_output,
                vits_speaker=vits_speaker,
            )
    except ValueError as e:
        raise click.BadParameter(str(e))

    results = bench.run(texts)
    generate_report(results, output)
    click.echo(f"Report written to {output}")
    if demo_output:
        click.echo(f"Demo audio saved under {demo_output}")


def main():
    cli()