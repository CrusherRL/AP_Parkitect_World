import logging
logger = logging.getLogger("Archipelago")

class LoggerHelper:
  @staticmethod
  def log(thing, subject = ""):
    logger.info(f"----- {subject} -----")
    logger.info(thing)
    logger.info(f"----- {subject} -----")
    logger.info("")

  @staticmethod
  def info(thing):
    logger.info(thing)
    logger.info("")
