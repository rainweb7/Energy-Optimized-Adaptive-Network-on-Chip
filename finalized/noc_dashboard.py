# import streamlit as st
# import numpy as np
# import plotly.graph_objects as go
# import networkx as nx
# import pandas as pd

# st.set_page_config(layout="wide")

# st.title("Energy Optimized Adaptive Network-on-Chip")

# # ======================
# # 🔷 LOAD DATASET
# # ======================
# try:
#     data = pd.read_csv("noc_dataset_realistic.csv")

#     st.subheader("Dataset Overview")
#     st.dataframe(data.head())

#     fig_data = go.Figure()

#     # fig_data.add_trace(go.Scatter(
#     #     x=data['Injection_Rate'],
#     #     y=data['Latency'],
#     #     name='Latency'
#     # ))

#     # fig_data.update_layout(title="Latency vs Injection Rate")

#     # st.plotly_chart(fig_data, width='stretch')

# except:
#     st.error("Dataset not loaded")

# # ======================
# # 🔷 SIDEBAR
# # ======================
# size = st.sidebar.selectbox("Network Size", [4, 8, 16])
# inj = st.sidebar.slider("Injection Rate", 0.01, 1.5, 0.5)

# traffic_type = st.sidebar.selectbox(
#     "Traffic Pattern",
#     ["uniform", "hotspot", "transpose", "bit_complement"]
# )

# topology = st.sidebar.selectbox("Topology", ["Mesh", "Flattened Butterfly"])

# # ======================
# # 🔷 FILTER DATASET
# # ======================
# filtered = data[
#     (data["Size"] == size) &
#     (data["Traffic"].str.lower() == traffic_type.lower())
# ]

# # pick closest injection rate
# row = filtered.iloc[(filtered["Injection_Rate"] - inj).abs().argsort()[:1]]

# # extract values
# latency = row["Latency"].values[0]
# energy = row["Energy"].values[0]
# throughput = row["Throughput"].values[0]
# inflight = row["Inflight_Flits"].values[0]
# route = row["Routing"].values[0]

# st.sidebar.write("Routing:", route)

# # ======================
# # 🔷 TOPOLOGY
# # ======================
# if topology == "Mesh":
#     G = nx.grid_2d_graph(size, size)
#     def convert(n): return n
# else:
#     # SAFE flattened butterfly approximation
#     G = nx.complete_graph(size)
#     def convert(n): return n

# # ======================
# # 🔥 REAL TRAFFIC FROM DATA
# # ======================
# traffic = np.random.rand(size, size) * (inflight / (size * size))

# # ======================
# # 🔥 MULTI-PATH TRAFFIC
# # ======================
# num_packets = int(inj * 10) + 1
# all_paths = []

# nodes = list(G.nodes())

# for _ in range(num_packets):

#     s = nodes[np.random.randint(len(nodes))]
#     d = nodes[np.random.randint(len(nodes))]

#     while d == s:
#         d = nodes[np.random.randint(len(nodes))]

#     try:
#         if route == "RAN_MIN":
#             paths = list(nx.all_shortest_paths(G, s, d))
#             path = paths[np.random.randint(len(paths))]

#         elif route == "VALIANT":
#             mid = nodes[np.random.randint(len(nodes))]
#             p1 = nx.shortest_path(G, s, mid)
#             p2 = nx.shortest_path(G, mid, d)
#             path = p1 + p2[1:]

#         else:  # DOR
#             path = nx.shortest_path(G, s, d)

#         all_paths.append(path)

#     except:
#         continue

# # ======================
# # 🔷 DRAW NETWORK
# # ======================
# edge_x, edge_y = [], []
# for e in G.edges():
#     x0, y0 = (e[0], 0) if not isinstance(e[0], tuple) else e[0]
#     x1, y1 = (e[1], 0) if not isinstance(e[1], tuple) else e[1]

#     edge_x += [x0, x1, None]
#     edge_y += [y0, y1, None]

# edge_trace = go.Scatter(x=edge_x, y=edge_y, mode="lines")

# node_x, node_y = [], []
# for n in G.nodes():
#     if isinstance(n, tuple):
#         node_x.append(n[0])
#         node_y.append(n[1])
#     else:
#         node_x.append(n)
#         node_y.append(0)

# node_trace = go.Scatter(
#     x=node_x,
#     y=node_y,
#     mode="markers",
#     marker=dict(size=10, color="lightblue")
# )

