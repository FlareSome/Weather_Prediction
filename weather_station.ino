// Smart Weather Station Sketch - Professional Firmware
// Components: DHT-22, BMP-280, Raindrop Sensor, OLED Display

#include <DHT.h>
#include <Adafruit_BMP280.h>

// Sensor Pin Definitions
#define DHTPIN 2      // Digital pin connected to the DHT sensor
#define DHTTYPE DHT22 // DHT 22 (AM2302)
#define RAIN_PIN 7    // Digital pin for Raindrop sensor (D0 output)

DHT dht(DHTPIN, DHTTYPE);
Adafruit_BMP280 bmp; // Default I2C address 0x76

// Variables
float temperature_c = 0.0;
float humidity_perc = 0.0;
float pressure_hpa = 0.0;

void setup() {
  Serial.begin(9600);
  delay(100);

  // Initialize DHT
  dht.begin();
  
  // Initialize BMP280
  if (!bmp.begin()) {
    Serial.println(F("BMP280 Sensor not found. Check wiring!"));
    while (1);
  }
  
  pinMode(RAIN_PIN, INPUT);
  
  Serial.println(F("SYSTEM_INITIALIZED"));
  Serial.println(F("Transmitting Data Format: T(C), H(%), P(hPa), R(mm_sim)"));
}

void loop() {
  // Wait 5 seconds between measurements.
  delay(5000); 

  // --- Read Sensors ---
  humidity_perc = dht.readHumidity();
  temperature_c = dht.readTemperature();
  pressure_hpa = bmp.readPressure() / 100.0F; // Convert Pa to hPa
  
  // Reading the digital rain sensor output (0 or 1)
  int rain_digital = digitalRead(RAIN_PIN);
  float rainfall_mm_sim = (rain_digital == LOW) ? random(1, 10) / 10.0 : 0.0;
  
  // Check if any reads failed
  if (isnan(humidity_perc) || isnan(temperature_c)) {
    Serial.println("SENSOR_ERROR: Failed to read from DHT sensor!");
    return;
  }

  // --- Transmit Data over Serial ---
  // Format: T=XX.X,H=XX.X,P=XXXX.X,R=X.X
  String data_string = "T=" + String(temperature_c, 1) + 
                       ",H=" + String(humidity_perc, 1) + 
                       ",P=" + String(pressure_hpa, 1) + 
                       ",R=" + String(rainfall_mm_sim, 1);
                       
  Serial.println(data_string);
}