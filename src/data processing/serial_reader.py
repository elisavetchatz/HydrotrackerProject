import serial 

arduino_Serial_Data = serial.Serial('COM5', 9600, timeout=1)

print("Listening for data from Arduino...")

while True:
    if arduino_Serial_Data.in_waiting > 0:
        try:
            # reaad line
            myData = arduino_Serial_Data.readline().decode('utf-8').strip()

            # Node:3 - State:EMPTY
            if myData.startswith("Node:") and " - State:" in myData:
                parts = myData.split(" - state:")
                node = parts[0].replace("node:", "").strip()
                state = parts[1].strip()

                print(f"Node {node} is in state: {state}")

        except Exception as e:
            print("Error while parsing data:", e)