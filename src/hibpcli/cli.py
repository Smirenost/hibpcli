import click
from hibpcli.exceptions import ApiError
from hibpcli.keepass import check_passwords_from_db
from hibpcli.password import Password


@click.group()
def main():
    """Command line interface to the haveibeenpwned.com API."""
    pass


@click.command()
@click.argument("path")
@click.option("--password", default=None, help="Password for the KeePass database.")
def check_keepass(path, password):
    """Check all passwords stored in the keepass database."""
    if password is None:
        password = click.prompt(
            "Please enter the master password for the database", hide_input=True
        )
    try:
        rv = check_passwords_from_db(path=path, master_password=password)
    except ApiError as e:
        click.echo(str(e))
    else:
        if rv:
            click.echo("The passwords of following entries are leaked:")
            click.echo(rv)
        else:
            click.echo("Hooray, everything is safe!")


@click.command()
@click.option("--password", default=None, help="Password which should be checked.")
def check_password(password):
    """Check a single password."""
    if password is None:
        password = click.prompt(
            "Please enter a password which should be checked", hide_input=True
        )
    p = Password(password)
    try:
        is_leaked = p.is_leaked()
    except ApiError as e:
        click.echo(str(e))
    else:
        if is_leaked:
            click.echo("Please change your password!")
        else:
            click.echo("Your password is safe!")


main.add_command(check_keepass)
main.add_command(check_password)


if __name__ == "__main__":
    main()
