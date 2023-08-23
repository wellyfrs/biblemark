import click
from flask_caching import Cache

cache = Cache()


def get_cache():
    return cache


@click.command("clear-cache")
def clear_cache_command():
    cache.clear()
    click.echo("Cleared the cache")


def init_app(app):
    cache.init_app(app, config={
        "CACHE_TYPE": "FileSystemCache",
        "DEBUG": app.debug,
        "CACHE_DEFAULT_TIMEOUT": app.config["CACHE_DEFAULT_TIMEOUT"],  # 3600s = 1h
        "CACHE_DIR": app.config["CACHE_DIR"],
        "CACHE_THRESHOLD": app.config["CACHE_THRESHOLD"],
    })
    app.cli.add_command(clear_cache_command)
