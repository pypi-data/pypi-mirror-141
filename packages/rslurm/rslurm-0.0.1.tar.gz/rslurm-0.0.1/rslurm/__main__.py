import click

from rslurm import rslurm
from rslurm.config import load_config


@click.group(invoke_without_command=True)
@click.option('-c', '--config', default='rslurm.yaml', help='The path to config file.')
@click.pass_context
def main(ctx, config):
    """Command line entry point.

    Parameters
    ----------
    config : str
        Path to config file.
    """
    ctx.ensure_object(dict)
    config = load_config(path=config)
    ctx.obj['CONFIG'] = config
    # rslurm.rsync(config)


@main.command()
@click.pass_context
def list(ctx):
    """List all the runs."""
    config = ctx.obj['CONFIG']
    rslurm.list(config)


@main.command()
@click.pass_context
def delete(ctx):
    """Delete all the runs."""
    config = ctx.obj['CONFIG']
    rslurm.delete(config)


@main.command()
@click.pass_context
def upload(ctx):
    """Copy the folder and the command on that folder."""
    config = ctx.obj['CONFIG']
    rslurm.upload(config)


@main.command()
@click.pass_context
def download(ctx):
    """Copy the folder and the command on that folder."""
    config = ctx.obj['CONFIG']
    rslurm.download(config)


@main.command()
@click.pass_context
def sync(ctx):
    """Copy the folder and the command on that folder."""
    config = ctx.obj['CONFIG']
    rslurm.upload(config)
    rslurm.download(config)


@main.command()
@click.pass_context
def config(ctx):
    cfg = ctx.obj['CONFIG']
    click.echo(cfg)


if __name__ == '__main__':
    main()
