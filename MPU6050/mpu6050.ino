/* Get tilt angles on X and Y, and rotation angle on Z
    Angles are given in degrees
 License: MIT
 */
 #include "Wire.h"
 #include <MPU6050_light.h>
 MPU6050 mpu(Wire);
 void setup() {
   Serial.begin(9600);
   Wire.begin();
  
 }
 void loop() {
   mpu.update();
 }
 void set_gyro(){
 byte status = mpu.begin();
   Serial.print(F("MPU6050 status: "));
   Serial.println(status);
   while (status != 0) { } // stop everything if could not connect to MPU6050
 Serial.println(F("Calculating offsets, do not move MPU6050"));
   delay(1000);
   mpu.calcOffsets(); // gyro and accelero
   Serial.println("Done!\n");
 }
 int angle_z(){
    int new_angle = mpu.getAngleZ();
     Serial.print(" AngleZ:");
     Serial.print(new_angle);
     return new_angle;
 }
