import logging
logger = logging.getLogger("chose_setting")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')

#logfile= logging.FileHandler("../log.txt")
logfile= logging.FileHandler("../logs/settings.log")
logfile.setFormatter(formatter)
#logfile.setLevel(logging.DEBUG)
logger.addHandler(logfile)
