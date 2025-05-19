import tkinter as tk
import configparser
import random

# CONFIG
UPDATE_INTERVAL = 1000             # milliseconds to update the GUI 
FONT = "Ubuntu"                

class HydrotrackerMonitor:
    def __init__(self, root, logger):
        self.root = root        # main window
        self.logger = logger
        self.root.title("HydroTracker Monitor")
        self.labels = {}        # dictionary that connects each node_id to a gui label
        self.node_states = {}   # dictionary that saves the currect state of each node

        title = tk.Label(root, text="   HydroTracker Status Panel   ", font=(FONT, 16, "bold"),
                         bg="#2c3e50", fg="white", pady=10)
        title.pack()

        self.container = tk.Frame(root, bg="#2c3e50")
        self.container.pack(pady=10)

        # START GUI UPDATE LOOP
        self.update_gui_loop()
        # self.simulate_random_states() # for testing

    def create_gui_label(self, node_id):
        """ Creates a label for each node and adds it to the GUI """
        frame = tk.Frame(self.container, bg="#34495e", pady=5, padx=5)
        frame.pack(fill="x", pady=5)

        label = tk.Label(frame, text=f"Node {node_id}: Waiting...",
                         font=(FONT, 12),
                         bg="#bdc3c7", width=30, height=2)
        label.pack(pady=5, padx=5)

        self.labels[node_id] = label
        self.node_states[node_id] = "Unknown"
        self.logger.info(f"New node detected: Node {node_id} added to GUI.")

    def update_gui_loop(self):
        """ Checks the state of each node and updates the GUI labels accordingly """
        for node_id, state in self.node_states.items():
            label = self.labels[node_id]
            label.config(text=f"Node {node_id}: {state}") 

            if state == "EMPTY":
                label.config(bg="#e74c3c", fg="white") # red
            elif state == "NOTEMPTY":
                label.config(bg="#2ecc71", fg="white") # green
            elif state == "NOTEXIST":
                label.config(bg="#7f8c8d", fg="white") # gray
            else:
                label.config(bg="#bdc3c7", fg="black") # neutral gray

        self.root.after(UPDATE_INTERVAL, self.update_gui_loop) # update every UPDATE_INTERVAL milliseconds

    def update_node_state(self, node_id, new_state):
        """ Updates the state of a node when a new state is sent and logs the change """
        if node_id not in self.labels:
            self.create_gui_label(node_id)
        
        previous = self.node_states.get(node_id, "Unknown")

        if previous != new_state:
            self.logger.info(f"Node {node_id} changed state: {previous} → {new_state}")

        self.node_states[node_id] = new_state

    ## for testing purposes
    # def simulate_random_states(self):
    #     pass
    #     # node_id = random.randint(1, 20)
    #     # state = random.choice(["EMPTY", "NOTEMPTY", "NOTEXIST"])
    #     # self.update_node_state(node_id, state)
    #     # self.root.after(UPDATE_INTERVAL, self.simulate_random_states)

