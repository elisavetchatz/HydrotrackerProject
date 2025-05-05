import tkinter as tk
import random

# CONFIG
MAX_NODES = 5                   # maximum number of nodes
UPDATE_INTERVAL = 10000         # milliseconds to update the GUI (review and maybe change)

class HydrotrackerMonitor:
    def __init__(self, root, logger):
        self.root = root        # main window
        self.root.title("HydroTracker Monitor")
        self.logger = logger
        self.labels = {}        #labels for each coaster
        self.node_states = {}   # to remember the state of each coaster

        # LABELS
        for node_id in range(1, MAX_NODES + 1):
            label = tk.Label(root, text=f"Node {node_id}: Waiting...", width=30, font=("Arial", 12), bg="lightgray")
            label.pack(pady=2)
            self.labels[node_id] = label
            self.node_states[node_id] = "Unknown"

        # START GUI UPDATE LOOP
        self.update_gui_loop()
        #self.simulate_random_states()

    def update_gui_loop(self):
        for node_id, state in self.node_states.items():
            label = self.labels[node_id]
            label.config(text=f"Node {node_id}: {state}")

            if state == "EMPTY":
                label.config(bg="red")
            elif state == "NOTEMPTY":
                label.config(bg="lightgreen")
            elif state == "NOTEXIST":
                label.config(bg="gray")
            else:
                label.config(bg="lightgray")

        self.root.after(UPDATE_INTERVAL, self.update_gui_loop) # update every 100ms

    def update_node_state(self, node_id, state):
        if node_id in self.node_states:
            self.node_states[node_id] = state

            previous = self.node_states[node_id]
            if previous != state:
                self.logger.info(f"Node {node_id} changed state: {previous} → {state}")
            self.node_states[node_id] = state

    # def simulate_random_states(self):
    #     possible_states = ["FULL", "EMPTY", "NOEXIST"]
    #     for node_id in range(1, MAX_NODES + 1):
    #         random_state = random.choice(possible_states)
    #         self.update_node_state(node_id, random_state)

    #     self.root.after(UPDATE_INTERVAL, self.simulate_random_states)