# # ======================
# # 🔥 PATH VISUALIZATION
# # ======================
# path_traces = []

# for path in all_paths:
#     px = [p[0] if isinstance(p, tuple) else p for p in path]
#     py = [p[1] if isinstance(p, tuple) else 0 for p in path]

#     path_traces.append(go.Scatter(x=px, y=py, mode="lines"))

# fig = go.Figure(data=[edge_trace, node_trace] + path_traces)

# fig.update_layout(title=f"{size}x{size} {topology} Traffic ({traffic_type})")

# st.plotly_chart(fig, width='stretch')

# # ======================
# # 🔥 HEATMAP
# # ======================
# st.subheader("Traffic Congestion")

# st.plotly_chart(
#     go.Figure(data=go.Heatmap(z=traffic, colorscale='RdYlGn_r')),
#     width='stretch'
# )

# # ======================
# # 🔥 PERFORMANCE GRAPH
# # ======================
# st.subheader("Performance Metrics")

# fig_perf = go.Figure()

# fig_perf.add_trace(go.Bar(
#     x=["Latency", "Energy", "Throughput"],
#     y=[latency, energy, throughput]
# ))

# st.plotly_chart(fig_perf, width='stretch')

# # ======================
# # 🔥 METRICS DISPLAY
# # ======================
# c1, c2, c3, c4 = st.columns(4)
# c1.metric("Latency", round(latency, 2))
# c2.metric("Energy", round(energy, 2))
# c3.metric("Throughput", round(throughput, 3))
# c4.metric("Inflight Flits", round(inflight, 2))




# import networkx as nx
# import streamlit as st
# import numpy as np
# import plotly.graph_objects as go
# import pandas as pd


# st.set_page_config(layout="wide", page_title="Energy Optimized NoC")

# st.title("⚡ Energy Optimized Adaptive NoC with Traffic Patterns")

# # ======================
# # 🔷 LOAD DATASET
# # ======================
# @st.cache_data
# def get_data():
#     try:
#         df = pd.read_csv("noc_dataset_realistic.csv")
#         df.columns = df.columns.str.strip()
#         return df
#     except:
#         return None

# data = get_data()

# # ======================
# # 🔷 SIDEBAR & PARAMETERS
# # ======================
# size = st.sidebar.selectbox("Network Size", [4, 8, 16])
# inj = st.sidebar.slider("Injection Rate", 0.01, 1.5, 0.7)
# traffic_type = st.sidebar.selectbox("Traffic Pattern", ["uniform", "hotspot", "transpose", "bit_complement"])
# topology = st.sidebar.selectbox("Topology", ["Mesh", "Flattened Butterfly"])

# # ======================
# # 🔷 FILTER DATASET FOR METRICS
# # ======================
# if data is not None:
#     filtered = data[(data["Size"] == size) & (data["Traffic"].str.lower() == traffic_type.lower())]
#     if not filtered.empty:
#         row = filtered.iloc[(filtered["Injection_Rate"] - inj).abs().argsort()[:1]]
#         latency = row["Latency"].values[0]
#         energy = row["Energy"].values[0]
#         throughput = row["Throughput"].values[0]
#         inflight = row["Inflight_Flits"].values[0]
#         route_mode = row["Routing"].values[0]
#     else:
#         latency, energy, throughput, inflight, route_mode = 10.0, 50.0, 0.5, 100, "ADAPTIVE"
# else:
#     st.error("Dataset not found. Using simulation defaults.")
#     latency, energy, throughput, inflight, route_mode = 10.0, 50.0, 0.5, 100, "ADAPTIVE"

# st.sidebar.info(f"Mode: {route_mode}")

# # ======================
# # 🔷 TOPOLOGY GENERATION
# # ======================
# G = nx.grid_2d_graph(size, size)
# if topology == "Flattened Butterfly":
#     # Add bypass edges for express routing
#     for i in range(size):
#         for j in range(size):
#             for k in range(size):
#                 if k != j: G.add_edge((i, j), (i, k))
#                 if k != i: G.add_edge((i, j), (k, j))

# # ======================
# # 🔥 TRAFFIC CONGESTION HEATMAP
# # ======================
# # Initialize heatmap based on traffic pattern
# traffic = np.zeros((size, size))
# if traffic_type == "hotspot":
#     traffic[size//2, size//2] = 0.8  # Center is hot
#     traffic[size//2-1, size//2] = 0.6
# elif traffic_type == "transpose":
#     for i in range(size): traffic[i, size-1-i] = 0.5
# else:
#     traffic = (np.random.rand(size, size) ** 2) * inj

