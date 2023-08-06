import asyncclick as click

import idac_sdk.cli.commands.status as status_set
import idac_sdk.cli.commands.restart as restart_set
import idac_sdk.cli.commands.cleanup as cleanup_set
import idac_sdk.cli.commands.create as create_set
import idac_sdk.cli.commands.extend as extend_set
import idac_sdk.cli.commands.config as config_set


@click.group()
async def cli():
    """Group for CLI commands"""
    pass


def main():
    m = click.CommandCollection(
        sources=[
            cli,
            create_set.commands,
            cleanup_set.commands,
            status_set.commands,
            restart_set.commands,
            extend_set.commands,
            config_set.commands,
        ]
    )
    m(_anyio_backend="asyncio")


if __name__ == "__main__":
    main()
