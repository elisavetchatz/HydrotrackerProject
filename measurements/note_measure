# Calibration του HX711 Load Cell 


## Συνδέσεις:

### Load Cell to HX711
- Red → E+
- Black → E-
- White → A-
- Green → A+

### HX711 → Arduino
- VCC → 5V
- GND → GND
- DT → 4
- SCK → 5

---

## Calibration.ino upload to Arduino
- Serial Monitor στα ** baud**
- message `"Send 't' from serial monitor to set the tare offset."`

---

## Tare
- No weigtht on the scale
- **`t`** στο Serial Monitor και Enter
- `"Tare complete"`

---

## Τοποθέτηση γνωστού βάρους
- Place a known weight on the scale
- Type the known weight in grams
- calibration factor υπολογιζεται και εμφανίζεται στο Serial Monitor


---

## save calibration factor
- **`y`** για αποθήκευση στο EEPROM
- else **`n`**
---

## τελος
- στο `setup()` ```cpp
LoadCell.setCalFactor(calibration_factor);```
