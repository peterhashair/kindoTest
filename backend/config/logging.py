from enum import StrEnum
import logging

LOG_FORMAT_DEBUG = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

class LogLevels(StrEnum):
    debug = "DEBUG"
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"
    
    
def configure_logging(log_level: LogLevels = LogLevels.info):
   
   log_level = str(log_level).upper()
   log_levels = [level.value for level in LogLevels]
   
   if log_level not in log_levels:
       logging.basicConfig(level=LogLevels.error)
       return 
   
   if log_level == LogLevels.debug:
       logging.basicConfig(level=log_level, format=LOG_FORMAT_DEBUG)
       
   
   logging.basicConfig(level=log_level)