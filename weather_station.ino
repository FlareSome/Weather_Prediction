#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
#include <DHT.h>

// ---------------- CONFIG ----------------
#define DHT_PIN 2
#define DHT_TYPE DHT22
#define RAIN_ANALOG A0
#define RAIN_DIGITAL 4

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define OLED_ADDR 0x3C

DHT dht(DHT_PIN, DHT_TYPE);
Adafruit_BMP280 bmp;
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

bool bmpOK = false;

float temperature, humidity, pressure, altitude;
int rainValue, rainDigital;

unsigned long lastRead = 0;
const unsigned long INTERVAL = 5000;

// Forward declare
void printJSON();

// --------------- SETUP -------------------
void setup() {
  Serial.begin(115200);
  delay(300);

  dht.begin();

  // BMP detect
  bmpOK = bmp.begin(0x76) || bmp.begin(0x77);

  // OLED detect
  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
    while (1); // freeze
  }

  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(10, 20);
  display.println("Weather");
  display.setCursor(10, 40);
  display.println("Station");
  display.display();
  delay(1500);
}

// --------------- LOOP ---------------------
void loop() {
  if (millis() - lastRead >= INTERVAL) {
    lastRead = millis();
    readSensors();
    updateDisplay();
    printJSON();
  }
}

// --------------- READ SENSORS -------------
void readSensors() {
  humidity = dht.readHumidity();
  temperature = dht.readTemperature();

  if (bmpOK) {
    pressure = bmp.readPressure() / 100.0;
    altitude = bmp.readAltitude(1013.25);
  } else {
    pressure = 0;
    altitude = 0;
  }

  rainValue = analogRead(RAIN_ANALOG);
  rainDigital = digitalRead(RAIN_DIGITAL);
}

// --------------- OLED DISPLAY -------------
void updateDisplay() {
  display.clearDisplay();
  display.fillRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, SSD1306_BLACK);

  // ---- Title ----
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("Weather Station");

  // ---- Big Temperature ----
  display.setTextSize(2);
  display.setCursor(0, 12);
  if (temperature != -999) {
    display.print(temperature, 1);
    display.println(" C");
  } else {
    display.println("ERR");
  }

  // ---- Row 1: Humidity + Pressure ----
  display.setTextSize(1);
  display.setCursor(0, 34);
  display.print("H: ");
  display.print(humidity, 1);
  display.print("%");

  display.setCursor(70, 34);   // ← aligned right side
  display.print("P:");
  display.print(pressure, 0);
  display.print("hPa");

  // ---- Row 2: Rain + Analog ----
  display.setCursor(0, 48);
  display.print("Rain: ");
  display.print(rainDigital ? "Dry" : "Wet");

  display.setCursor(70, 48);
  display.print("A:");
  display.print(rainValue);
  
  display.fillRect(124, 0, 4, SCREEN_HEIGHT, SSD1306_BLACK);

  display.display();
}

// --------------- JSON OUTPUT --------------
void printJSON() {
  Serial.print("{");

  Serial.print("\"timestamp\":"); Serial.print(millis()/1000);
  Serial.print(",\"temperature\":"); Serial.print(temperature);
  Serial.print(",\"humidity\":"); Serial.print(humidity);
  Serial.print(",\"pressure\":"); Serial.print(pressure);
  Serial.print(",\"altitude\":"); Serial.print(altitude);
  Serial.print(",\"rain_value\":"); Serial.print(rainValue);
  Serial.print(",\"rain_digital\":"); Serial.print(rainDigital);

  Serial.println("}");
}
