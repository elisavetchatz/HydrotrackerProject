import tkinter as tk
from logging_utils import setup_logger
from HydrotrackerMonitor import HydrotrackerMonitor
from SerialReaderThread import SerialReaderThread as SerialReader
    
logger = setup_logger()
logger.info("Log test message")

root = tk.Tk()
app = HydrotrackerMonitor(root, logger)

reader = SerialReader(app, logger, port='COM7', baudrate=9600)
reader.start()
root.mainloop()

#reader.stop()
