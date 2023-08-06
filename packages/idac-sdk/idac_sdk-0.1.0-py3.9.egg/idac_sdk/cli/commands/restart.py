import asyncclick as click

from idac_sdk import IDACRequestAsync
from idac_sdk.cli.lib._controller_options import _controller_options, with_controller
from idac_sdk.cli.lib._helpers import add_options


@click.group()
def commands():
    pass


@commands.command(short_help="restart a request")
@add_options(_controller_options)
@click.argument("request_id")
@with_controller
async def restart(controller, request_id):
    """Restart request

    REQUEST_ID - id/uuid of the request"""
    req = IDACRequestAsync(uuid=request_id, controller=controller)
    await req.restart()
    click.echo("Request restarted")
