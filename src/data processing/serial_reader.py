import serial 
import threading

def start_serial_reader(app, logger, port='COM5', baudrate=9600):
    """"Sarts a thread to read data from the serial port and update the GUI accordingly."""
    
    def read_serial():
        """Reads data from the serial port and updates the GUI."""
        try:
            arduino_Serial_Data = serial.Serial(port, baudrate, timeout=1)
            logger.info(f"Serial connection established on {port} at {baudrate} baud.")

            while True:
                try:
                    if arduino_Serial_Data.in_waiting > 0:
                        line = arduino_Serial_Data.readline().decode('utf-8', errors='ignore').strip() # decode the bytes to string and remove whitespace
                        logger.info(f"RAW: {line}")

                        if line.startswith("Node") and " - State: " in line: # check if the line contains the expected format: "Node X - State: Y"
                            before, _, after = line.partition(" - State:")
                            node_id_str = before.replace("Node", "").strip()
                            state = after.strip()
                        
                            if node_id_str.isdigit():
                                app.update_node_state(int(node_id_str), state) # responsible for updating the GUI
                except Exception as inner_e:
                    logger.warning(f"Error reading line: {inner_e}")
        
        except Exception as e:
            logger.error(f"Serial Error: {e}")

        finally:
            try:
                arduino_Serial_Data.close()
                logger.info("Serial connection closed.")
            except Exception as close_e:
                logger.error(f"Error closing serial connection: {close_e}")

    # Start the serial reading in a separate thread so as not to block the GUI
    thread = threading.Thread(target=read_serial, daemon=True) #daemon=True makes sure the thread will close when the main program exits
    thread.start()