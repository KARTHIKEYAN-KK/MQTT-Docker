#define TINY_GSM_MODEM_SIM800
#include <TinyGsmClient.h>
#include <SoftwareSerial.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>

LiquidCrystal_I2C lcd(0x3F, 16, 2);
Servo myservo;

char apn[]  = "airtelgprs.com";
char user[] = "";
char pass[] = "";

static const int rxPin = 12, txPin = 11;

const char* server_address = "13.232.49.108";
const int server_port = 5010;

unsigned long previousMillis1 = 0;
unsigned long previousMillis2 = 0;
const long scaning = 1000;
const long sending = 15000;

int sensor = 2;
int sensor_val = 0;

String state = "False";

SoftwareSerial sim800(rxPin, txPin);
TinyGsm modem(sim800);
TinyGsmClient client(modem);

void setup() {
  Serial.begin(9600);
  lcd.init();
  lcd.init();
  myservo.attach(3); 

  delay(10);
  lcd.backlight();

  pinMode(sensor, INPUT_PULLUP);

  sim800.begin(9600);
  myservo.write(0);
  Serial.println("SIM800L serial initialize");
  Serial.println("Initializing modem...");
  lcd.setCursor(0, 0);
  lcd.print("System  Starting");
  lcd.setCursor(3, 1);
  lcd.print("Modem init");
  modem.restart();
  String modemInfo = modem.getModemInfo();
  Serial.print("Modem Info: ");
  Serial.println(modemInfo);
  lcd.clear();
  lcd.setCursor(3, 0);
  lcd.print("Modem Info");
  lcd.setCursor(1, 1);
  lcd.print(modemInfo);

  modem.gprsConnect(apn, user, pass);

  Serial.print("Waiting for network...");
  lcd.clear();
  lcd.setCursor(2, 0);
  lcd.print("Signal  wait");
  if (!modem.waitForNetwork()) {
    Serial.println(" fail");
    delay(5000);
    return;
  }
  Serial.println(" success");


  if (modem.isNetworkConnected()) {
    Serial.println("Network connected");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Signal Connected");
    delay(500);
  }
  Serial.print(F("Connecting to "));
  lcd.clear();
  lcd.setCursor(2, 0);
  lcd.print("Network wait");
  Serial.print(apn);
  if (!modem.gprsConnect(apn, user, pass)) {
    Serial.println(" fail");
    return;
  }
  Serial.println(" success");

  if (modem.isGprsConnected()) {
    Serial.println("GPRS connected");
    lcd.clear();
    lcd.setCursor(1, 0);
    lcd.print("Net  Connected");
    delay(500);
  }


}

void loop() {
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis1 >= scaning) {
    previousMillis1 = currentMillis;

    if (!modem.isGprsConnected()) {
      if (!modem.gprsConnect(apn, user, pass)) {
        Serial.println(" fail");
        delay(1000);
        return;
      }
    }

    sensor_val = digitalRead(sensor);
    if (sensor_val == 1) {
      state = "True";
      myservo.write(90);
      lcd.clear();
      lcd.setCursor(1, 0);
      lcd.print("FLOOD ALERT  !");
      lcd.setCursor(0, 1);
      lcd.print("-TAKE  DIVESION-");
      Send_data();
    }
    else {
      state = "False";
      myservo.write(0);
      lcd.clear();
      lcd.setCursor(4, 0);
      lcd.print("WELCOME");
      lcd.setCursor(0, 1);
      lcd.print("-HAPPY  JOURNEY-");
    }
    Serial.println(sensor_val);
  }


  if (currentMillis - previousMillis2 >= sending) {
    previousMillis2 = currentMillis;
    Send_data();
    Serial.println("Sending");
  }
}

String convertToHex(String data) {
  String hexData = "";
  char hex[2];
  for (int i = 0; i < data.length(); i++) {
    sprintf(hex, "%02X", data.charAt(i));
    hexData += hex;
  }
  return hexData;
}

void Send_data() {
  int rssi = modem.getSignalQuality();
  //  int mapped_rssi = map(rssi, -100, -20, 1, 10);
  String device_id = "1";
  String mac_address = "43:56:7U:89:90";
  String gsm_signal =  String(rssi);
  String flood_status = state;
  String data = device_id + "#" + mac_address + "#" + gsm_signal + "#" + flood_status;
  String hexData = convertToHex(data);

  // Create an HTTP POST request
  Serial.println("Connecting to server.....");
  if (!client.connect(server_address, server_port)) {
    Serial.println("Connection failed");
    return;
  }

  Serial.println("Sending request:");
  Serial.println(hexData);
  client.print(hexData);

  // Wait for server response
  while (client.connected()) {
    if (client.available()) {
      String response = client.readStringUntil('\r');
      Serial.print(response);
    }
  }

  client.stop();
}