import yaml
import asyncclick as click
import idac_sdk
import idac_sdk.config


@click.group()
def commands():
    pass


@commands.command(short_help="configure iDAC SDK")
@click.option("-U", "--controller-url", default=None, type=str, help="URL of iDAC controller")
@click.option(
    "-P",
    "--controller-proto",
    type=click.Choice(["http", "https"], case_sensitive=False),
    default=None,
    help="Which protocol should be used to connect to controller",
)
@click.option(
    "-T",
    "--auth-type",
    type=click.Choice([e.name for e in idac_sdk.IDACAuthType], case_sensitive=False),
    help="Type of authentication",
    default=None,
)
@click.option(
    "-A",
    "--auth",
    type=str,
    help="Token if Auth Type is BEARER, base64 string if BASIC. Ignored for other auth types",
    default=None,
)
@click.option("-V", "--api-version", default=None, help="API version to use")
async def config(controller_url, controller_proto, auth_type, auth, api_version):
    current_config = idac_sdk.config.load_config()

    if not controller_url:
        controller_url = click.prompt(
            "Enter default iDAC URL",
            type=str,
            default=current_config.defaults.idac_fqdn,
        )

    if not controller_proto:
        controller_proto = click.prompt(
            "Enter default iDAC controller proto",
            type=click.Choice(["http", "https"], case_sensitive=False),
            show_choices=True,
            default=current_config.defaults.idac_proto,
        )

    if not api_version:
        api_version = click.prompt(
            "Enter default iDAC controller API version",
            type=str,
            default=current_config.defaults.api_version,
        )

    if not auth_type:
        auth_type = click.prompt(
            "Enter default iDAC auth type",
            type=click.Choice([e.name for e in idac_sdk.IDACAuthType], case_sensitive=False),
            show_choices=True,
            default=current_config.defaults.auth_type,
        )

    if auth_type in [idac_sdk.IDACAuthType.BASIC.name, idac_sdk.IDACAuthType.BEARER.name]:
        if not auth:
            auth = click.prompt(
                "Enter default base64 string (username:password) for BASIC auth"
                if auth_type == idac_sdk.IDACAuthType.BASIC.name
                else "Enter default API token for BEARER auth",
                type=str,
                hide_input=True,
                default=current_config.defaults.auth,
                value_proc=lambda val: val if val else True,
            )
            if auth is True:
                auth = ""
    else:
        auth = ""

    with open(idac_sdk.config.IDAC_CONFIG_FILE, "w") as file:
        file.write(
            yaml.dump(
                {
                    "defaults": {
                        "idac_fqdn": controller_url,
                        "idac_proto": controller_proto,
                        "auth_type": auth_type,
                        "auth": auth,
                        "api_version": api_version,
                    }
                }
            )
        )

    click.echo("Done")
