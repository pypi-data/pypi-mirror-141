import os
import sys
import logging
import colorlog
import traceback
from datetime import datetime


def get_root_log_level():
    """
    Log level of root logger
    :return:
    DEBUG: all logs
    INFO: except debug, all logs
    WARNING: except debug, info and warning, all logs
    ERROR: only error and critical logs
    CRITICAL: only critical logs
    """
    return os.environ.get("ROOT_LOG_LEVEL", "DEBUG")


def get_current_log_level():
    """
    Log Level of the modules you write and whose logs you want to print
    :return:
    DEBUG: all logs
    INFO: except debug, all logs
    WARNING: except debug, info and warning, all logs
    ERROR: only error and critical logs
    CRITICAL: only critical logs
    """
    return os.environ.get("CURRENT_LOG_LEVEL", "DEBUG")


def get_log_depth():
    """
    Specifies which logs you want to see. Logs of modules only you typed or all logs
    :return:
    deep: for all logs
    current: for logs of modules you typed
    """
    return os.environ.get("LOG_DEPTH", 'deep')


def get_logger():
    """
    It creates logger, using which you can see the logs of the modules written by you separately
    :return:
    logger: Logger Object
    """
    root_log_level = get_root_log_level()
    current_log_level = get_current_log_level()
    logging.root.setLevel(root_log_level)
    logger = logging.getLogger('logger')
    logger.setLevel(current_log_level)
    all_loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    if get_log_depth() == "current":
        for logr in all_loggers:
            logr.addFilter(logging.Filter('logger'))
    format_str = "[%(asctime)s — %(filename)s — %(funcName)s:%(lineno)d] — %(levelname)s  — %(message)s"
    date_format = '%Y-%m-%d %H:%M:%S'
    bold_seq = '\033[1m'
    color_log_format = f'{bold_seq} %(log_color)s {format_str}'
    colorlog.basicConfig(format=color_log_format, datefmt=date_format)
    return logger


def prepare_log(message, code=""):
    """
    It gives a different look to your logs so that you can easily identify them.
    :param message: message you want to log
    :param code: error code if you want to log error (optional)
    :return:
    styled log message
    """
    if code:
        message = f"|~| {message}, error_code: {code} |~|"
    else:
        message = f"|~| {message} |~|"
    return message


def prepare_exception_log(message="", code=""):
    """
    This gives a different look to the exception traceback so that you can read them easily.
    :param message: extra message you want to log (optional)
    :param code: error code if you want to log error (optional)
    :return:
    styled exception traceback
    """
    if code:
        message = f"|~| {message}, error_code: {code} |~|"
    else:
        message = f"|~| {message} |~|"
    exc_type, exc_value, exc_traceback = sys.exc_info()
    error = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
    traceback_details = {
        'timestamp': datetime.utcnow().strftime('%Y-%m-%s %H:%M:%S'),
        'custom_message': message,
        'error_trace': error
    }
    return str(traceback_details)
