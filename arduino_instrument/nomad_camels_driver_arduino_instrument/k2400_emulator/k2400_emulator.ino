/*
  Minimal Keithley 2400 SCPI emulator for Arduino Nano 33 IoT (SAMD21).

  - Reads voltage from A7 on :READ? when :CONF:VOLT
  - Computes current on :READ? when :CONF:CURR as (VA1 - VA7)/Rshunt
  - Sets output "voltage" on DAC pin A0 via :SOUR:VOLT <value>
  - Ignores/accepts other commands used by the provided driver.

  Serial settings expected by the Python driver:
    9600 baud, CRLF line endings on both TX and RX.

  Voltage assumptions:
    - 0..3.3 V measurable on A1/A7 relative to GND
    - DAC output on A0 is ~0..3.3 V

  Returns a single ASCII float per :READ? depending on :CONF:
*/

#define PIN_VIN_NEG A7     // negative sense input (e.g., shunt low side)
#define PIN_VIN_POS A1     // positive sense input (e.g., shunt high side)
#define PIN_VOUT   A0      // DAC output (Nano 33 IoT)

static const float VREF = 3.3f;                 // board reference (approx)
static const float SHUNT_RESISTANCE = 96.6f;    // ohms (adjust to your shunt)
static const int ADC_BITS = 12;                 // 12-bit ADC for better resolution
static const int DAC_BITS = 10;                 // SAMD21 DAC is 10-bit (0..1023)

// State
enum Func { F_VOLT, F_CURR, F_RES };
Func conf_func = F_VOLT;   // measurement function
Func source_func = F_VOLT; // source function (only VOLT used here)
bool output_on = false;    // accept but not strictly needed

float set_voltage_V = 0.0f;

// --- Utilities ---
String trimCRLF(const String& s) {
  String t = s;
  while (t.length() && (t[t.length()-1] == '\r' || t[t.length()-1] == '\n')) {
    t.remove(t.length()-1);
  }
  t.trim();
  return t;
}

String toUpperStr(String s) {
  s.toUpperCase();
  return s;
}

bool startsWithCI(const String& s, const String& prefix) {
  String S = s; S.toUpperCase();
  String P = prefix; P.toUpperCase();
  return S.startsWith(P);
}

float clampf(float x, float lo, float hi) {
  if (x < lo) return lo;
  if (x > hi) return hi;
  return x;
}

void writeDAC_V(float volts) {
  volts = clampf(volts, 0.0f, VREF);
  int code = (int)roundf(volts * ((1 << DAC_BITS) - 1) / VREF);
  code = constrain(code, 0, (1 << DAC_BITS) - 1);
  analogWrite(PIN_VOUT, code);
}

// Parse a float from a command like ":SOUR:VOLT 1.23"
bool parseFloatAfter(const String& cmd, float& outVal) {
  int sp = cmd.indexOf(' ');
  if (sp < 0) return false;
  String num = cmd.substring(sp + 1);
  num.trim();
  if (!num.length()) return false;
  outVal = num.toFloat();
  return true;
}

/*** NEW: small helper readers for reuse ***/
float readVoltage_AvgV(int pin, int samples = 100) {
  uint32_t raw = 0;
  for (int i = 0; i < samples; i++) {
    raw += analogRead(pin);
  }
  return (float)raw * VREF / ((1 << ADC_BITS) - 1) / samples;
}

float readCurrent_AvgI(int samples = 100) {
  uint32_t raw_pos = 0;
  uint32_t raw_neg = 0;
  for (int i = 0; i < samples; i++) {
    raw_pos += analogRead(PIN_VIN_POS);
    raw_neg += analogRead(PIN_VIN_NEG);
  }
  float Vpos = (float)raw_pos * VREF / ((1 << ADC_BITS) - 1) / samples;
  float Vneg = (float)raw_neg * VREF / ((1 << ADC_BITS) - 1) / samples;
  float Vdiff = Vpos - Vneg;                // A1 - A7
  float I = Vdiff / SHUNT_RESISTANCE;       // amps
  return I;
}
/*** END NEW helpers ***/

