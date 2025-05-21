import serial
import threading

#CONFIG
PORT='COM10'  # Serial port to connect to
BAUDRATE=9600  # Baud rate for the serial connection

class SerialReaderThread:
    """
    Manages a serial connection in a background thread and updates the GUI when new data arrives.
    """

    def __init__(self, app, logger, port=PORT, baudrate=BAUDRATE):

        self.app = app
        self.logger = logger
        self.port = port
        self.baudrate = baudrate
        self.serial_conn = None
        self.thread = None
        self.running = False

    def start(self):
        """
        Starts the background thread to read data from the serial port.
        """
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.read_serial, daemon=True)
            self.thread.start()
        else:
            self.logger.warning("SerialReader is already running.")

    def stop(self):
        """
        Stops the serial reading and closes the connection.
        """
        self.running = False
        if self.serial_conn and self.serial_conn.is_open:
            try:
                self.serial_conn.close()
                self.logger.info("Serial connection closed.")
            except Exception as e:
                self.logger.error(f"Error closing serial connection: {e}")

    def read_serial(self):
        """
        Internal method that runs in a background thread and reads data from the serial port.
        """
        try:
            self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=1)
            self.logger.info(f"Serial connection established on {self.port} at {self.baudrate} baud.")

            while self.running:
                try:
                    if self.serial_conn.in_waiting > 0:
                        line = self.serial_conn.readline().decode('utf-8', errors='ignore').strip() # decode the bytes to string and remove whitespace
                        self.logger.info(f"RAW: {line}")

                        if line.startswith("Node") and " - State: " in line:
                            before, _, after = line.partition(" - State:")
                            node_id_str = before.replace("Node", "").strip()
                            state = after.strip()

                            if node_id_str.isdigit():
                                self.app.update_node_state(int(node_id_str), state) # responsible for updating the GUI

                except Exception as inner_e:
                    self.logger.warning(f"Error reading line: {inner_e}")

        except Exception as e:
            self.logger.error(f"Serial Error: {e}")

        finally:
            if self.serial_conn and self.serial_conn.is_open:
                try:
                    self.serial_conn.close()
                    self.logger.info("Serial connection closed (final cleanup).")
                except Exception as close_e:
                    self.logger.error(f"Error closing serial connection: {close_e}")
