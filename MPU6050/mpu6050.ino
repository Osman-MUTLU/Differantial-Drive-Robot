/* Get tilt angles on X and Y, and rotation angle on Z
    Angles are given in degrees
 License: MIT
 */
 #include "Wire.h"
 #include <MPU6050_light.h>
 MPU6050 mpu(Wire);
 int angle_prev = 0;
 unsigned long timer = 0;
 void setup() {
   Serial.begin(9600);
   Wire.begin();
 byte status = mpu.begin();
   Serial.print(F("MPU6050 status: "));
   Serial.println(status);
   while (status != 0) { } // stop everything if could not connect to MPU6050
 Serial.println(F("Calculating offsets, do not move MPU6050"));
   delay(1000);
   mpu.calcOffsets(); // gyro and accelero
   Serial.println("Done!\n");
 }
 void loop() {
   mpu.update();
   if ((millis() - timer) > 100) { // print data every 10ms;
    int new_angle = mpu.getAngleZ();
     Serial.print("\tZ : ");
     Serial.print(new_angle);
     
     Serial.print("\tD : ");
     Serial.println(new_angle-angle_prev);
     angle_prev = new_angle;
     timer = millis();
   }
 }
