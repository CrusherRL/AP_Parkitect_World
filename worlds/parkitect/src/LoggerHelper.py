import logging
from ..data.constants import DEBUG

logger = logging.getLogger("Archipelago")

class LoggerHelper:
  @staticmethod
  def log(thing, subject = ""):
    if DEBUG:
      logger.info(f"----- {subject} -----")
      logger.info(thing)
      logger.info(f"----- {subject} -----")
      logger.info("")

  @staticmethod
  def info(thing):
    if DEBUG:
      logger.info(thing)
      logger.info("")
