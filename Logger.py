class Logger:
    LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    level = "DEBUG"

    @staticmethod
    def debug(message):
        Logger.log(message, log_level="DEBUG")

    @staticmethod
    def info(message):
        Logger.log(message, log_level="INFO")

    @staticmethod
    def warning(message):
        Logger.log(message, log_level="WARNING")

    @staticmethod
    def error(message):
        Logger.log(message, log_level="ERROR")

    @staticmethod
    def critical(message):
        Logger.log(message, log_level="CRITICAL")

    @staticmethod
    def log(message, log_level="INFO"):
        if log_level not in Logger.LOG_LEVELS:
            raise ValueError(f"Invalid log level: {log_level}")

        if Logger.LOG_LEVELS.index(log_level) >= Logger.LOG_LEVELS.index(Logger.level):
            print(f"[{log_level}] - {message}")
