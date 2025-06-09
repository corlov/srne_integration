
import logging
import uuid

logging.basicConfig(level=logging.DEBUG, filename='solar_monitor.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Account for negative temperatures.
def getRealTemp(temp):
    if(temp/int(128) > 1):
        return -(temp%128)
    return temp

L_DEBUG = 0
L_INFO = 2
L_WARNING = 3
L_ERROR = 4
L_CRITICAL = 5


def logmsg(msg, level=L_INFO, arg=None):
    print(msg)

    if level == L_DEBUG:
        logging.debug(msg)
    else:
        logging.info(msg)



def modbus_crc(data: bytes) -> int:
    crc = 0xFFFF
    
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    
    return crc


def get_mac_addr():
    mac_address = uuid.getnode()  # Returns MAC as 48-bit integer
    formatted_mac = ':'.join(['{:02x}'.format((mac_address >> elements) & 0xff) for elements in range(0,8*6,8)][::-1])
    return formatted_mac

