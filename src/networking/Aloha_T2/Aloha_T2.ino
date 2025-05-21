#include <HX711_ADC.h>
#include <RF22.h>
#include <RF22Router.h>

#define MY_ADDRESS 2
#define DESTINATION_ADDRESS 25
#define FREQUENCY 444.0
RF22Router rf22(MY_ADDRESS);

const int HX711_DOUT = 4; // HX711 data pin
const int HX711_SCK = 5;  // HX711 clock pin
HX711_ADC LoadCell(HX711_DOUT, HX711_SCK);

const float NOEXIST_THRESHOLD = -20.0; // Threshold for no existence
const float EMPTY_THRESHOLD = 50.0;    // Threshold for empty

const int TARE_BUTTON_PIN = 8; // Pin for tare button
const int LED_PIN = 7;         // Pin for LED

enum state
{
    NOEXIST,
    EMPTY,
    FULL
};

state previousState = NOEXIST;

const char *stateToString(state s)
{
    switch (s)
    {
    case NOEXIST:
        return "NOTEXIST";
    case EMPTY:
        return "EMPTY";
    case FULL:
        return "NOTEMPTY";
    default:
        return "UNKNOWN";
    }
}

state getCurrentState()
{

    LoadCell.update();
    float currentWeight = LoadCell.getData();
    Serial.print("Measured Weight: ");
    Serial.println(currentWeight);

    while (1)
    {
        delay(1000);
        LoadCell.update();
        float weight = LoadCell.getData();

        Serial.print("Measured Weight: ");
        Serial.println(weight);

        if (weight < currentWeight + 1.0 && weight > currentWeight - 1.0)
        {
            currentWeight = weight;
            break; // Exit the loop if weight is stable
        }

        currentWeight = weight;
    }

    if (currentWeight < NOEXIST_THRESHOLD)
    {
        return NOEXIST;
    }
    else if (currentWeight < EMPTY_THRESHOLD)
    {
        return EMPTY;
    }
    else if (currentWeight >= EMPTY_THRESHOLD)
    {
        return FULL;
    }

    return NOEXIST;
}

void sendPacket(state currentState)
{
    // Prepare the data to be sent - Format: <state>
    char data_read[RF22_ROUTER_MAX_MESSAGE_LEN];
    uint8_t data_send[RF22_ROUTER_MAX_MESSAGE_LEN];
    memset(data_read, '\0', sizeof(data_read));
    memset(data_send, '\0', sizeof(data_send));

    const char *stateStr = stateToString(currentState);
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

void setup()
{
    Serial.begin(9600);

    pinMode(TARE_BUTTON_PIN, INPUT);
    pinMode(LED_PIN, OUTPUT);
    digitalWrite(LED_PIN, LOW);

    if (!rf22.init())
        Serial.println("RF22 init failed");
    if (!rf22.setFrequency(FREQUENCY))
        Serial.println("setFrequency Fail");
    rf22.setTxPower(RF22_TXPOW_20DBM);
    rf22.setModemConfig(RF22::GFSK_Rb125Fd125);
    rf22.addRouteTo(DESTINATION_ADDRESS, DESTINATION_ADDRESS);

    LoadCell.begin();
    bool tare = true;
    LoadCell.start(2000, tare);

    if (LoadCell.getTareTimeoutFlag() || LoadCell.getSignalTimeoutFlag())
    {
        Serial.println("HX711 not found. Check wiring and pin designations.");
        while (1)
            ;
    }
    else
    {
        float calibrationFactor = -455.90; // TODO: Set the calibration factor
        LoadCell.setCalFactor(calibrationFactor);
    }

    randomSeed(MY_ADDRESS);
}

void loop()
{

    if (digitalRead(TARE_BUTTON_PIN) == HIGH)
    {
        Serial.println("Tare button pressed. Taring...");
        digitalWrite(LED_PIN, HIGH);
        LoadCell.tare();
        digitalWrite(LED_PIN, LOW);
    }
    state currentState = getCurrentState();

    if (currentState != previousState)
    {
        sendPacket(currentState);
        previousState = currentState;
    }
    else
    {
        Serial.print("State unchanged: ");
        Serial.println(stateToString(currentState));
    }

    delay(1000); // Delay between packets
}