import pandas as pd
import numpy as np

data = []

sizes = [4, 8, 16]
routes = ["DOR", "VALIANT", "RAN_MIN"]
traffic_types = ["uniform", "hotspot", "transpose", "bit_complement"]

for size in sizes:
    for inj in np.linspace(0.01, 1.5, 150):

        for traffic in traffic_types:
            for route in routes:

                # ======================
                # 🔹 TRAFFIC IMPACT
                # ======================
                if traffic == "uniform":
                    congestion = 1.0
                elif traffic == "hotspot":
                    congestion = 2.0
                elif traffic == "transpose":
                    congestion = 1.5
                elif traffic == "bit_complement":
                    congestion = 1.7

                # ======================
                # 🔹 ROUTING IMPACT
                # ======================
                if route == "DOR":
                    routing_factor = 1.5
                elif route == "VALIANT":
                    routing_factor = 1.2
                else:
                    routing_factor = 1.0

                # ======================
                # 🔹 LATENCY
                # ======================
                latency = inj * size * congestion * routing_factor * 5
                latency += np.random.uniform(0, 2)

                # ======================
                # 🔹 THROUGHPUT
                # ======================
                throughput = inj / (1 + latency)

                # ======================
                # 🔹 INFLIGHT FLITS
                # ======================
                inflight = inj * size * congestion

                # ======================
                # 🔹 HOPS (approx)
                # ======================
                avg_hops = size / 2

                # ======================
                # 🔹 ENERGY
                # ======================
                energy = inflight * avg_hops * 0.3

                data.append([
                    size, inj, traffic, route,
                    latency, throughput, inflight, energy
                ])

df = pd.DataFrame(data, columns=[
    "Size", "Injection_Rate", "Traffic",
    "Routing", "Latency",
    "Throughput", "Inflight_Flits", "Energy"
])

df.to_csv("noc_dataset_realistic.csv", index=False)

print("Dataset created successfully!")