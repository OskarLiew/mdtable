from pathlib import Path
from typing import Callable

import pandas as pd
import typer

app = typer.Typer()

suffix_map: dict[str, Callable[[Path], pd.DataFrame]] = {
    ".csv": pd.read_csv,
    ".xlsx": pd.read_excel,
    ".json": pd.read_json,
}


@app.command()
def main(path: Path, index: bool = typer.Option(False, "-i", "--index")) -> None:
    if not path.exists():
        typer.echo("Error: File does not exist")
        raise typer.Exit(1)

    read_fn = suffix_map.get(path.suffix)
    if read_fn is None:
        typer.echo(
            f"Error: Invalid suffix. Should be one of {', '.join(suffix_map.keys())}"
        )
        raise typer.Exit(1)

    df = read_fn(path)
    typer.echo(df.to_markdown(index=index))


if __name__ == "__main__":
    app()
