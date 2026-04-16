# ⚡ Energy Optimized Adaptive Network-on-Chip (NoC)

## 📌 Overview
This project presents an **Energy Optimized Adaptive Routing framework for Network-on-Chip (NoC)** using Machine Learning and congestion-aware routing techniques.

The system simulates different NoC topologies and dynamically selects optimal routing paths based on:
- Traffic patterns
- Network congestion
- Injection rate

A **Streamlit-based interactive dashboard** is developed to visualize:
- Traffic flow
- Congestion heatmap
- Routing paths
- Performance metrics

---

## 🎯 Objectives
- Reduce latency and energy consumption in NoC
- Implement adaptive routing strategies
- Compare Mesh and Flattened Butterfly topologies
- Visualize real-time traffic and congestion
- Use ML to predict optimal routing behavior

---

## 🧠 Key Features

### 🔹 Adaptive Routing
- Supports:
  - DOR (Deterministic)
  - Valiant Routing
  - RAN_MIN (Adaptive)

### 🔹 Congestion-Aware Routing
- Uses **dynamic edge weights**
- Avoids highly congested paths
- Updates traffic heatmap in real-time

### 🔹 Topologies
- 🟦 Mesh
- 🟨 Flattened Butterfly (with express links)

### 🔹 Traffic Patterns
- Uniform
- Hotspot
- Transpose
- Bit Complement

### 🔹 Machine Learning
- Random Forest Classifier
- Predicts optimal routing strategy
- Trained using generated + BookSim-inspired datasets

---

## 📊 Performance Metrics

- 📉 Latency
- ⚡ Energy Consumption
- 📦 Throughput
- 🔁 Inflight Flits

---

## 🖥️ Dashboard (Streamlit)

Interactive dashboard features:
- Network visualization with routing paths
- Congestion heatmap
- Performance graphs
- Real-time parameter tuning

---

## 🛠️ Tech Stack

- Python
- Streamlit
- NetworkX
- NumPy
- Pandas
- Plotly
- Scikit-learn (Random Forest)

---

## 📂 Project Structure
