import logging

def getLogging(logger=None):
    logger_=logging.getLogger(logger)
    if not logger_.handlers:
        logger_.setLevel(logging.DEBUG)
        fh = logging.FileHandler("./log.log")
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(filename)-18s %(funcName)-18s [line:%(lineno)5d] %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        logger_.addHandler(fh)
        logger_.addHandler(ch)
        logger_.propagate=0
    return logger_

def test():
    log=getLogging()
    log.info("test")
    log.info("test")

def test2():
    log=getLogging("XD")
    log.info("test")
    log.info("test")

if __name__ == '__main__':
    test()
    test2()