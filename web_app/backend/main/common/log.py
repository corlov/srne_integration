
#import logging

#logging.basicConfig(level=logging.DEBUG, filename='backend.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

L_DEBUG = 0
L_INFO = 2
L_WARNING = 3
L_ERROR = 4
L_CRITICAL = 5


def logmsg(msg, level=L_INFO, arg=None):
    print(msg)
    if level == L_DEBUG:
        #logging.debug(msg)
        pass
    else:
        #logging.info(msg)
        pass



