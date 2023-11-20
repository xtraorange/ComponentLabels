class Logger:
    log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
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
        if log_level not in Logger.log_levels:
            raise ValueError(f"Invalid log level: {log_level}")

        if Logger.log_levels.index(log_level) >= Logger.log_levels.index(Logger.level):
            print(f"[{log_level}] - {message}")