# # ======================
# # 🧠 CONGESTION-AWARE ROUTING LOGIC
# # ======================
# num_packets = int(inj * 20) + 2
# all_paths = []
# nodes = list(G.nodes())

# for _ in range(num_packets):
#     s = nodes[np.random.randint(len(nodes))]
#     d = nodes[np.random.randint(len(nodes))]
#     while d == s: d = nodes[np.random.randint(len(nodes))]

#     try:
#         # 1. Update Edge Weights based on Heatmap (THE FIX)
#         for u, v in G.edges():
#             # Get congestion from the heatmap grid
#             u_cong = traffic[u[0], u[1]]
#             v_cong = traffic[v[0], v[1]]
#             avg_cong = (u_cong + v_cong) / 2

#             # THE WALL: Total avoidance of Red Zones (> 0.4)
#             if avg_cong > 0.4:
#                 weight = 10000 
#             else:
#                 weight = 1 + (avg_cong * 30)**2
#             G[u][v]['weight'] = weight

#         # 2. Pattern-Based Routing
#         if route_mode == "VALIANT":
#             mid = nodes[np.random.randint(len(nodes))]
#             path = nx.shortest_path(G, s, mid, weight='weight') + nx.shortest_path(G, mid, d, weight='weight')[1:]
#         elif route_mode == "RAN_MIN":
#             # Find paths that are congestion-minimal
#             path = nx.shortest_path(G, s, d, weight='weight')
#         else:
#             path = nx.shortest_path(G, s, d, weight='weight')

#         # 3. Update Heatmap dynamically
#         for node in path:
#             traffic[node[0], node[1]] = min(1.0, traffic[node[0], node[1]] + 0.03)
        
#         all_paths.append(path)
#     except:
#         continue

# # ======================
# # 🔷 VISUALIZATION
# # ======================
# fig_grid = go.Figure()

# # Draw Base Grid
# edge_x, edge_y = [], []
# for e in G.edges():
#     edge_x += [e[0][0], e[1][0], None]
#     edge_y += [e[0][1], e[1][1], None]
# fig_grid.add_trace(go.Scatter(x=edge_x, y=edge_y, mode="lines", line=dict(color="#333", width=0.7), hoverinfo='none'))

# # Draw Adaptive Paths
# colors = ['#FF4B4B', '#00CC96', '#636EFA', '#AB63FA', '#FFA15A']
# for i, path in enumerate(all_paths[:10]): # Show first 10 for clarity
#     px = [p[0] for p in path]
#     py = [p[1] for p in path]
#     fig_grid.add_trace(go.Scatter(x=px, y=py, mode="lines+markers", line=dict(width=3, color=colors[i % len(colors)])))

# fig_grid.update_layout(title=f"{topology} Paths - {traffic_type.upper()} Pattern", showlegend=False)
# st.plotly_chart(fig_grid, use_container_width=True)

# # Heatmap
# st.subheader("Traffic Congestion Heatmap")
# fig_heat = go.Figure(data=go.Heatmap(z=traffic.T, colorscale='RdYlGn_r', zmin=0, zmax=0.7))
# st.plotly_chart(fig_heat, use_container_width=True)

# # Metrics
# st.subheader("System Performance")
# c1, c2, c3, c4 = st.columns(4)
# c1.metric("Latency", f"{round(latency, 2)} ns")
# c2.metric("Energy", f"{round(energy, 2)} pJ")
# c3.metric("Throughput", f"{round(throughput, 3)} Gbps")
# c4.metric("Inflight Flits", round(inflight, 2))

# # Performance Bar
# fig_perf = go.Figure(go.Bar(x=["Latency", "Energy", "Throughput"], y=[latency, energy, throughput*100], marker_color='teal'))
# st.plotly_chart(fig_perf, use_container_width=True)






# import networkx as nx
# import streamlit as st
# import numpy as np
# import plotly.graph_objects as go
# import pandas as pd


# st.set_page_config(layout="wide", page_title="Energy Optimized NoC")

# st.title("⚡ Energy Optimized Adaptive NoC with Traffic Patterns")

# # ======================
# # 🔷 LOAD DATASET
# # ======================
# @st.cache_data
# def get_data():
#     try:
#         df = pd.read_csv("noc_dataset_realistic.csv")
#         df.columns = df.columns.str.strip()
#         return df
#     except:
#         return None