// --- SCPI handlers ---
void handleQuery(const String& cmdU) {
  if (cmdU == "*IDN?") {
    Serial.print("Arduino,Nano33IoT,SCPI-Emulator Keithley 2400,1.0\r\n");
    return;
  }

  if (cmdU == ":CONF?") {
    if (conf_func == F_VOLT) Serial.print("\"VOLT\"\r\n");
    else if (conf_func == F_CURR) Serial.print("\"CURR\"\r\n");
    else Serial.print("\"RES\"\r\n");
    return;
  }

  if (cmdU == ":READ?") {
    const int number_of_reads = 100;

    if (conf_func == F_VOLT) {
      // Average A7 as before
      uint32_t raw = 0;
      for (int i = 0; i < number_of_reads; i++) {
        raw += analogRead(PIN_VIN_NEG);
      }
      float avg = (float)raw * VREF / ((1 << ADC_BITS) - 1) / number_of_reads;
      Serial.print(String(avg, 6));
      Serial.print("\r\n");
      return;
    } else if (conf_func == F_CURR) {
      uint32_t raw_pos = 0;
      uint32_t raw_neg = 0;
      // Average paired samples from A1 and A7, compute I = (VA1 - VA7)/R
      for (int i = 0; i < number_of_reads; i++) {
        raw_pos += analogRead(PIN_VIN_POS);
        raw_neg += analogRead(PIN_VIN_NEG);
      }
      float Vpos = (float)raw_pos * VREF / ((1 << ADC_BITS) - 1) / number_of_reads;
      float Vneg = (float)raw_neg * VREF / ((1 << ADC_BITS) - 1) / number_of_reads;
      float Vdiff = Vpos - Vneg;      // A1 - A7 (your requested order)
      float I = Vdiff / SHUNT_RESISTANCE;     // amps (can be negative)
      Serial.print(String(I, 6));
      Serial.print("\r\n");
      return;
    } else {
      Serial.print("0.000000\r\n");
      return;
    }
  }

  // Unknown query -> reply with simple error marker
  Serial.print("?\r\n");
}

