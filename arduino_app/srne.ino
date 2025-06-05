#include <Arduino.h>
#include <CRC32.h>
#include <ArduinoJson.h>    // https://github.com/bblanchon/ArduinoJson
#include <ModbusMaster.h>   // https://github.com/4-20ma/ModbusMaster
#include <SoftwareSerial.h> // Software serial for modbus.

/*
    Pins to use for software serial for talking to the charge controller through the MAX3232.
*/
#define MAX3232_RX 2 // RX pin.
#define MAX3232_TX 3 // TX pin.

/*
    Modbus Constants
    All charge controllers will respond to address 255 no matter what their actual address is, this is useful if you do not know what address to use.
    You can try using 1 here instead of 255 if you don't want to make changes to the library, but it is not guaranteed to work.
*/
#define NUM_REGISTERS 35
#define MODBUS_SLAVE_ADDR 2 //255
#define MODBUS_REQUEST_START_ADDR 256

/*
    Other settings.
*/
#define REQUEST_DELAY 5000     // Delay in ms between requests to the charge controller over modbus.
#define SETUP_FINISH_DELAY 100 // Delay in ms after finishing setup.
#define JSON_BUFFER_SIZE 512 // 1024  // Maximum size for the JSON.

/*
    Describes the different states the program can be in.
*/
enum STATE {
    WAIT = 0,
    QUERY = 1,
    TRANSMIT = 2
};
STATE state;

/*
    Array of charging mode strings.
    These are the states the charge controller can be in when charging the battery.
*/
const char *chargeModes[7] = {
    "OFF",      // 0
    "NORMAL",   // 1
    "MPPT",     // 2
    "EQUALIZE", // 3
    "BOOST",    // 4
    "FLOAT",    // 5
    "CUR_LIM"   // 6 (Current limiting)
};

/*
    Array of fault codes.
    These are all the possible faults the charge controller can indicate.
*/
const char *faultCodes[15] = {
    "Charge MOS short circuit",      // (16384 | 01000000 00000000)
    "Anti-reverse MOS short",        // (8192  | 00100000 00000000)
    "PV panel reversely connected",  // (4096  | 00010000 00000000)
    "PV working point over voltage", // (2048  | 00001000 00000000)
    "PV counter current",            // (1024  | 00000100 00000000)
    "PV input side over-voltage",    // (512   | 00000010 00000000)
    "PV input side short circuit",   // (256   | 00000001 00000000)
    "PV input overpower",            // (128   | 00000000 10000000)
    "Ambient temp too high",         // (64    | 00000000 01000000)
    "Controller temp too high",      // (32    | 00000000 00100000)
    "Load over-power/current",       // (16    | 00000000 00010000)
    "Load short circuit",            // (8     | 00000000 00001000)
    "Battery undervoltage warning",  // (4     | 00000000 00000100)
    "Battery overvoltage",           // (2     | 00000000 00000010)
    "Battery over-discharge"         // (1     | 00000000 00000001)
};

// Create the modbus node for the charge controller.
ModbusMaster node;

// Create software serial for communicating with Charge Controller.
SoftwareSerial mySerial(MAX3232_RX, MAX3232_TX);

// Store all the raw data collected from the charge controller.
uint16_t chargeControllerRegisterData[NUM_REGISTERS];

// Was there an error when reading from the charge controller?
uint8_t modbusErr;

// Last time isTime() was run and returned 1.
unsigned long lastTime;

void setup() {
    pinMode(LED_BUILTIN, OUTPUT);    
    Serial.begin(115200);
    // Start the software serial for the modbus connection.
    mySerial.begin(9600);

    node.begin(MODBUS_SLAVE_ADDR, mySerial);

    state = WAIT;
    delay(SETUP_FINISH_DELAY);
    lastTime = millis();
}

// // этот сетап только если мы будем нестандартные команды отправлять т.е. 78 и 79 коды команд
// void setup() {
//     pinMode(LED_BUILTIN, OUTPUT);
//     Serial.begin(115200);
//     // Start the software serial for the modbus connection.
//     mySerial.begin(9600);
//     delay(SETUP_FINISH_DELAY);
// }



#define ADDR_LOAD_CONTROL 0x010A
void setLoadControl(bool ON) {
    int loadValue = 0;
    if (ON) {
        loadValue = 1;
    }

    uint8_t result;
    result = node.writeSingleRegister(ADDR_LOAD_CONTROL, loadValue);
    if (result == node.ku8MBSuccess) {
        Serial.println("successfully wrote");
    } else {
        Serial.print("Error writing: ");
        Serial.println(result, HEX);
    }
}

