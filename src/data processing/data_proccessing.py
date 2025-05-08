import tkinter as tk
from logging import setup_logger
from hydrotracker_monitor import HydrotrackerMonitor
from serial_reader import start_serial_reader

if __name__ == "__main__":
    
    logger = setup_logger()
    logger.info("Log test message")

    root = tk.Tk()
    app = HydrotrackerMonitor(root, logger)

    start_serial_reader(app)
    root.mainloop()
