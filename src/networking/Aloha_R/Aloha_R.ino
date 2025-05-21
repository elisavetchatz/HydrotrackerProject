#include <RF22.h>
#include <RF22Router.h>

#define MY_ADDRESS 25
#define NODE_ADDRESS_1 1
#define NODE_ADDRESS_2 2
#define FREQUENCY 444.0
RF22Router rf22(MY_ADDRESS);


void setup() {
    Serial.begin(9600);

    if (!rf22.init())
        Serial.println("RF22 init failed");
    if (!rf22.setFrequency(FREQUENCY))
        Serial.println("setFrequency Fail");
    rf22.setTxPower(RF22_TXPOW_20DBM);
    rf22.setModemConfig(RF22::GFSK_Rb125Fd125);

    rf22.addRouteTo(NODE_ADDRESS_1, NODE_ADDRESS_1);
    rf22.addRouteTo(NODE_ADDRESS_2, NODE_ADDRESS_2);

}

void loop() {
    uint8_t buf[RF22_ROUTER_MAX_MESSAGE_LEN];
    memset(buf, '\0', sizeof(buf));
    uint8_t len = sizeof(buf);
    uint8_t from;

    if (rf22.recvfromAck(buf, &len, &from)) {
        // Format: Node <node_id> - State: <state>
        buf[len - 1] = '\0';
        Serial.print("Node ");
        Serial.print(from);
        Serial.print(" - State: ");
        Serial.println((char*)buf);
    }
}