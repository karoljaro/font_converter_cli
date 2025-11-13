"""Composition root / DI container for the application."""

from dependency_injector import containers, providers

from application.use_cases.convert_font_use_case import ConvertFontUseCase
from infrastructure.adapters.file_service import FileService
from infrastructure.adapters.fonttools_converter import FontToolsConverter
from infrastructure.adapters.output_path_resolver import OutputPathResolver
from presentation import FontConverterCLI


class Container(containers.DeclarativeContainer):
    """Dependency injection container for application wiring."""

    file_service = providers.Singleton(FileService)
    font_converter = providers.Singleton(FontToolsConverter)
    output_path_resolver = providers.Singleton(OutputPathResolver)

    convert_use_case = providers.Factory(
        ConvertFontUseCase,
        converter=font_converter,
        file_service=file_service,
    )

    # CLI constructed with DI-friendly class
    cli = providers.Factory(
        FontConverterCLI,
        use_case=convert_use_case,
        output_path_resolver=output_path_resolver,
    )


def create_container() -> Container:
    return Container()
