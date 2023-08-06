import pyperclip
import typer

app = typer.Typer()


@app.command()
def main():
    """
    Reads and adjusts the contents of your clipboard by normalizing the whitespace.
    """
    pyperclip.copy(" ".join(pyperclip.paste().split()))
    typer.secho(
        "✨ Clipboard contents have been whitespace-normalized!", fg=typer.colors.MAGENTA
    )
