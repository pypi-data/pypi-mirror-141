"""
@package utils.exception

Module with custom excpetion and for handling exception in multiprocessing
"""

import traceback
from mfire.settings import get_logger

# Logging
LOGGER = get_logger(name="config_processor.mod", bind="config_processor")


class PrometheeError(Exception):
    """Base class promethee's custom exception"""

    def __init__(self, err, **kwargs):
        self.err = err
        for key, value in kwargs.items():
            if value is None:
                continue
            try:
                self.err += " {}={}.".format(key, value)
            except Exception:
                LOGGER.exception(
                    "Exception caught in PrometheeError execution", exc_info=True,
                )
        super().__init__(self.err)


class ConfigurationError(PrometheeError):
    """Raised when a wrong configuration has been given"""

    def __init__(self, err, **kwargs):
        super().__init__(err, **kwargs)


def handle_error(excpt, log):
    """handle_error
    Cette fonction va etre utilise pour handler les erreurs de apply_async
    Le log doit être passé.
    Pour cela, definir dans le module
    module_handle_error = partial(handle_error, log=my_module_log)
    puis utiliser le callback de la maniere suivante
    pool.apply_async(my_func,args=(my_args,),error_callback=module_handle_error)


    Args:
        excpt (Error): L'erreur en question
        log (): Le logger dans lequel on va ecrire l'erreur
    """
    trace = traceback.format_exception(type(excpt), excpt, excpt.__traceback__)
    log.error(f"An error has been caught {repr(excpt)}.\n" + "".join(trace))
