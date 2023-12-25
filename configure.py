import typing as t
import secrets
import click
import string
import json
from web.app.ext.sqlalchemy.model import User

from string import Template

from web.app.utils import filesystem

APP_CONFIG_FILE = "web/instance/config.py"
INSTANCE_CONFIG_TEXT = """
SECRET_KEY = "$secret_key"
SQLALCHEMY_DATABASE_URI = "$sqlalchemy_database_uri"
"""

DOT_ENV_FILE = "web/"
DOT_ENV_TEXT = """
FLASK_DEBUG=1
APP_CONFIG=$flask_env
FLASK_RUN_PORT=$flask_port
"""

SECRETS_FOLDER = ".secrets/"
DB_ROOT_PASSWORD_FILE = "db_root_password.txt"
DB_PASSWORD_FILE = "db_password.txt"


def create_instance_config():
    secret_key: str = secrets.token_hex()

    variables: dict = {
        "secret_key": secret_key,
        "sqlalchemy_database_uri": ""
    }

    filesystem.set_file(
        APP_CONFIG_FILE,
        Template(INSTANCE_CONFIG_TEXT).substitute(variables)
    )

    click.echo(click.style("[x] %s created." % APP_CONFIG_FILE, fg="green", bold=True))


def generate_random_password(length: int = 20) -> str:
    alphabet = (string.ascii_letters + string.digits + string.punctuation
                .replace("'", "").replace('"', ""))
    password = ""
    for i in range(length):
        password += secrets.choice(alphabet)
    return password


def create_docker_secrets() -> None:
    filesystem.create_folder_if_not(SECRETS_FOLDER)

    if filesystem.has_file(f"{SECRETS_FOLDER}{DB_PASSWORD_FILE}"):
        click.echo("Looks like you already have %s" % DB_PASSWORD_FILE)
    else:
        # web db user password
        filesystem.set_file(f"{SECRETS_FOLDER}{DB_PASSWORD_FILE}", generate_random_password(32))
        click.echo(click.style("[x] created db user password for web container", fg="green", bold=True))

    if filesystem.has_file(f"{SECRETS_FOLDER}{DB_ROOT_PASSWORD_FILE}"):
        click.echo("Looks like you already have %s" % DB_ROOT_PASSWORD_FILE)
    else:
        # db root password
        filesystem.set_file(f"{SECRETS_FOLDER}{DB_ROOT_PASSWORD_FILE}", generate_random_password(32))
        click.echo(click.style("[x] created root password for db", fg="green", bold=True))


def create_dot_env() -> None:
    flask_env: t.Any = click.prompt("APP_CONFIG", default="development")

    if flask_env != "production":
        flask_port: str = click.prompt("FLASK_RUN_PORT", default="5000")
        filesystem.set_file(f"{DOT_ENV_FILE}.env", Template(DOT_ENV_TEXT).substitute({
            "flask_env": flask_env,
            "flask_port": flask_port
        }))
        click.echo(click.style("[x] .env created.", fg="green", bold=True))

    else:
        click.echo(click.style("[] .env ignored.", fg="green", bold=True))


def create_app_admin() -> None:
    admin = User()
    admin_arguments = ["username", "email", "password", "first_name", "last_name"]

    for arg in admin_arguments:
        is_valid_arg = False
        while not is_valid_arg:
            try:
                if arg == "email":
                    user_input = click.prompt(f"Enter the admin {arg}", default="")
                else:
                    user_input = click.prompt(f"Enter the admin {arg}")
                if user_input != "":
                    admin.__setattr__(arg, user_input)
            except ValueError as e:
                for error in e.args[0]:
                    click.echo(click.style(error, fg="red", bold=True))
            else:
                is_valid_arg = True
    admin_info = {
        "username": admin.username,
        "email": admin.email,
        "password": admin.password,
        "first_name": admin.first_name,
        "last_name": admin.last_name,
    }
    filesystem.set_file(f"{SECRETS_FOLDER}admin.json", json.dumps(admin_info))


@click.command()
def init_config() -> None:
    click.echo(click.style("*** Starting initial configuration ***", fg="green", bold=True))

    # instance/config.py
    if filesystem.has_file(APP_CONFIG_FILE):
        click.echo("Looks like you already have %s" % APP_CONFIG_FILE)
    else:
        create_instance_config()

    # .env
    if filesystem.has_file(".env"):
        click.echo("Looks like you already have .env")
    else:
        create_dot_env()

    # docker secrets
    click.echo(click.style("*** Now creating necessary docker secrets ***", fg="green", bold=True))
    create_docker_secrets()

    create_app_admin()

    click.echo(click.style("All done. Now you can use 'flask run'", fg="green", bold=True))

if __name__ == '__main__':
    init_config()
