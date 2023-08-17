

class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

    def setup_logger(level: Union[str, int] = "DEBUG"):
        logging.basicConfig(
            handlers=[InterceptHandler()],
            level=logging.getLevelName(level)
        )
        for ignore in ignored:
            logger.disable(ignore)
        logger.info('Logging is successfully configured')