void handleCommand(const String& cmd, const String& cmdU) {
  if (cmdU == ":FORM:DATA ASC" ||
      startsWithCI(cmdU, ":VOLT:RANG") ||
      startsWithCI(cmdU, ":CURR:RANG") ||
      startsWithCI(cmdU, ":SOUR:VOLT:RANG") ||
      startsWithCI(cmdU, ":SOUR:CURR:RANG") ||
      startsWithCI(cmdU, "SENS:VOLT:PROT") ||
      startsWithCI(cmdU, "CURR:PROT") ||
      cmdU == ":OUTP 1" || cmdU == ":OUTP 0") {
    if (cmdU == ":OUTP 1") output_on = true;
    if (cmdU == ":OUTP 0") output_on = false;
    return;
  }

  // Configure measure function
  if (cmdU == ":CONF:VOLT") { conf_func = F_VOLT; return; }
  if (cmdU == ":CONF:CURR") { conf_func = F_CURR; return; }
  if (cmdU == ":CONF:RES")  { conf_func = F_RES;  return; }

  // Source function (only VOLT is meaningful here)
  if (cmdU == ":SOUR:FUNC VOLT") { source_func = F_VOLT; return; }
  if (cmdU == ":SOUR:FUNC CURR") { source_func = F_CURR; return; }

  // Set source voltage: ":SOUR:VOLT <value>"
if (startsWithCI(cmdU, ":SOUR:VOLT")) {
  float v;
  if (parseFloatAfter(cmd, v)) {
    // 1) Set as before
    set_voltage_V = v;
    if (output_on || true) {
      writeDAC_V(set_voltage_V);
    }

    // 2) Measure-and-correct loop (10 passes)
    const int repeat_set_loop = 10;
    float R_est = 0.0f;

    for (int i = 0; i < repeat_set_loop; ++i) {
      delay(2); // brief settle time after the last write

      // Read V and I
      float V_read = readVoltage_AvgV(PIN_VIN_NEG, 5); // A7
      float I_read = readCurrent_AvgI(5);               // (A1-A7)/R

      // Optional: estimate resistance for debugging/telemetry
      if (fabs(I_read) > 1e-12f) {
        R_est = V_read / I_read;
      }

      // Guard against divide-by-zero or nonsense
      if (V_read > 1e-9f) {
        // V_set_new = V_set_old * (1 + 96.6 * I_read / V_read)
        float V_set_new = set_voltage_V * (1.0f + SHUNT_RESISTANCE * I_read / V_read);

        // Clamp and apply for the *next* iteration to measure again
        V_set_new = clampf(V_set_new, 0.0f, VREF);
        writeDAC_V(V_set_new);
      }
      // if V_read ~ 0, skip this correction pass
    }
  }
  return;
}
// ### ------ Iterative Error correction -------- ###
// Set source voltage: ":SOUR:VOLT <value>"
// if (startsWithCI(cmdU, ":SOUR:VOLT")) {
//   float v_target; // This is the final voltage we want to achieve.
//   if (parseFloatAfter(cmd, v_target)) {
    
//     // --- Configuration for the Correction Loop ---
//     const int CORRECTION_PASSES = 10;
//     // Kp: How strongly we react to the error. 
//     // 0.0 to 1.0. Start with ~0.5.
//     // Smaller values are more stable but slower. Larger values are faster but may overshoot.
//     const float PROPORTIONAL_GAIN = 0.2f; 

//     // --- Loop Implementation ---

//     // 1. Start by setting the DAC to the initial target voltage.
//     float dac_output_voltage = v_target;
//     // Clamp the initial value just in case.
//     dac_output_voltage = clampf(dac_output_voltage, 0.0f, VREF);
//     writeDAC_V(dac_output_voltage);
    
//     // This global variable holds the user's intended setpoint.
//     set_voltage_V = v_target;

//     // 2. Start the correction loop.
//     for (int i = 0; i < CORRECTION_PASSES; ++i) {

//       // Read the actual voltage being produced at the output terminals.
//       float v_read = readVoltage_AvgV(PIN_VIN_NEG, 5);

//       // Calculate the error: (where we want to be) - (where we are).
//       float error = v_target - v_read;

//       // Calculate the adjustment. We add a *fraction* of the error back.
//       // This prevents overshooting and oscillation.
//       float correction = error * PROPORTIONAL_GAIN;

//       // Apply the correction to our DAC setting for the next loop.
//       dac_output_voltage += correction;

//       // Clamp the new DAC value to ensure it's within the valid hardware range.
//       dac_output_voltage = clampf(dac_output_voltage, 0.0f, VREF);
      
//       // Write the newly corrected value to the DAC.
//       writeDAC_V(dac_output_voltage);
//     }
//   }
//   return;
// }

// --- CURRENT SOURCE ADDITIONS ---
  // -------- Iterative Current Set: ":SOUR:CURR <amps>" --------
  if (startsWithCI(cmdU, ":SOUR:CURR")) {
    float set_current_A = 0.0f; // last requested current setpoint
    float i_target; // amps
    if (parseFloatAfter(cmd, i_target)) {
      const int CORRECTION_PASSES =75;
      const float PROPORTIONAL_GAIN = 0.5f;

      // Start from Vset = 100 mV as requested
      float dac_output_voltage = 0.1f;
      dac_output_voltage = clampf(dac_output_voltage, 0.0f, VREF);
      writeDAC_V(dac_output_voltage);

      set_current_A = i_target;

      for (int i = 0; i < CORRECTION_PASSES; ++i) {
        float i_read = readCurrent_AvgI(5);                 // amps
        float error_I = i_target - i_read;                  // amps
        float correction_V = error_I * SHUNT_RESISTANCE;    // volts (Ohm's law)
        correction_V *= PROPORTIONAL_GAIN;                  // scaled

        dac_output_voltage = clampf(dac_output_voltage + correction_V, 0.0f, VREF);
        writeDAC_V(dac_output_voltage);
      }

      // Optionally store the approximate resulting voltage
      set_voltage_V = dac_output_voltage;
    }
    return;
  }

  // Silently ignore any other commands
}

// --- Setup & loop ---
void setup() {
  analogReadResolution(ADC_BITS);   // 12-bit ADC
  analogWriteResolution(DAC_BITS);  // 10-bit DAC on SAMD21

  pinMode(PIN_VIN_NEG, INPUT);
  pinMode(PIN_VIN_POS, INPUT);
  // A0 is DAC; no pinMode required for analogWrite on DAC

  Serial.begin(9600);
  delay(200);
}

void loop() {
  static String line;
  while (Serial.available()) {
    char c = (char)Serial.read();
    line += c;

    if (c == '\n') {
      String raw = trimCRLF(line);
      line = "";
      if (raw.length() == 0) continue;

      String cmdU = toUpperStr(raw);

      if (cmdU.endsWith("?")) {
        handleQuery(cmdU);
      } else {
        handleCommand(raw, cmdU);
      }
    }
  }
}