# data = get_data()

# # ======================
# # 🔷 SIDEBAR & PARAMETERS
# # ======================
# size = st.sidebar.selectbox("Network Size", [4, 8, 16])
# inj = st.sidebar.slider("Injection Rate", 0.01, 1.5, 0.7)
# traffic_type = st.sidebar.selectbox("Traffic Pattern", ["uniform", "hotspot", "transpose", "bit_complement"])
# topology = st.sidebar.selectbox("Topology", ["Mesh", "Flattened Butterfly"])

# # ======================
# # 🔷 FILTER DATASET FOR METRICS
# # ======================
# if data is not None:
#     filtered = data[(data["Size"] == size) & (data["Traffic"].str.lower() == traffic_type.lower())]
#     if not filtered.empty:
#         row = filtered.iloc[(filtered["Injection_Rate"] - inj).abs().argsort()[:1]]
#         latency = row["Latency"].values[0]
#         energy = row["Energy"].values[0]
#         throughput = row["Throughput"].values[0]
#         inflight = row["Inflight_Flits"].values[0]
#         route_mode = row["Routing"].values[0]
#     else:
#         latency, energy, throughput, inflight, route_mode = 10.0, 50.0, 0.5, 100, "ADAPTIVE"
# else:
#     st.error("Dataset not found. Using simulation defaults.")
#     latency, energy, throughput, inflight, route_mode = 10.0, 50.0, 0.5, 100, "ADAPTIVE"

# st.sidebar.info(f"Mode: {route_mode}")

# # ======================
# # 🔷 TOPOLOGY GENERATION
# # ======================
# G = nx.grid_2d_graph(size, size)
# if topology == "Flattened Butterfly":
#     # Add bypass edges for express routing
#     for i in range(size):
#         for j in range(size):
#             for k in range(size):
#                 if k != j: G.add_edge((i, j), (i, k))
#                 if k != i: G.add_edge((i, j), (k, j))

# # ======================
# # 🔥 TRAFFIC CONGESTION HEATMAP
# # ======================
# # Initialize heatmap based on traffic pattern
# traffic = np.zeros((size, size))
# if traffic_type == "hotspot":
#     traffic[size//2, size//2] = 0.8  # Center is hot
#     traffic[size//2-1, size//2] = 0.6
# elif traffic_type == "transpose":
#     for i in range(size): traffic[i, size-1-i] = 0.5
# else:
#     traffic = (np.random.rand(size, size) ** 2) * inj

# # ======================
# # 🧠 CONGESTION-AWARE ROUTING LOGIC
# # ======================
# num_packets = int(inj * 20) + 2
# all_paths = []
# nodes = list(G.nodes())

# for _ in range(num_packets):
#     s = nodes[np.random.randint(len(nodes))]
#     d = nodes[np.random.randint(len(nodes))]
#     while d == s: d = nodes[np.random.randint(len(nodes))]

#     try:
#         # 1. Update Edge Weights based on Heatmap (THE FIX)
#         for u, v in G.edges():
#             # Get congestion from the heatmap grid
#             u_cong = traffic[u[0], u[1]]
#             v_cong = traffic[v[0], v[1]]
#             avg_cong = (u_cong + v_cong) / 2

#             # THE WALL: Total avoidance of Red Zones (> 0.4)
#             if avg_cong > 0.4:
#                 weight = 10000 
#             else:
#                 weight = 1 + (avg_cong * 30)**2
#             G[u][v]['weight'] = weight

#         # 2. Pattern-Based Routing
#         if route_mode == "VALIANT":
#             mid = nodes[np.random.randint(len(nodes))]
#             path = nx.shortest_path(G, s, mid, weight='weight') + nx.shortest_path(G, mid, d, weight='weight')[1:]
#         elif route_mode == "RAN_MIN":
#             # Find paths that are congestion-minimal
#             path = nx.shortest_path(G, s, d, weight='weight')
#         else:
#             path = nx.shortest_path(G, s, d, weight='weight')

#         # 3. Update Heatmap dynamically
#         for node in path:
#             traffic[node[0], node[1]] = min(1.0, traffic[node[0], node[1]] + 0.03)
        
#         all_paths.append(path)
#     except:
#         continue

# # ======================
# # 🔷 VISUALIZATION
# # ======================
# fig_grid = go.Figure()

