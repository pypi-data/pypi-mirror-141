import asyncclick as click

from idac_sdk import IDACRequestAsync
from idac_sdk.cli.lib._controller_options import _controller_options, with_controller
from idac_sdk.cli.lib._helpers import add_options


@click.group()
def commands():
    pass


@commands.command(short_help="get state of a request")
@add_options(_controller_options)
@click.argument("request_id")
@with_controller
async def state(controller, request_id):
    """Get JSON state object of a request

    REQUEST_ID - id/uuid of the request"""
    req = IDACRequestAsync(uuid=request_id, controller=controller)
    state = await req.get_state()
    click.echo(state.json())


@commands.command(short_help="get status of a request")
@add_options(_controller_options)
@click.argument("request_id")
@with_controller
async def status(controller, request_id):
    """Get current status of a request

    REQUEST_ID - id/uuid of the request"""
    req = IDACRequestAsync(uuid=request_id, controller=controller)
    state = await req.get_state()
    click.echo(state.status)
