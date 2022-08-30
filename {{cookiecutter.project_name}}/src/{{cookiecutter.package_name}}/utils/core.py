import inspect
import logging
import os
import traceback
from pathlib import Path
from types import FrameType
from typing import Any, Dict, List, Tuple, Union

from dependency_injector import containers, providers


# See https://stackoverflow.com/questions/251464/how-to-get-a-function-name-as-a-string
def get_function_name() -> Any:
    return traceback.extract_stack(None, 2)[0][2]


def get_function_parameters_and_values() -> List[Tuple[str, Any]]:
    args: List[str] = []
    values: Dict[str, Any] = {}
    current_frame: Union[FrameType, None] = inspect.currentframe()
    if current_frame is not None:
        if current_frame.f_back is not None:
            frame: FrameType = current_frame.f_back
            args, _, _, values = inspect.getargvalues(frame)
    return [(i, values[i]) for i in args]


class Core(containers.DeclarativeContainer):
    config = providers.Configuration()

    logging = providers.Resource(
        logging.basicConfig,
        level=config.default.logging_level,
        filename=config.default.logfile,
        filemode=config.default.filemode,
        format=config.default.format,
    )


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    core = providers.Container(
        Core,
        config=config,
    )


def find_config_file( filename: str, package_home: str) -> str:
    """Search for configuration file [filename] in the following directories (highest first):
        - explicit path (if given)
        - current working directory
        - directory pointed to by environment variable CSP_TOOLS_HOME

    Args:
        filename (str): full or partial name of configuration file

    Returns:
        str: full path to configuration file or empty string if not found
    """

    result: str = ""
    p = Path(filename)
    # Check explicit path first
    if p.exists() and p.is_file():
        result = str(p.resolve())
        return result

    # Check in current working directory
    p = Path.cwd() / filename
    if p.exists() and p.is_file():
        result = str(p.resolve())
        return result

    # Check in PACKAGE_HOME directory
    if os.environ[package_home]:
        p = Path(os.environ[package_home]) / filename
        if p.exists() and p.is_file():
            result = str(p.resolve())
            return result

    return result
