#include <RF22.h>
#include <RF22Router.h>

#define MY_ADDRESS 12
#define DESTINATION_ADDRESS 25
#define FREQUENCY 431.0
RF22Router rf22(MY_ADDRESS);

enum state {NOEXIST, EMPTY, FULL};

state previusState = NOEXIST;

const char* stateToString(state s) {
    switch (s) {
        case NOEXIST: return "NOTEXIST";
        case EMPTY:   return "EMPTY";
        case FULL:    return "NOTEMPTY";
        default:      return "UNKNOWN";
    }
}

state getCurrentState() {
    // TODO: Take measurements and determine the state of the node

    // For now, we will simulate the state with a random number
    // 0: NOEXIST, 1: EMPTY, 2: FULL
    int randomValue = random(0, 3);
    if (randomValue == 0) {
        return NOEXIST;
    } else if (randomValue == 1) {
        return EMPTY;
    } else if (randomValue == 2) {
        return FULL;
    }

    return NOEXIST;
}

void sendPacket(state currentState) {
    // Prepare the data to be sent - Format: <state>
    char data_read[RF22_ROUTER_MAX_MESSAGE_LEN];
    uint8_t data_send[RF22_ROUTER_MAX_MESSAGE_LEN];
    memset(data_read, '\0', sizeof(data_read));
    memset(data_send, '\0', sizeof(data_send));

    const char* stateStr = stateToString(currentState);
    sprintf(data_read, "%s", stateStr);
    uint8_t msg_len = strlen(data_read) + 1;
    memcpy(data_send, data_read, msg_len);


    // Aloha protocol implementation
    bool successful_packet = false;
    while (!successful_packet)
    {

        if (rf22.sendtoWait(data_send, msg_len, DESTINATION_ADDRESS) != RF22_ROUTER_ERROR_NONE)
        {
            Serial.print("Sending: ");
            Serial.println(data_read);
            long randNumber = random(200, 3000);
            delay(randNumber);
        }
        else
        {
            successful_packet = true;
            Serial.println("Packet sent successfully!");
        }
    }
}

void setup() {
    Serial.begin(9600);

    if (!rf22.init())
        Serial.println("RF22 init failed");
    if (!rf22.setFrequency(FREQUENCY))
        Serial.println("setFrequency Fail");
    rf22.setTxPower(RF22_TXPOW_20DBM);
    rf22.setModemConfig(RF22::GFSK_Rb125Fd125);
    rf22.addRouteTo(DESTINATION_ADDRESS, DESTINATION_ADDRESS);

    randomSeed(MY_ADDRESS);
}

void loop() {

    state currentState = getCurrentState();

    if(currentState != previusState) {
        sendPacket(currentState);
        previusState = currentState;
    }
    else{
        Serial.print("State unchanged: ");
        Serial.println(stateToString(currentState));
    }

    delay(1000); // Delay between packets
}