// Include the TimerOne Library from Paul Stoffregen

#include "TimerOne.h"
#include "Wire.h"
#include <MPU6050_light.h>
// MPU6050 Setup
MPU6050 mpu(Wire);
// Left Motor (A)
int enA = 10;
int in1 = 9;
int in2 = 8;
// Right Motor (B)
int enB = 5;
int in3 = 7;
int in4 = 6;

// Constants for Interrupt Pins
// Change values if not using Arduino Uno

const byte MOTOR1 = 2;  // Motor 1 Interrupt Pin - INT 0 MOTOR RIGHT
const byte MOTOR2 = 3;  // Motor 2 Interrupt Pin - INT 1 MOTOR LEFT

// Integers for pulse counters
unsigned int counter1 = 0;
unsigned int counter2 = 0;
int x = 4;
// Float for number of slots in encoder disk
const float diskslots = 2500.00;  // Change to match value of encoder disk
const float wheeldiameter = 20.0; // Wheel diameter in cm
float wheelbase = 30.0; // in cm
// Interrupt Service Routines

// Motor 1 pulse count ISR
void ISR_count1()
{
  counter1++;  // increment Motor 1 counter value
}

// Motor 2 pulse count ISR
void ISR_count2()
{
  counter2++;  // increment Motor 2 counter value
}

// TimerOne ISR
void ISR_timerone()
{
  Timer1.detachInterrupt();  // Stop the timer
  //Serial.print("Right Motor Speed: ");
  float rotation1 = (counter1 / diskslots) * 60.00;  // calculate RPM for Motor 1
  Serial.print(" R:");
  Serial.print(rotation1);

  counter1 = 0;  //  reset counter to zero
  //Serial.print("Left Motor Speed: ");
  float rotation2 = (counter2 / diskslots) * 60.00;  // calculate RPM for Motor 2
  Serial.print(" L:");
  Serial.print(rotation2);
  
  int new_angle = mpu.getAngleZ();
  Serial.print(" Z:");
  Serial.print(new_angle);
  counter2 = 0;  //  reset counter to zero
  Timer1.attachInterrupt( ISR_timerone );  // Enable the timer
}

void setup()
{
  Serial.begin(9600);
  Serial.setTimeout(1);
  Wire.begin();
  set_gyro();
  Timer1.initialize(100000); // set timer for 1sec
  attachInterrupt(digitalPinToInterrupt (MOTOR1), ISR_count1, RISING);  // Increase counter 1 when speed sensor pin goes High
  attachInterrupt(digitalPinToInterrupt (MOTOR2), ISR_count2, RISING);  // Increase counter 2 when speed sensor pin goes High
  Timer1.attachInterrupt( ISR_timerone ); // Enable the timer
}

void loop()
{
  mpu.update();
  if (Serial.available()) {
    x = Serial.readString().toInt();
  }
  motor_control();
}
void motor_control(){
  if (x == 0) {
      front();
    }
    if (x == 1) {
      back();
    }
    if (x == 2) {
      left();
    }
    if (x == 3) {
      right();
    }
    if (x == 4) {
      stop_();
    }
}
void front() {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(enA, 255);
  // Set Motor B forward
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  analogWrite(enB, 255);
}
void back() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  analogWrite(enA, 255);
  // Set Motor B forward
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  analogWrite(enB, 255);
}
void stop_() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  analogWrite(enA, 255);
  // Set Motor B forward
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
  analogWrite(enB, 255);
}
void right() {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(enA, 255);
  // Set Motor B forward
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  analogWrite(enB, 255);
}
void left() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  analogWrite(enA, 255);
  // Set Motor B forward
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  analogWrite(enB, 255);
}
void set_gyro(){
  byte status = mpu.begin();
  mpu.calcOffsets(); // gyro and accelero
}
void set_gyro_print() {
  byte status = mpu.begin();
  Serial.print(F("MPU6050 status: "));
  Serial.println(status);
  while (status != 0) { } // stop everything if could not connect to MPU6050
  Serial.println(F("Calculating offsets, do not move MPU6050"));
  delay(1000);
  mpu.calcOffsets(); // gyro and accelero
  Serial.println("Done!\n");
}