# # Draw Base Grid
# edge_x, edge_y = [], []
# for e in G.edges():
#     edge_x += [e[0][0], e[1][0], None]
#     edge_y += [e[0][1], e[1][1], None]
# fig_grid.add_trace(go.Scatter(x=edge_x, y=edge_y, mode="lines", line=dict(color="#333", width=0.7), hoverinfo='none'))

# # Draw Adaptive Paths
# colors = ['#FF4B4B', '#00CC96', '#636EFA', '#AB63FA', '#FFA15A']
# for i, path in enumerate(all_paths[:10]): # Show first 10 for clarity
#     px = [p[0] for p in path]
#     py = [p[1] for p in path]
#     fig_grid.add_trace(go.Scatter(x=px, y=py, mode="lines+markers", line=dict(width=3, color=colors[i % len(colors)])))

# fig_grid.update_layout(title=f"{topology} Paths - {traffic_type.upper()} Pattern", showlegend=False)
# st.plotly_chart(fig_grid, use_container_width=True)

# # Heatmap
# st.subheader("Traffic Congestion Heatmap")
# fig_heat = go.Figure(data=go.Heatmap(z=traffic.T, colorscale='RdYlGn_r', zmin=0, zmax=0.7))
# st.plotly_chart(fig_heat, use_container_width=True)

# # Metrics
# st.subheader("System Performance")
# c1, c2, c3, c4 = st.columns(4)
# c1.metric("Latency", f"{round(latency, 2)} ns")
# c2.metric("Energy", f"{round(energy, 2)} pJ")
# c3.metric("Throughput", f"{round(throughput, 3)} Gbps")
# c4.metric("Inflight Flits", round(inflight, 2))

# # Performance Bar
# fig_perf = go.Figure(go.Bar(x=["Latency", "Energy", "Throughput"], y=[latency, energy, throughput*100], marker_color='teal'))
# st.plotly_chart(fig_perf, use_container_width=True)





import networkx as nx
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(layout="wide", page_title="Energy Optimized NoC")

st.title("⚡ Energy Optimized Adaptive NoC with Traffic Patterns")

# ======================
# 🔷 LOAD DATASET
# ======================
@st.cache_data
def get_data():
    try:
        df = pd.read_csv("noc_dataset_realistic.csv")
        df.columns = df.columns.str.strip()
        return df
    except:
        return None

data = get_data()

# ======================
# 🔷 SIDEBAR
# ======================
size = st.sidebar.selectbox("Network Size", [4, 8, 16])
inj = st.sidebar.slider("Injection Rate", 0.01, 1.5, 0.7)
traffic_type = st.sidebar.selectbox(
    "Traffic Pattern", ["uniform", "hotspot", "transpose", "bit_complement"]
)
topology = st.sidebar.selectbox("Topology", ["Mesh", "Flattened Butterfly"])

# ======================
# 🔷 DATASET FILTER (ONLY DISPLAY PURPOSE)
# ======================
if data is not None:
    filtered = data[
        (data["Size"] == size) &
        (data["Traffic"].str.lower() == traffic_type.lower())
    ]
    if not filtered.empty:
        row = filtered.iloc[(filtered["Injection_Rate"] - inj).abs().argsort()[:1]]
        route_mode = row["Routing"].values[0]
    else:
        route_mode = "ADAPTIVE"
else:
    route_mode = "ADAPTIVE"

st.sidebar.info(f"Mode: {route_mode}")

# ======================
# 🔷 TOPOLOGY
# ======================
G = nx.grid_2d_graph(size, size)

if topology == "Flattened Butterfly":
    # Add long-range express links
    for i in range(size):
        for j in range(size):
            for k in range(size):
                if k != j:
                    G.add_edge((i, j), (i, k))
                if k != i:
                    G.add_edge((i, j), (k, j))

# ======================
# 🔥 TRAFFIC HEATMAP
# ======================
traffic = np.zeros((size, size))

