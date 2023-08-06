import asyncclick as click

from idac_sdk import IDACRequestAsync
from idac_sdk.cli.lib._controller_options import _controller_options, with_controller
from idac_sdk.cli.lib._helpers import add_options


@click.group()
def commands():
    pass


@commands.command(short_help="cleanup a request")
@add_options(_controller_options)
@click.option("-f", "--force", is_flag=True, default=False, help="Use force cleanup")
@click.argument("request_id")
@with_controller
async def cleanup(controller, request_id, force):
    """Execute STOP tasks of a request

    REQUEST_ID - id/uuid of the request"""
    req = IDACRequestAsync(uuid=request_id, controller=controller)
    if force:
        await req.force_cleanup()
        click.echo("Started force cleanup")
    else:
        await req.cleanup()
        click.echo("Started cleanup")
