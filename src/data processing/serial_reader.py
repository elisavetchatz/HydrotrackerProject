import serial 
import threading

def start_serial_reader(app, logger, port='COM5', baudrate=9600):
    
    def read_serial():
        try:
            arduino_Serial_Data = serial.Serial(port, baudrate, timeout=1)

            while True:
                if arduino_Serial_Data.in_waiting > 0:
                    line = arduino_Serial_Data.readline().decode('utf-8').strip()
                    logger.info(f"RAW: {line}")

                    if line.startswith("Node") and " - State: " in line:
                        parts = line.split(" - State:")
                        node_id_str = parts[0].replace("Node", "").strip()
                        state = parts[1].strip()
                        
                        if node_id_str.isdigit():
                            # responsible for updating the GUI
                            app.update_node_state(int(node_id_str), state)
        
        except Exception as e:
            print("Serial Error:", e)

    # Start the serial reading in a separate thread so as not to block the GUI
    thread = threading.Thread(target=read_serial, daemon=True)
    thread.start()