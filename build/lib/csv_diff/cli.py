import click
import json as std_json
from . import load_csv, load_json, compare, human_text


@click.command()
@click.version_option()
@click.argument(
    "previous",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, allow_dash=False),
)
@click.argument(
    "current",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, allow_dash=False),
)
@click.option(
    "--keys", type=str, default=None, help="Column to use as a unique ID for each row"
)

@click.option(
    "--charset", type=str, default="utf-8", help="Import CSV charset.(JSON must specify utf-8)"
)

@click.option(
    "--trim",
    is_flag=True,
    default=True,
    help="Trim field value"
)

@click.option(
    "--reverse",
    is_flag=False,
    default=False,
    help="Reverse first input file"
)

@click.option(
    "--format",
    type=click.Choice(["csv", "tsv", "json"]),
    default=None,
    help="Explicitly specify input format (csv, tsv, json) instead of auto-detecting",
)
@click.option(
    "--json", type=bool, default=False, help="Output changes as JSON", is_flag=True
)
@click.option(
    "--singular",
    type=str,
    default=None,
    help="Singular word to use, e.g. 'tree' for '1 tree'",
)
@click.option(
    "--plural",
    type=str,
    default=None,
    help="Plural word to use, e.g. 'trees' for '2 trees'",
)
@click.option(
    "--show-unchanged",
    is_flag=True,
    help="Show unchanged fields for rows with at least one change",
)
def cli(previous, current, keys, charset, trim, reverse, format, json, singular, plural, show_unchanged):
    "Diff two CSV or JSON files"
    dialect = {
        "csv": "excel",
        "tsv": "excel-tab",
    }
    keys = split_key(keys)

    def load(filename):
        if format == "json":
            return load_json(open(filename), keys=keys)
        else:
            csv_file = open(filename, newline="",encoding=charset, errors="ignore")
            return load_csv(csv_file, keys=keys, dialect=dialect.get(format),trim=trim,charset=charset)

    previous_file = load(previous)
    current_file = load(current)
    diff = compare(previous_file, current_file, show_unchanged)
    if json:
        print(std_json.dumps(diff, indent=4))
    else:
        print(human_text(diff, keys, singular, plural))

def split_key(keys):
    if keys:
        return keys.split(",")
    else:
        return None