if traffic_type == "hotspot":
    traffic[size//2, size//2] = 0.9
    traffic[size//2-1, size//2] = 0.7

elif traffic_type == "transpose":
    for i in range(size):
        traffic[i, size-1-i] = 0.6

elif traffic_type == "bit_complement":
    for i in range(size):
        for j in range(size):
            traffic[i, j] = abs((i ^ j) % size) / size

else:  # uniform
    traffic = (np.random.rand(size, size) ** 2) * inj

# ======================
# 🧠 CONGESTION-AWARE ROUTING
# ======================
num_packets = int(inj * 20) + 3
nodes = list(G.nodes())

all_paths = []
total_hops = 0

for _ in range(num_packets):

    s = nodes[np.random.randint(len(nodes))]
    d = nodes[np.random.randint(len(nodes))]

    while d == s:
        d = nodes[np.random.randint(len(nodes))]

    try:
        # 🔥 EDGE WEIGHT (CONGESTION + TOPOLOGY AWARE)
        for u, v in G.edges():
            u_cong = traffic[u[0], u[1]]
            v_cong = traffic[v[0], v[1]]
            avg_cong = (u_cong + v_cong) / 2

            if avg_cong > 0.4:
                weight = 10000
            else:
                weight = 1 + (avg_cong * 30)**2

            # 🔥 FLATFLY ADVANTAGE
            if topology == "Flattened Butterfly":
                if u[0] == v[0] or u[1] == v[1]:
                    weight *= 0.3  # faster express link

            G[u][v]['weight'] = weight

        # ROUTING
        if route_mode == "VALIANT":
            mid = nodes[np.random.randint(len(nodes))]
            path = nx.shortest_path(G, s, mid, weight='weight') + \
                   nx.shortest_path(G, mid, d, weight='weight')[1:]
        else:
            path = nx.shortest_path(G, s, d, weight='weight')

        # 🔥 UPDATE TRAFFIC (DYNAMIC CONGESTION)
        for node in path:
            traffic[node[0], node[1]] = min(1.0, traffic[node[0], node[1]] + 0.03)

        total_hops += len(path) - 1
        all_paths.append(path)

    except:
        continue

# ======================
# 📊 VISUALIZATION
# ======================
fig = go.Figure()

# Draw edges
edge_x, edge_y = [], []
for e in G.edges():
    edge_x += [e[0][0], e[1][0], None]
    edge_y += [e[0][1], e[1][1], None]

fig.add_trace(go.Scatter(
    x=edge_x, y=edge_y,
    mode="lines",
    line=dict(color="#444", width=0.6),
    hoverinfo='none'
))

# Draw paths
colors = ['red', 'green', 'blue', 'purple', 'orange']

for i, path in enumerate(all_paths[:10]):
    px = [p[0] for p in path]
    py = [p[1] for p in path]

    fig.add_trace(go.Scatter(
        x=px, y=py,
        mode="lines+markers",
        line=dict(width=3, color=colors[i % len(colors)])
    ))

fig.update_layout(
    title=f"{topology} Traffic ({traffic_type})",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# ======================
# 🔥 HEATMAP
# ======================
st.subheader("Traffic Congestion Heatmap")

heat = go.Figure(
    data=go.Heatmap(
        z=traffic.T,
        colorscale='RdYlGn_r',
        zmin=0,
        zmax=1
    )
)

st.plotly_chart(heat, use_container_width=True)

# ======================
# 📈 METRICS (FIXED)
# ======================
if len(all_paths) > 0:
    avg_hops = total_hops / len(all_paths)
else:
    avg_hops = 1

latency = avg_hops * (1 + np.mean(traffic) * 5)

if topology == "Flattened Butterfly":
    energy = avg_hops * 1.5
else:
    energy = avg_hops * 2.5

throughput = 1 / (latency + 0.5)

# ======================
# 📊 PERFORMANCE
# ======================
# st.subheader("System Performance")

# c1, c2, c3= st.columns(3)
# c1.metric("Latency", round(latency, 2))
# c2.metric("Energy", round(energy, 2))
# c3.metric("Throughput", round(throughput, 3))

# ======================
# 📊 METRICS DISPLAY
# ======================
st.subheader("System Performance")

# 🔥 Calculate inflight flits (NEW ADDITION)
inflight = np.sum(traffic) * size

c1, c2, c3, c4 = st.columns(4)

c1.metric("Latency", f"{round(latency, 2)} ns")
c2.metric("Energy", f"{round(energy, 2)} pJ")
c3.metric("Throughput", f"{round(throughput, 3)} Gbps")
c4.metric("Inflight Flits", round(inflight, 2))

fig_perf = go.Figure(go.Bar(
    x=["Latency", "Energy", "Throughput"],
    y=[latency, energy, throughput * 100], marker_color='teal'
))

st.plotly_chart(fig_perf, use_container_width=True)
