"""Main entry point for font converter CLI application."""

from presentation.cli import app
from bootstrap import create_container


def main() -> None:
    """Run the CLI application after wiring dependencies."""
    container = create_container()
    container.wire(modules=["presentation.cli"])

    app()


if __name__ == "__main__":
    main()