int getLoadControl() {    
    // проверка как записалось значение
    uint8_t result = node.readHoldingRegisters(ADDR_LOAD_CONTROL, 1);    
    if (result == node.ku8MBSuccess) {        
        return node.getResponseBuffer(0);
    } else {
        Serial.print("Read failed: ");
        Serial.println(result, HEX); // Print error code in hexadecimal
        return -1;
    }
}


int getValue(int addr) {    
    uint8_t result = node.readHoldingRegisters(addr, 1);    
    if (result == node.ku8MBSuccess) {        
        return node.getResponseBuffer(0);
    } else {
        Serial.print("Read failed: ");
        Serial.println(result, HEX); // Print error code in hexadecimal
        return -1;
    }
}



void setParameter(uint16_t addr, int val) {    
    uint8_t result;
    result = node.writeSingleRegister(addr, val);
    if (result == node.ku8MBSuccess) {
        Serial.println("successfully wrote");
    } else {
        Serial.print("Error writing: ");
        Serial.println(result, HEX);
    }
    delay(2000);
}

// здесь все читаем по 4тому разделу
void loop2() { 

    //  4.3、
    uint8_t result = node.readHoldingRegisters(0x000C, 16);
    if (result == node.ku8MBSuccess) {                
        Serial.println("Read successful!");
        for (int i = 0; i < 16; i++) {
            Serial.print("Register ");
            Serial.print(i);
            Serial.print(": ");
            Serial.println(node.getResponseBuffer(i));
            Serial.println((char)(node.getResponseBuffer(i) >> 8));
            Serial.println((char)(node.getResponseBuffer(i) && 0xFF));
        }
    } else {
        Serial.print("Read failed: ");
        Serial.println(result, HEX); // Print error code in hexadecimal
    }


    
    // //  4.15、To read faults and warnings
    // uint8_t result = node.readHoldingRegisters(0x0121, 1);    
    // if (result == node.ku8MBSuccess) {                        
    //     Serial.print("Part 1: "); Serial.println(node.getResponseBuffer(0));
    // } else {
    //     Serial.print("Read failed: ");
    //     Serial.println(result, HEX); // Print error code in hexadecimal
    // }
    // delay(2000);
    // result = node.readHoldingRegisters(0x0122, 1);    
    // if (result == node.ku8MBSuccess) {                        
    //     Serial.print("Part 2: "); Serial.println(node.getResponseBuffer(0));
    // } else {
    //     Serial.print("Read failed: ");
    //     Serial.println(result, HEX); // Print error code in hexadecimal
    // }


    // // 4.16 on/off load (lamp)   
    // setLoadControl(true);
    // Serial.println(getLoadControl());
    // delay(5000);
    // setLoadControl(false);
    // Serial.println(getLoadControl());
    // delay(5000);

    
    // // 4.17、To read street light brightness
    // uint8_t result = node.readHoldingRegisters(0x0120, 1);    
    // if (result == node.ku8MBSuccess) {                        
    //     Serial.print("Read street light brightness: "); Serial.println(node.getResponseBuffer(0) & 0x7F);
    // } else {
    //     Serial.print("Read failed: ");
    //     Serial.println(result, HEX); // Print error code in hexadecimal
    // }

    // // 4.18 
    // setParameter(0xE005, 150); // FIXME: запсь не работает!
    // setParameter(0xE006, 150); // FIXME: запсь не работает!
    // setParameter(0xE007, 140); // FIXME: запсь не работает!
    // // прочитать значения всех параметров 4.18
    // const int regCount = 16;
    // uint16_t readValues[regCount]; 
    // uint8_t result = node.readHoldingRegisters(0xE005, regCount);    
    // if (result == node.ku8MBSuccess) {                
    //     Serial.println("Read successful!");
    //     for (int i = 0; i < regCount; i++) {
    //         readValues[i] = node.getResponseBuffer(i); // Get the value of each register
    //         Serial.print("Register ");
    //         Serial.print(i);
    //         Serial.print(": ");
    //         Serial.println(readValues[i]);
    //     }
    // } else {
    //     Serial.print("Read failed: ");
    //     Serial.println(result, HEX); // Print error code in hexadecimal
    // }


    // // 4.19 read mode
    // Serial.println(getValue(0xE01D));

    // // 4.20
    // funcReadHistory(5);

    // возможно нужен особый вариант функции setup!
    // // 4.21
    // funcResetToFactoryDefaults();

    // возможно нужен особый вариант функции setup!
    // // 4.22
    // funcClearHistory();

    // 4.23 charge current
    // Serial.println(getValue(0xE001));
    // setParameter(0xE001, 1950);
    
    delay(5000);
}


