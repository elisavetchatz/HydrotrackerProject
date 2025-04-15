# 💧 Smart Water Cup Station for Cafés

A smart hydration tracking system designed to remind users to drink water—evolved into a real-time service assistant tool for cafés.

## 🚀 Overview

This project began with the idea of a **smart base (coaster)** that tracks **daily water consumption** of office workers using a weight sensor and notifies them if they forget to hydrate.

Inspired by this concept, we **adapted** the system to be used in **cafés**, where when a customer’s glass is empty, the system notifies the server to refill it—enhancing customer service without manual checking.

## 🎯 Use Case

> 💡 Target: Cafés looking to automate customer service and ensure better hydration experience.

When the system detects that a glass is **empty**, it sends a **notification** to the waitstaff via a local network message. This is achieved using a **Velostat pressure-sensitive sensor** and an **Arduino** that processes the readings.

---

## 🧠 Project Structure

The repository is organized into three main folders:

```
📦 Hydrotracker
├── 📁 measurements       
├── 📁 media       
    ├── 📁 demo
│   └── 📁 promo       
├── 📁 src                
│   ├── 📁 data_processing 
│   └── 📁 networking      
```

---

## 🛠️ Hardware Used

- **Arduino Uno** 
- **Velostat** sheet
- **Resistor**
...

---

## 📐 Functionality

### 🧪 Sensor Function

- Detects weight change through Velostat.
- Determines if the cup is **full** or **empty**.
- If the cup stays empty for a set duration → sends **notification**.

### 🔔 Notification System

- When the system detects an empty cup:
  - Sends signal over Aloha protocol.
  - Waiter receives a **message/alert** to refill water.

---

## 📸 Media & Demo

`media/` folder for:
- Photos of the prototype
- Videos of the system in action
- Presentation slides

---

## 📊 Measurements

Sensor test results and raw data from experiments are stored in the `measurements/` folder.

