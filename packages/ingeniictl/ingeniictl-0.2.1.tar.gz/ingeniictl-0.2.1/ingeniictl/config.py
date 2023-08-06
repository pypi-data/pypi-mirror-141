from os import getenv

# Logging
II_LOG_ENABLE_COLORS = bool(int(getenv("II_LOG_ENABLE_COLORS", 1)))
II_LOG_ENABLE_DATETIME_PREFIX = bool(int(getenv("II_LOG_ENABLE_DATETIME_PREFIX", 1)))