void funcReadHistory (int daysHistoryLen) {
    // 4.20
    const int regCount = 10;
    uint16_t readValues[regCount]; 

    static uint32_t i;
    i++;
    // set word 0 of TX buffer to least-significant word of counter (bits 15..0)
    node.setTransmitBuffer(0, lowWord(i));
    // set word 1 of TX buffer to most-significant word of counter (bits 31..16)
    node.setTransmitBuffer(1, highWord(i));

    // 0xF003 - 3 дня, F006 - 6 дней и т.д.
    int startAddr = 0xF000;
    for (int d = 0; d < daysHistoryLen; d++) {
        uint8_t result = node.readHoldingRegisters(startAddr++, regCount);    
        if (result == node.ku8MBSuccess) {                        
            Serial.print("Day "); Serial.println(d);
            for (int i = 0; i < regCount ; i++) {
                readValues[i] = node.getResponseBuffer(i); // Get the value of each register
                Serial.print(i); Serial.print(": "); Serial.print(readValues[i]); Serial.print(", ");
            }
            Serial.println("\n---------");
        } else {
            Serial.print("Read failed: ");
            Serial.println(result, HEX); // Print error code in hexadecimal
        }
        delay(2000);
    }
    
}

void funcResetToFactoryDefaults () {
    // 4.21 reset to factory defaults
        // dev_id = 1
        // 01 78 00 00 00 01 60 00
        // dev_id = 2
        // 01 78 00 00 00 01 60 33
    byte b = 0x02;
    mySerial.write(b);
    b = 0x78;
    mySerial.write(b);
    b = 0x00;
    mySerial.write(b); 
    b = 0x00;
    mySerial.write(b); 
    b = 0x00;
    mySerial.write(b); 
    b = 0x01;
    mySerial.write(b); 
    b = 0x60;
    mySerial.write(b); 
    b = 0x33;
    mySerial.write(b); 
    // в ответ должны получить тоже самое что и отправилив контроллер
    if (mySerial.available()) {
        for (int i = 0; i < 8; i++) {
            byte c = mySerial.read(); // Read a byte
            Serial.print("Received byte: "); Serial.println(c);
        }
    }
}


void funcClearHistory () {
    // 4.22 clear history
        // dev_id = 1
        // 01 79 00 00 00 01 5D C0
        // dev_id = 2
        // 02 79 00 00 00 01 5D F3    
    byte b = 0x02;
    mySerial.write(b);
    b = 0x79;
    mySerial.write(b);
    b = 0x00;
    mySerial.write(b); 
    b = 0x00;
    mySerial.write(b); 
    b = 0x00;
    mySerial.write(b); 
    b = 0x01;
    mySerial.write(b); 
    b = 0x5D;
    mySerial.write(b); 
    b = 0xF3;
    mySerial.write(b); 
    // в ответ должны получить тоже самое что и отправилив контроллер
    if (mySerial.available()) {
        for (int i = 0; i < 8; i++) {
            byte c = mySerial.read(); // Read a byte
            Serial.print("Received byte: "); Serial.println(c);
        }
    }
}

/*
    Ардуина отправляет на контроллер:
    000002 13:22:12.720  02 03 F0 01 00 0A A7 3E                         ..ð...§>

    02 03 F0 01 00 0A A7 3E
    02 адрес девайса 
    03 команда 
    F0 01 адрес регистра начального
    00 0A сколько считывать регистров
    A7 3E контрольная сумма

    Надо отправить в ком порт такую команду:
    01 79 00 00 00 01 5D C0

*/


/*
    millis() Rollover safe time delay tracking.
*/
uint8_t isTime() {
    if (millis() - lastTime >= REQUEST_DELAY) {
        lastTime = millis();
        return 1;
    }
    return 0;
}

/*
    Helper function to handle the sign bit for negative temperatures.
*/
int getRealTemp(int temp) {
    return temp / 128 ? -(temp % 128) : temp;
}

