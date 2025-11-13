"""Main entry point for font converter CLI application."""

from bootstrap import create_container


def main() -> None:
    """Run the CLI application after constructing dependencies."""
    container = create_container()

    # Build CLI via the container and run it. No module wiring required
    # because CLI is constructed with explicit constructor injection.
    cli = container.cli()
    cli.run()


if __name__ == "__main__":
    main()
