#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <BluetoothSerial.h> // Biblioteca para Bluetooth Serial


Adafruit_MPU6050 IMU1; //definindo IMU 1:
Adafruit_MPU6050 IMU2; //definindo IMU 2:
BluetoothSerial SerialBT; // Inicializa o Bluetooth Serial


void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);
  
  SerialBT.begin("CaLuBiMaGaLu");

  // Inicializa IMU 1
  IMU1.begin(0x69);
  // Inicializa IMU 2
  IMU2.begin(0x68);

}


void loop() {
//IMU 1
  sensors_event_t a1, g1, temp1;
  IMU1.getEvent(&a1, &g1, &temp1);

//IMU 2
  sensors_event_t a2, g2, temp2;
  IMU2.getEvent(&a2, &g2, &temp2);


// Envio dos dados:
  unsigned long elapsed_time = millis();
  SerialBT.print(elapsed_time); SerialBT.print(",");

  SerialBT.print(a1.acceleration.x); SerialBT.print(",");
  SerialBT.print(a1.acceleration.y); SerialBT.print(",");
  SerialBT.print(a1.acceleration.z); SerialBT.print(",");

  SerialBT.print(g1.gyro.x); SerialBT.print(",");
  SerialBT.print(g1.gyro.y); SerialBT.print(",");
  SerialBT.print(g1.gyro.z); SerialBT.print(",");

  SerialBT.print(a2.acceleration.x); SerialBT.print(",");
  SerialBT.print(a2.acceleration.y); SerialBT.print(",");
  SerialBT.print(a2.acceleration.z); SerialBT.print(",");
  
  SerialBT.print(g2.gyro.x); SerialBT.print(",");
  SerialBT.print(g2.gyro.y); SerialBT.print(",");
  SerialBT.println(g2.gyro.z);


  delay(8);
  
}