/*
    Convert the charge controller register data into a formatted JSON string and print to console.
    Register addresses were figured out from the modbus document.
*/

void registerToJson() {
    
    if (modbusErr) {
        
        String res = "";
        res += "{\"modbusError\": true}";        
    } else {
        // We need to account for the load being on when determining the charging mode.
        int loadOffset = chargeControllerRegisterData[32] > 6 ? 32768 : 0;

        String res = "";
        res += "{\"modbusError\": false,";        

        // controller
        res += "\"controller\": {";
        res += "\"chargingMode\": \"";
        res += chargeModes[chargeControllerRegisterData[32] - loadOffset];
        res += "\", ";
        res += "\"temperature\": \"";
        res += getRealTemp(chargeControllerRegisterData[3] >> 8);
        res += "\", ";
        res += "\"days\": \"";
        res += chargeControllerRegisterData[21];
        res += "\", ";
        res += "\"overDischarges\": \""; //
        res += chargeControllerRegisterData[22]; res += "\", ";
        res += "\"fullCharges\": \""; //
        res += chargeControllerRegisterData[23]; res += "\"";
        res += "}, ";
        Serial.println(res);
        Serial.println(res.length());        
        res = "";     

        // charging
        res += "\"charging\": {";
        res += "\"amps\": \""; //
        res += chargeControllerRegisterData[2] * 0.01; res += "\", ";
        res += "\"maxAmps\": \""; //
        res += chargeControllerRegisterData[13] * 0.01; res += "\", ";
        res += "\"watts\": \""; //
        res += chargeControllerRegisterData[9]; res += "\", ";
        res += "\"maxWatts\": \""; //
        res += chargeControllerRegisterData[15]; res += "\", ";
        res += "\"dailyAmpHours\": \""; //
        res += chargeControllerRegisterData[17]; res += "\", ";
        res += "\"totalAmpHours\": \""; //
        res += (chargeControllerRegisterData[24] * 65536 + chargeControllerRegisterData[25]) * 0.001; res += "\", ";
        res += "\"dailyPower\": \""; //
        res += chargeControllerRegisterData[19] * 0.001; res += "\", ";
        res += "\"totalPower\": \""; //
        res += (chargeControllerRegisterData[28] * 65536 + chargeControllerRegisterData[29]) * 0.001; res += "\"";
        res += "}, ";
        Serial.println(res);
        Serial.println(res.length());  
        res = "";      
        
        // battery
        res += "\"battery\": {";
        res += "\"stateOfCharge\": \""; //
        res += chargeControllerRegisterData[0]; res += "\", ";
        res += "\"volts\": \""; //
        res += chargeControllerRegisterData[1] * 0.1; res += "\", ";
        res += "\"minVolts\": \""; //
        res += chargeControllerRegisterData[11] * 0.1; res += "\", ";
        res += "\"maxVolts\": \""; //
        res += chargeControllerRegisterData[12] * 0.1; res += "\", ";
        res += "\"temperature\": \""; //
        res += getRealTemp(chargeControllerRegisterData[3] & 0xFF); res += "\"";
        res += "}, ";
        Serial.println(res);
        Serial.println(res.length());        
        res = "";     

        // panels
        res += "\"panels\": {";        
        res += "\"volts\": \""; //
        res += chargeControllerRegisterData[7] * 0.1; res += "\", ";
        res += "\"amps\": \""; //
        res += chargeControllerRegisterData[8] * 0.01; res += "\"";
        res += "}, ";
        Serial.println(res);
        Serial.println(res.length());        
        res = "";      

        // load
        res += "\"load\": {";        
        res += "\"state\": \""; //
        res += chargeControllerRegisterData[10] ? true : false; res += "\", ";
        res += "\"volts\": \""; //
        res += chargeControllerRegisterData[4] * 0.1; res += "\", ";
        res += "\"amps\": \""; //
        res += chargeControllerRegisterData[5] * 0.01; res += "\", ";
        res += "\"watts\": \""; //
        res += chargeControllerRegisterData[6]; res += "\", ";
        res += "\"maxAmps\": \""; //
        res += chargeControllerRegisterData[14] * 0.01; res += "\", ";
        res += "\"maxWatts\": \""; //
        res += chargeControllerRegisterData[16]; res += "\", ";
        res += "\"dailyAmpHours\": \""; //
        res += chargeControllerRegisterData[18]; res += "\", ";
        res += "\"totalAmpHours\": \""; //
        res += (chargeControllerRegisterData[26] * 65536 + chargeControllerRegisterData[27]) * 0.001; res += "\", ";
        res += "\"dailyPower\": \""; //
        res += chargeControllerRegisterData[20] * 0.001; res += "\", ";
        res += "\"totalPower\": \""; //
        res += (chargeControllerRegisterData[30] * 65536 + chargeControllerRegisterData[31]) * 0.001; res += "\"";
        res += "}, ";
        Serial.println(res);
        //Serial.println(res.length());
        uint32_t checksum = CRC32::calculate(res.c_str(), res.length());
        Serial.println(checksum);
        res = "";            

        int faultIdHi = chargeControllerRegisterData[33];
        int faultIdLo = chargeControllerRegisterData[34];
        res += "\"faults\": {";        
        res += "\"hi\": \""; //
        res += faultIdHi; res += "\", ";
        res += "\"lo\": \""; //
        res += faultIdLo; res += "\"} }";
        Serial.println(res);
        checksum = CRC32::calculate(res.c_str(), res.length());
        Serial.println(checksum);
        res = "";

        // uint8_t count = 0;
        // while ((faultId != 0) && (count < 3)) {
        //     if (faultId >= pow(2, 15 - count)) {
        //         //faults.add(faultCodes[count - 1]);
        //         //faultId -= pow(2, 15 - count);
        //         Serial.print("Fault:");
        //         Serial.println(faultCodes[count - 1]);
        //         Serial.print("faultId:");
        //         Serial.println(pow(2, 15 - count));

        //     }
        //     count += 1;
        // }
        
    }

    Serial.println("-------------------------------------\n");
}



