import tkinter as tk
from logging_utils import setup_logger
from hydrotracker_monitor import HydrotrackerMonitor
from serial_reader import SerialReader

if __name__ == "__main__":
    
    logger = setup_logger()
    logger.info("Log test message")

    root = tk.Tk()
    app = HydrotrackerMonitor(root, logger)

    reader = SerialReader(app, logger, port='COM5', baudrate=9600)
    reader.start()
    root.mainloop()

    #reader.stop()
