#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <BluetoothSerial.h> // Biblioteca para Bluetooth Serial


Adafruit_MPU6050 IMU1; //definindo IMU 1:
Adafruit_MPU6050 IMU2; //definindo IMU 2:
BluetoothSerial SerialBT; // Inicializa o Bluetooth Serial

int i = 0;

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);



  Serial.println("Escaneando barramento I2C...");
  for (byte addr = 1; addr < 127; addr++) {
    Wire.beginTransmission(addr);
    if (Wire.endTransmission() == 0) {
      Serial.print("Dispositivo encontrado em: 0x");
      Serial.println(addr, HEX);
    }
  }


  
  SerialBT.begin("CaLuBiMaGaLu");
  Serial.println("Iniciando sensores...");
  // Inicializa IMU 1
  if (!IMU1.begin(0x69)) {
    Serial.println("ERRO: MPU6050 (1) não encontrado no endereço 0x68!");
  } else {
    Serial.println("MPU6050 (1) conectado com sucesso.");
  }

  // Inicializa IMU 2
  if (!IMU2.begin(0x68)) {
    Serial.println("ERRO: MPU6050 (2) não encontrado no endereço 0x69!");
  } else {
    Serial.println("MPU6050 (2) conectado com sucesso.");
  }
}


void loop() {
//IMU 1
  sensors_event_t a1, g1, temp1;
  IMU1.getEvent(&a1, &g1, &temp1);

//IMU 2
  sensors_event_t a2, g2, temp2;
  IMU2.getEvent(&a2, &g2, &temp2);


  // Serial.printf("\n_________________iteração %d_________________\n", i);
  // i += 1;
  
// aceleração
  // Serial.println("aceleração1:");
  Serial.print("\nax1: ");
  Serial.print(a1.acceleration.x);
  Serial.print("\tay1: ");
  Serial.print(a1.acceleration.y);
  Serial.print("\taz1: ");
  Serial.println(a1.acceleration.z);

//giro
  Serial.print("gx1: ");
  Serial.print(g1.gyro.x);
  Serial.print("\tgy1: ");
  Serial.print(g1.gyro.y);
  Serial.print("\tgz1: ");
  Serial.println(g1.gyro.z);



// aceleração
  // Serial.println("aceleração2:");
  Serial.print("ax2: ");
  Serial.print(a2.acceleration.x);
  Serial.print("\tay2: ");
  Serial.print(a2.acceleration.y);
  Serial.print("\taz2: ");
  Serial.println(a2.acceleration.z);

//giro
  // Serial.println("Giro2:");
  Serial.print("gx2: ");
  Serial.print(g2.gyro.x);
  Serial.print("\tgy2: ");
  Serial.print(g2.gyro.y);
  Serial.print("\tgz2: ");
  Serial.println(g2.gyro.z);
  // Serial.println(millis());


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


  delay(1000);
  
}