/*
    Request data from the charge controller and store it.
*/
void readNode() {
    static uint32_t i;
    i++;
    // set word 0 of TX buffer to least-significant word of counter (bits 15..0)
    node.setTransmitBuffer(0, lowWord(i));
    // set word 1 of TX buffer to most-significant word of counter (bits 31..16)
    node.setTransmitBuffer(1, highWord(i));

    uint8_t result = node.readHoldingRegisters(MODBUS_REQUEST_START_ADDR, NUM_REGISTERS);    
    if (result == node.ku8MBSuccess) {        
        modbusErr = 0;
        Serial.println(F("Successfully read from CC"));

        for (int j = 0; j < NUM_REGISTERS; j++) {
            chargeControllerRegisterData[j] = node.getResponseBuffer(j);
        }
    } else {
        modbusErr = 1;
        char *channelName[] = {"Failed to read from CC", "Aileron", "Elevator", "Rudder", "Gear", "Aux"};
        Serial.print(F("Failed to read from CC"));
        Serial.print(F(" ("));
        Serial.print(result, HEX);
        Serial.println(F(")"));
    }
}

// считывание регистров с состоянием (раздел 3 документации)
void loop() {
    if (state == WAIT && isTime()) {
        state = QUERY;
    } else if (state == QUERY) {
        readNode();
        state = TRANSMIT;        
    } else if (state == TRANSMIT) {
        // Handle printing to console in this function.
        registerToJson();
        state = WAIT;
    } else {
        state = WAIT;
    }

    // Wait for a while before the next write
    delay(2000); // Adjust the delay as needed
}


/*
{
  "modbusError": false,
  "controller": {
    "chargingMode": "OFF",
    "temperature": "22",
    "days": "1",
    "overDischarges": "1",
    "fullCharges": "0"
  },
  "charging": {
    "amps": "0.00",
    "maxAmps": "0.00",
    "watts": "0",
    "maxWatts": "0",
    "dailyAmpHours": "0",
    "totalAmpHours": "0.00",
    "dailyPower": "0.00",
    "totalPower": "0.00"
  },
  "battery": {
    "stateOfCharge": "0",
    "volts": "0.00",
    "minVolts": "0.00",
    "maxVolts": "0.00",
    "temperature": "25"
  },
  "panels": {
    "volts": "12.20",
    "amps": "0.00"
  },
  "load": {
    "state": "0",
    "volts": "0.00",
    "amps": "0.00",
    "watts": "0",
    "maxAmps": "0.00",
    "maxWatts": "0",
    "dailyAmpHours": "0",
    "totalAmpHours": "0.00",
    "dailyPower": "0.00",
    "totalPower": "0.00"
  }
}
*/



