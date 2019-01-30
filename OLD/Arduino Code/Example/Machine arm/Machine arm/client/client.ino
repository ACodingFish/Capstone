#include <SPI.h>
#include <Mirf.h>
#include <nRF24L01.h>
#include <MirfHardwareSpiDriver.h>
#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
Servo servo6;

float k_1;
float k_2;
float k_3;
float k_4;
float k_5;
float k_6;
float k_1_Temp, k_2_Temp, k_3_Temp, k_4_Temp, k_5_Temp, k_6_Temp;

float speed_1;
float speed_2;
float speed_3;
float speed_4;
float speed_5;
float speed_6;

struct Axis  // Datas from remote control
{
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

  servo1.attach(8);
  servo2.attach(9);
  servo3.attach(10);
  servo4.attach(11);
  servo5.attach(12);
  servo6.attach(13);

  Mirf.cePin = 53;
  Mirf.csnPin = 48;
  Mirf.spi = &MirfHardwareSpi;
  Mirf.init();
  Mirf.setTADDR((byte *)"serv1");
  Mirf.payload = 16;
  Mirf.config();
}

void loop() {
  if (!Mirf.isSending() && Mirf.dataReady()) {
    Mirf.getData((byte *) &axis_x);
  }
  if (axis_x.axis_1 > 530)
  {
    k_1_Temp = map(axis_x.axis_1, 531, 1023, 0, 500) / 4000.00;
  }
  else if (axis_x.axis_1 < 470)
  {
    k_1_Temp = map(axis_x.axis_1, 0, 469, -500, 0) / 4000.00;
  }
  else {
    k_1_Temp = 0;
  }

  if (axis_x.axis_2 > 530)
  {
    k_2_Temp = -map(axis_x.axis_2, 531, 1023, 0, 500) / 4000.00;
  }
  else if (axis_x.axis_2 < 470)
  {
    k_2_Temp = -map(axis_x.axis_2, 0, 469, -500, 0) / 4000.00;
  }
  else {
    k_2_Temp = 0;
  }

  if (axis_x.axis_3 > 530)
  {
    k_3_Temp = -map(axis_x.axis_3, 531, 1023, 0, 500) / 4000.00;
  }
  else if (axis_x.axis_3 < 470)
  {
    k_3_Temp = -map(axis_x.axis_3, 0, 469, -500, 0) / 4000.00;
  }
  else {
    k_3_Temp = 0;
  }

  if (axis_x.axis_4 > 530) {
    k_4_Temp = -map(axis_x.axis_4, 531, 1023, 0, 500) / 4000.00;
  }
  else if (axis_x.axis_4 < 470) {
    k_4_Temp = -map(axis_x.axis_4, 0, 469, -500, 0) / 4000.00;
  }
  else {
    k_4_Temp = 0;
  }

  if (axis_x.axis_5 > 530) {
    k_5_Temp = -map(axis_x.axis_5, 531, 1023, 0, 500) / 4000.00;
  }
  else if (axis_x.axis_5 < 470) {
    k_5_Temp = -map(axis_x.axis_5, 0, 469, -500, 0) / 4000.00;
  }
  else {
    k_5_Temp = 0;
  }

  if (axis_x.axis_6 > 530) {
    k_6_Temp = -map(axis_x.axis_6, 531, 1023, 0, 500) / 4000.00;
  }
  else if (axis_x.axis_6 < 470) {
    k_6_Temp = -map(axis_x.axis_6, 0, 469, -500, 0) / 4000.00;
  }
  else {
    k_6_Temp = 0;
  }

  k_1 += 0.02 * (k_1_Temp - k_1);
  k_2 += 0.02 * (k_2_Temp - k_2);
  k_3 += 0.02 * (k_3_Temp - k_3);
  k_4 += 0.02 * (k_4_Temp - k_4);
  k_5 += 0.02 * (k_5_Temp - k_5);
  k_6 += 0.02 * (k_6_Temp - k_6);
  
  speed_1 = min(90, max(-90, speed_1 += k_1));
  speed_2 = min(90, max(-90, speed_2 += k_2));
  speed_3 = min(90, max(-90, speed_3 += k_3));
  speed_4 = min(90, max(-90, speed_4 += k_4));
  speed_5 = min(90, max(-90, speed_5 += k_5));
  speed_6 = min(90, max(-90, speed_6 += k_6));

  Serial.print("  k_1_Temp="); Serial.print(k_1_Temp); Serial.print("  k_2="); Serial.print(k_2); Serial.print("  k_3="); Serial.print(k_3); Serial.print("  k_4="); Serial.println(k_4);
  //Serial.print("  S_1="); Serial.print(speed_1);Serial.print("  S_2="); Serial.print(speed_2);Serial.print("  S_3="); Serial.print(speed_3);Serial.print("  S_4="); Serial.println(speed_4);

  servo1.write(speed_1 + 90);
  servo2.write(speed_2 + 90);
  servo3.write(speed_3 + 90);
  servo4.write(speed_4 + 90);
  servo5.write(speed_5 + 90);
  servo6.write(speed_6 + 90);
}

