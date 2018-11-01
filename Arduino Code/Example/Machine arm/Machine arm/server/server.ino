#include "SPI.h"
#include "Mirf.h"
#include "nRF24L01.h"
#include "MirfHardwareSpiDriver.h"

int Button_Counter;
int Button_Delay;
struct Axis {
  uint16_t axis_1;
  uint16_t axis_2;
  uint16_t axis_3;
  uint16_t axis_4;
  uint16_t axis_5;
  uint16_t axis_6;
  uint16_t axis_7;
  uint16_t axis_8;
};
Axis axis_x;

void setup() {
  Serial.begin(115200);
  Mirf.spi = &MirfHardwareSpi;
  Mirf.init();
  Mirf.setTADDR((byte *)"serv1");
  Mirf.payload = 16;
  Mirf.config();
}

void loop() {
  axis_x.axis_1 = analogRead(A0);
  axis_x.axis_2 = analogRead(A1);
  digitalWrite(2, HIGH);

  while (digitalRead(2) == LOW) {
    Button_Delay++;
    delay(1);
  }
  if (Button_Delay > 10) {
    Button_Counter ++;
  }
  Button_Delay = 0;

  if (Button_Counter % 2 != 0) {
    axis_x.axis_3 = analogRead(A2);
    axis_x.axis_4 = analogRead(A3);
    axis_x.axis_5 = axis_x.axis_5;
    axis_x.axis_6 = axis_x.axis_6;
  }
  else {
    axis_x.axis_5 = analogRead(A2);
    axis_x.axis_6 = analogRead(A3);
    axis_x.axis_3 = axis_x.axis_3;
    axis_x.axis_4 = axis_x.axis_4;
  }
  while (digitalRead(2) == 0)
  {
    delay(1);
  }
  Serial.println(Button_Counter);
  Mirf.send((byte *)&axis_x);
  while (Mirf.isSending()) {
  }
}


