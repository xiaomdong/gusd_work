import logging

def getLogging(logger=None):
    logging.basicConfig(filename='log.log', level=logging.INFO,
                        format='%(asctime)s %(filename)-15s %(funcName)-15s [line:%(lineno)5d] %(message)s')
    # # 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(filename)-15s %(funcName)-15s [line:%(lineno)5d] %(message)s')
    console.setFormatter(formatter)
    logging.getLogger(logger).addHandler(console)

    return logging.getLogger(logger)

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