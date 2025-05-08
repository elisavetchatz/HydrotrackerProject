import tkinter as tk
import random

# CONFIG
MAX_NODES = 5                   # maximum number of nodes
UPDATE_INTERVAL = 1000          # milliseconds to update the GUI 
FONT = "Ubuntu"                

class HydrotrackerMonitor:
    def __init__(self, root, logger):
        self.root = root        # main window
        self.logger = logger
        self.root.title("💧 HydroTracker Monitor")
        self.labels = {}        # dictionary that connects each node_id to a gui label
        self.node_states = {}   # dictionary that saves the currect state of each node

        title = tk.Label(root, text="💧 HydroTracker Status Panel 💧", font=(FONT, 16, "bold"),
                         bg="#2c3e50", fg="white", pady=10)
        title.pack()

        self.container = tk.Frame(root, bg="#2c3e50")
        self.container.pack(pady=10)

        # LABELS
        for node_id in range(1, MAX_NODES + 1):
            frame = tk.Frame(self.container, bg="#34495e", pady=5, padx=5)
            frame.pack(fill="x", pady=5)

            label = tk.Label(frame, text=f"Node {node_id}: Waiting...",
                             font=(FONT, 12),
                             bg="#bdc3c7", width=30, height=2)
            label.pack(pady=5, padx=5)

            self.labels[node_id] = label
            self.node_states[node_id] = "Unknown" # initial state of each node

        # START GUI UPDATE LOOP
        self.update_gui_loop()
        #self.simulate_random_states()

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
        previous = self.node_states[node_id]

        if node_id in self.node_states:
            #self.node_states[node_id] = new_state
            if previous != new_state:
                self.logger.info(f"Node {node_id} changed state: {previous} → {new_state}")
            self.node_states[node_id] = new_state

    # def simulate_random_states(self):
    #     possible_states = ["FULL", "EMPTY", "NOEXIST"]
    #     for node_id in range(1, MAX_NODES + 1):
    #         random_state = random.choice(possible_states)
    #         self.update_node_state(node_id, random_state)

    #     self.root.after(UPDATE_INTERVAL, self.simulate_random_states)
