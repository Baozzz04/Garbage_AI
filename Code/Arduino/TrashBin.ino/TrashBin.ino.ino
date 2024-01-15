#include <SPI.h>
#include <Servo.h>
#include "nRF24L01.h"
#include "RF24.h"

// Device id
const int TRASHBIN_ID = 2;
const int CLOSE_ANGLE = 28; // 12, 28, 48 
const int OPEN_ANGLE = CLOSE_ANGLE + 90;

// Hardware configuration
RF24 radio(9, 10);

Servo servo;

// Radio pipe addresses for the 2 nodes to communicate.
const uint64_t address = 0xF0F0F0F0D2;

const int MAX_PAYLOAD_SIZE = 32;
char payload[MAX_PAYLOAD_SIZE + 1];

int currentAngle = CLOSE_ANGLE;

void setServo(int angle)
{
  if (angle == CLOSE_ANGLE && currentAngle == OPEN_ANGLE)
  {
     for (int i = OPEN_ANGLE; i > CLOSE_ANGLE; i -= 5)
     {
        servo.write(i);
        delay(20);
     }
  }
  if (angle == OPEN_ANGLE && currentAngle == CLOSE_ANGLE)
  {
     for (int i = CLOSE_ANGLE; i < OPEN_ANGLE; i += 5)
     {
        servo.write(i);
        delay(20);
     }
  }
  servo.write(angle);
  currentAngle = angle;
}

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
  servo.write(CLOSE_ANGLE);

  Serial.println("Start:");

  radio.begin();

  radio.enableDynamicPayloads();

  radio.setRetries(5, 15);

  radio.setDataRate(RF24_250KBPS);

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
          Serial.println("bbbb:");

    setServo(OPEN_ANGLE);
      } else {
        setServo(CLOSE_ANGLE);
      }
    }
  }
}
