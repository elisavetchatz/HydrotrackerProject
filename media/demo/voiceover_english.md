## Demo Voiceover in English

> *Note3: δεν έχω τεστάρει τους χρόνου ςμ ετο αγγλικό version*

At first, we see the coaster from a side view.
It consists of two 3D-printed bases, which enclose a variable metallic resistance — a load cell.

Placing it in a horizontal position, we observe the surface where the glass is placed.

Then, we take a look at the full wiring of the sensor.

First, we have the HX711 amplifier, which digitizes the analog signal from the load cell.
Next, we see the breadboard, where our microcontroller is connected — in this case, an Arduino Uno.

On the breadboard, there is an LED with a 470-ohm resistor and a button, used to automate the taring process.

The Arduino is also connected to an RF22 module, enabling wireless communication between the coaster nodes.

When the sensor is initialized, we observe weight measurements on the serial monitor.
Since the coaster is empty, these values fluctuate close to zero, and the default state displayed is "EMPTY".

We now place an empty glass on the coaster, with the purpose of performing a tare — zeroing the sensor using this specific glass as a tare weight.

We observe that the weight reading increases significantly — as expected.
At the same time, the state of the glass changes from "EMPTY" to "NOT EMPTY".

Due to this change, the transmitter sends a packet to the receiver, which then updates the GUI at the top right of the screen.

In order for the coaster to function correctly, the taring process must be completed first — as mentioned earlier.
We press the button to initiate the process. The LED turns on, and once the taring is complete, it turns off — indicating to the user that the system is ready for use.

After the taring, we observe on the GUI that the node now shows the correct state — "EMPTY".

Now, we fill the glass with water, and as expected, we see an immediate increase in the sensor's weight reading.

As soon as this reading exceeds a predefined threshold, the coaster’s state changes.
A new ALOHA packet is sent from the transmitter to the receiver, and the GUI updates automatically.

We now expand the network by adding another node — that is, a second glass.
This addition is immediately reflected in the GUI, as a new node label appears.

We fill the second glass with water, and observe the change in status from "EMPTY" to "NOT EMPTY".

Next, we remove the glass from the base. After a short delay, the state changes to "NOT EXIST".
During this time, the algorithm checks if the current state is significantly different from the previous ones, ensuring the change is valid before sending the update packet.

It is worth noting that the green color on the GUI indicates that the glass is not empty, and the waitress does not need to intervene.

In contrast, when the color turns red, it signals that it is time to serve the customer.

Continuing, we place the glass back on the base, and the state returns to "NOT EMPTY".

Finally, we lift the glass from the second node, which was previously full.
After consuming its contents, we place the now empty glass back on the coaster.

As expected, the coaster detects the change, the node sends a new packet, and the waitress sees on the GUI that the node has turned red, signaling that the glass is empty and the customer needs service.