import logging

@property
def log(obj):
    logger = logging.getLogger("Feeder")
    handler = logging.StreamHandler()
    handler.setFormatter(CustomFormatter())
    logger.addHandler(handler)
    return logger

class CustomFormatter():
    grey = "\x1b[38;5;8m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[38;20m"
    cyan = "\x1b[38;5;49m"
    reset = "\x1b[0m"
    format = "%(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    info_format = "--------------------------------------------------\nINFO: %(message)s\n--------------------------------------------------"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: cyan + info_format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

        
