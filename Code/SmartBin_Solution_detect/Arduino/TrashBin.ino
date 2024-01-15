#include <SPI.h>
#include <Servo.h>
#include "nRF24L01.h"
#include "RF24.h"

// Device id
const int TRASHBIN_ID = 3;

// Hardware configuration
RF24 radio(9, 10);

Servo servo;

// Radio pipe addresses for the 2 nodes to communicate.
const uint64_t address = 0xF0F0F0F0D2;

const int MAX_PAYLOAD_SIZE = 32;
char payload[MAX_PAYLOAD_SIZE + 1];

int byteArrayToInt(char* arr, int len)
{
  int value = 0;
  for (int i = 0; i < len; i++)
  {
    value = value * 10 + (int)(arr[i] - 48);
  }
  return value;
}

int byteToInt(char data)
{
  return (int)(data - 48);
}

void setup(void)
{
  Serial.begin(115200);

  servo.attach(3);
  servo.write(90);

  Serial.println("Start:");

  radio.begin();

  radio.enableDynamicPayloads();

  radio.setRetries(5, 15);

  radio.openReadingPipe(1, address);

  radio.startListening();
}

void loop(void)
{
  if ( radio.available() )
  {
    uint8_t len = radio.getDynamicPayloadSize();

    if (!len) {
      return;
    }

    radio.read(payload, len);

    Serial.println(payload);

    if (byteToInt(payload[0]) == TRASHBIN_ID)
    {
      if (byteToInt(payload[1]) == 1) {
        servo.write(0);
      } else {
        servo.write(90);
      }
    }
  }
}
