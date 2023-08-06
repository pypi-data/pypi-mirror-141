import coloredlogs
import logging


def get_logger(env=None, file_path=None, filemode='w'):
    if env is not None:
        if "LOG_LEVEL" in env:
            options = env.get("LOG_LEVEL")
        else:
            options = "INFO"
    else:
        options = "INFO"
    levels = {
            'critical': logging.CRITICAL,
            'error': logging.ERROR,
            'warn': logging.WARNING,
            'warning': logging.WARNING,
            'info': logging.INFO,
            'debug': logging.DEBUG
    }
    level = levels.get(options.lower())
    if level is None:
        raise ValueError(
            f"log level given: {options}"
            f" -- must be one of: {' | '.join(levels.keys())}")
    if options.lower() == "info":
        format='%(asctime)s,%(msecs)d - %(name)s %(levelname)-8s %(message)s'
    else:
        format='%(asctime)s,%(msecs)d - %(name)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
    if file_path is None:
        logging.basicConfig(format=format,
                            datefmt='%Y-%m-%d:%H:%M:%S',
                            level=level)
    else:
        logging.basicConfig(filename=file_path,
                            filemode=filemode,
                            format=format,
                            datefmt='%Y-%m-%d:%H:%M:%S',
                            level=level)
    coloredlogs.install(fmt=format, level=level)
    logger = logging.getLogger('TRANSFORMATION_TOOL_LOG')
    return logger


