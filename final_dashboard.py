<<<<<<< HEAD
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import networkx as nx
import joblib
import pandas as pd

st.set_page_config(layout="wide", page_title="Energy Optimized NoC")

st.title("🚀 Energy Optimized Adaptive Network-on-Chip")

# ======================
# 🔷 LOAD DATASET & MODEL
# ======================
@st.cache_resource
def load_assets():
    try:
        data = pd.read_csv("D:/FYP/final/noc_dataset.csv")
        model = joblib.load("noc_model.pkl")
        return data, model
    except:
        # Fallback if files aren't in place for testing
        return None, None

data, model = load_assets()

if data is not None:
    st.success("✅ System Ready")
else:
    st.warning("⚠️ Running in Simulation Mode (Dataset/Model not found)")

# ======================
# 🔷 SIDEBAR CONTROLS
# ======================
size = st.sidebar.selectbox("Network Size (NxN)", [4, 8, 16])
inj = st.sidebar.slider("Injection Rate (Traffic Load)", 0.01, 1.5, 0.7)
topology = st.sidebar.selectbox("Topology", ["Mesh", "Flattened Butterfly"])

if model:
    route_type = model.predict([[inj, size]])[0]
    st.sidebar.info(f"Model Prediction: {route_type}")

# ======================
# 🔷 NETWORK SETUP
# ======================
if topology == "Mesh":
    G = nx.grid_2d_graph(size, size)
else:
    # Flattened Butterfly: Start with Mesh, add long-range bypasses
    G = nx.grid_2d_graph(size, size)
    for i in range(size):
        for j in range(size):
            for k in range(size):
                if k != j: G.add_edge((i, j), (i, k)) # Horizontal express
                if k != i: G.add_edge((i, j), (k, j)) # Vertical express

# ======================
# 🔥 HEATMAP INITIALIZATION
# ======================
# Generate initial random congestion spots
traffic = (np.random.rand(size, size) ** 2) * inj

# ======================
# 🧠 TRULY ADAPTIVE ROUTING (CONGESTION-AVOIDANCE)
# ======================
num_packets = int(inj * 15) + 2
all_paths = []

for _ in range(num_packets):
    # Random Source/Dest
    s = (np.random.randint(0, size), np.random.randint(0, size))
    d = (np.random.randint(0, size), np.random.randint(0, size))
    while d == s:
        d = (np.random.randint(0, size), np.random.randint(0, size))

    try:
        # DYNAMIC WEIGHTING: We update edge weights based on the heatmap
        for u, v in G.edges():
            u_cong = traffic[u[0]][u[1]]
            v_cong = traffic[v[0]][v[1]]
            avg_cong = (u_cong + v_cong) / 2

            # THE "WALL" LOGIC:
            # If a node is Red (>0.4), the cost becomes massive (10,000)
            # Otherwise, cost grows exponentially with traffic
            if avg_cong > 0.4:
                weight = 10000 
            else:
                weight = 1 + (avg_cong * 20)**3 
            
            G[u][v]['weight'] = weight

        # Find the path with the lowest TOTAL congestion cost (Dijkstra)
        # This will detour around red zones even if the path is longer
        path = nx.shortest_path(G, source=s, target=d, weight='weight')
        
        # Update traffic dynamically as packets pass through
        for node in path:
            traffic[node[0]][node[1]] += 0.04
            
        all_paths.append(path)
    except:
        continue

# ======================
# 🔷 VISUALIZATION (PLOTLY)
# ======================
fig = go.Figure()

# Draw Edges
edge_x, edge_y = [], []
for e in G.edges():
    edge_x += [e[0][0], e[1][0], None]
    edge_y += [e[0][1], e[1][1], None]
fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode="lines", line=dict(color="#444", width=0.5), hoverinfo='none'))

# Draw Paths (Traces)
colors = ['#FF4B4B', '#00CC96', '#636EFA', '#AB63FA', '#FFA15A']
for i, path in enumerate(all_paths):
    px = [p[0] for p in path]
    py = [p[1] for p in path]
    fig.add_trace(go.Scatter(x=px, y=py, mode="lines+markers", 
                             line=dict(width=3, color=colors[i % len(colors)]),
                             name=f"Packet {i+1}"))

fig.update_layout(title=f"Adaptive {topology} Routing Paths", showlegend=False,
                  xaxis=dict(showgrid=False, zeroline=False), yaxis=dict(showgrid=False, zeroline=False))

st.plotly_chart(fig, use_container_width=True)

# ======================
# 🔥 HEATMAP
# ======================
st.subheader("Traffic Congestion Heatmap")
# We transpose traffic for visual alignment with the grid
fig_heat = go.Figure(data=go.Heatmap(
    z=traffic.T, 
    colorscale='RdYlGn_r', 
    zmin=0, zmax=0.8,
    colorbar=dict(title="Congestion Level")
))
fig_heat.update_layout(xaxis_title="X-Coordinate", yaxis_title="Y-Coordinate")
st.plotly_chart(fig_heat, use_container_width=True)

# ======================
# 🔥 PERFORMANCE METRICS
# ======================
st.subheader("System Performance")
latency = np.mean(traffic) * size * 5
energy = np.sum(traffic) * 1.2
throughput = 1 / (latency + 0.1)

c1, c2, c3 = st.columns(3)
c1.metric("Latency", f"{round(latency, 2)} ns")
c2.metric("Energy", f"{round(energy, 2)} pJ")
c3.metric("Throughput", f"{round(throughput, 3)} Gbps")

fig_perf = go.Figure(go.Bar(
    x=["Latency", "Energy", "Throughput"],
    y=[latency, energy, throughput * 100], # Scaled for visibility
    marker_color=['#EF553B', '#00CC96', '#636EFA']
))
st.plotly_chart(fig_perf, use_container_width=True)







# import streamlit as st
# import numpy as np
# import plotly.graph_objects as go
# import networkx as nx
# import joblib
# import pandas as pd
# import time

# st.set_page_config(layout="wide")

# st.title("Energy Optimized Adaptive Network-on-Chip")

# # ======================
# # 🔷 LOAD DATASET
# # ======================
# try:
#     data = pd.read_csv("D:/FYP/final/noc_dataset.csv")
#     data.columns = data.columns.str.strip()

#     st.success("✅ Dataset Loaded Successfully")

#     st.subheader("Dataset Overview")
#     st.dataframe(data.head())

# except Exception as e:
#     st.error(f"❌ Dataset Error: {e}")

# # ======================
# # 🔷 LOAD MODEL
# # ======================
# model = joblib.load("noc_model.pkl")

# # ======================
# # 🔷 SIDEBAR
# # ======================
# size = st.sidebar.selectbox("Network Size", [4, 8, 16])
# inj = st.sidebar.slider("Injection Rate", 0.01, 1.5, 0.5)

# topology = st.sidebar.selectbox("Topology", ["Mesh", "Flattened Butterfly"])

# route = model.predict([[inj, size]])[0]
# st.sidebar.write("Routing:", route)

# # ======================
# # 🔷 TOPOLOGY
# # ======================
# if topology == "Mesh":
#     G = nx.grid_2d_graph(size, size)
# else:
#     G = nx.complete_graph(size)  # simplified flatfly

# # ======================
# # 🔥 TRAFFIC MODEL
# # ======================
# traffic = np.random.rand(size, size) * inj

# # ======================
# # 🔥 MULTI-PATH TRAFFIC (FIXED)
# # ======================
# num_packets = int(inj * 10) + 1
# all_paths = []

# for _ in range(num_packets):

#     # ✅ FIX 1: NODE TYPE BASED ON TOPOLOGY
#     if topology == "Mesh":
#         s = (np.random.randint(0,size), np.random.randint(0,size))
#         d = (np.random.randint(0,size), np.random.randint(0,size))
#     else:
#         s = np.random.randint(0, size)
#         d = np.random.randint(0, size)

#     while d == s:
#         if topology == "Mesh":
#             d = (np.random.randint(0,size), np.random.randint(0,size))
#         else:
#             d = np.random.randint(0, size)

#     # ======================
#     # ROUTING LOGIC (FIXED)
#     # ======================
#     if route == "RAN_MIN":
#         if s in G.nodes and d in G.nodes:
#             try:
#                 paths = list(nx.all_shortest_paths(G, s, d))
#                 if len(paths) > 0:
#                     path = paths[np.random.randint(len(paths))]
#                 else:
#                     continue
#             except:
#                 continue
#         else:
#             continue

#     elif route == "VALIANT":

#         # ✅ FIX 2: MID NODE TYPE
#         if topology == "Mesh":
#             mid = (np.random.randint(0,size), np.random.randint(0,size))
#         else:
#             mid = np.random.randint(0, size)

#         try:
#             p1 = nx.shortest_path(G, s, mid)
#             p2 = nx.shortest_path(G, mid, d)
#             path = p1 + p2[1:]
#         except:
#             continue

#     else:  # DOR
#         try:
#             path = nx.shortest_path(G, s, d)
#         except:
#             continue

#     all_paths.append(path)

# # ======================
# # 🔷 DRAW NETWORK
# # ======================
# edge_x, edge_y = [], []
# for e in G.edges():
#     x0,y0 = e[0] if isinstance(e[0], tuple) else (e[0], 0)
#     x1,y1 = e[1] if isinstance(e[1], tuple) else (e[1], 0)
#     edge_x += [x0,x1,None]
#     edge_y += [y0,y1,None]

# edge_trace = go.Scatter(x=edge_x, y=edge_y, mode="lines")

# node_x, node_y = [], []
# for n in G.nodes():
#     node_x.append(n[0] if isinstance(n, tuple) else n)
#     node_y.append(n[1] if isinstance(n, tuple) else 0)

# node_trace = go.Scatter(
#     x=node_x,
#     y=node_y,
#     mode="markers",
#     marker=dict(size=10, color="lightblue")
# )

# # ======================
# # 🔥 MULTI PATH VISUAL
# # ======================
# path_traces = []

# for path in all_paths:
#     px = [p[0] if isinstance(p, tuple) else p for p in path]
#     py = [p[1] if isinstance(p, tuple) else 0 for p in path]

#     path_traces.append(
#         go.Scatter(x=px, y=py, mode="lines")
#     )

# fig = go.Figure(data=[edge_trace, node_trace] + path_traces)
# fig.update_layout(title=f"{size}x{size} {topology} Traffic")

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
# # 🔥 METRICS
# # ======================
# latency = np.mean(traffic) * size * 10
# energy = np.sum(traffic) * 2
# throughput = 1/(latency+1)

# # ======================
# # 🔥 METRIC GRAPH
# # ======================
# st.subheader("Performance Graph")

# fig_perf = go.Figure()

# fig_perf.add_trace(go.Bar(
#     x=["Latency","Energy","Throughput"],
#     y=[latency, energy, throughput]
# ))

# st.plotly_chart(fig_perf, width='stretch')

# c1,c2,c3 = st.columns(3)
# c1.metric("Latency", round(latency,2))
# c2.metric("Energy", round(energy,2))
# c3.metric("Throughput", round(throughput,3))

=======
# import streamlit as st
# import numpy as np
# import plotly.graph_objects as go
# import networkx as nx
# import joblib
# import pandas as pd
# import time

# st.set_page_config(layout="wide")

# st.title("Energy Optimized Adaptive Network-on-Chip")

# # ======================
# # 🔷 LOAD DATASET
# # ======================
# try:
#     data = pd.read_csv("noc_dataset.csv")

#     st.subheader("Dataset Overview")
#     st.dataframe(data.head())

#     fig_data = go.Figure()

#     fig_data.add_trace(go.Scatter(
#         x=data['Injection_Rate'],
#         y=data['DOR_Flit_Lat'],
#         name='DOR'
#     ))

#     fig_data.add_trace(go.Scatter(
#         x=data['Injection_Rate'],
#         y=data['Valiant_Flit_Lat'],
#         name='Valiant'
#     ))

#     fig_data.add_trace(go.Scatter(
#         x=data['Injection_Rate'],
#         y=data['Ranmin_Flit_Lat'],
#         name='RAN_MIN'
#     ))

#     fig_data.update_layout(title="Latency Comparison")

#     st.plotly_chart(fig_data, width='stretch')

# except:
#     st.warning("Dataset not loaded")

# # ======================
# # 🔷 LOAD MODEL
# # ======================
# model = joblib.load("noc_model.pkl")

# # ======================
# # 🔷 SIDEBAR
# # ======================
# size = st.sidebar.selectbox("Network Size", [4, 8, 16])
# inj = st.sidebar.slider("Injection Rate", 0.01, 1.5, 0.5)

# topology = st.sidebar.selectbox("Topology", ["Mesh", "Flattened Butterfly"])

# route = model.predict([[inj, size]])[0]
# st.sidebar.write("Routing:", route)

# # ======================
# # 🔷 TOPOLOGY
# # ======================
# if topology == "Mesh":
#     G = nx.grid_2d_graph(size, size)
# else:
#     G = nx.complete_graph(size)  # simplified flatfly

# # ======================
# # 🔥 TRAFFIC MODEL
# # ======================
# traffic = np.random.rand(size, size) * inj

# # ======================
# # 🔥 MULTI-PATH TRAFFIC
# # ======================
# num_packets = int(inj * 10) + 1
# all_paths = []

# for _ in range(num_packets):

#     s = (np.random.randint(0,size), np.random.randint(0,size))
#     d = (np.random.randint(0,size), np.random.randint(0,size))

#     while d == s:
#         d = (np.random.randint(0,size), np.random.randint(0,size))

#     if route == "RAN_MIN":
#         paths = list(nx.all_shortest_paths(G, s, d))
#         path = paths[np.random.randint(len(paths))]
#     elif route == "VALIANT":
#         mid = (np.random.randint(0,size), np.random.randint(0,size))
#         p1 = nx.shortest_path(G, s, mid)
#         p2 = nx.shortest_path(G, mid, d)
#         path = p1 + p2[1:]
#     else:
#         path = nx.shortest_path(G, s, d)

#     all_paths.append(path)

# # ======================
# # 🔷 DRAW NETWORK
# # ======================
# edge_x, edge_y = [], []
# for e in G.edges():
#     x0,y0 = e[0]
#     x1,y1 = e[1]
#     edge_x += [x0,x1,None]
#     edge_y += [y0,y1,None]

# edge_trace = go.Scatter(x=edge_x, y=edge_y, mode="lines")

# node_x, node_y = [], []
# for n in G.nodes():
#     node_x.append(n[0] if isinstance(n, tuple) else n)
#     node_y.append(n[1] if isinstance(n, tuple) else 0)

# node_trace = go.Scatter(
#     x=node_x,
#     y=node_y,
#     mode="markers",
#     marker=dict(size=10, color="lightblue")
# )

# # ======================
# # 🔥 MULTI PATH VISUAL
# # ======================
# path_traces = []

# for path in all_paths:
#     px = [p[0] if isinstance(p, tuple) else p for p in path]
#     py = [p[1] if isinstance(p, tuple) else 0 for p in path]

#     path_traces.append(
#         go.Scatter(x=px, y=py, mode="lines")
#     )

# fig = go.Figure(data=[edge_trace, node_trace] + path_traces)

# fig.update_layout(title=f"{size}x{size} {topology} Traffic")

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
# # 🔥 METRICS
# # ======================
# latency = np.mean(traffic) * size * 10
# energy = np.sum(traffic) * 2
# throughput = 1/(latency+1)

# # ======================
# # 🔥 METRIC GRAPH
# # ======================
# st.subheader("Performance Graph")

# fig_perf = go.Figure()

# fig_perf.add_trace(go.Bar(x=["Latency","Energy","Throughput"],
#                          y=[latency, energy, throughput]))

# st.plotly_chart(fig_perf, width='stretch')

# c1,c2,c3 = st.columns(3)
# c1.metric("Latency", round(latency,2))
# c2.metric("Energy", round(energy,2))
# c3.metric("Throughput", round(throughput,3))






import streamlit as st
import numpy as np
import plotly.graph_objects as go
import networkx as nx
import joblib
import pandas as pd
import time

st.set_page_config(layout="wide")

st.title("Energy Optimized Adaptive Network-on-Chip")

# ======================
# 🔷 LOAD DATASET
# ======================
try:
    data = pd.read_csv("D:/FYP/final/noc_dataset.csv")
    data.columns = data.columns.str.strip()

    st.success("✅ Dataset Loaded Successfully")

    st.subheader("Dataset Overview")
    st.dataframe(data.head())

except Exception as e:
    st.error(f"❌ Dataset Error: {e}")

# ======================
# 🔷 LOAD MODEL
# ======================
model = joblib.load("noc_model.pkl")

# ======================
# 🔷 SIDEBAR
# ======================
size = st.sidebar.selectbox("Network Size", [4, 8, 16])
inj = st.sidebar.slider("Injection Rate", 0.01, 1.5, 0.5)

topology = st.sidebar.selectbox("Topology", ["Mesh", "Flattened Butterfly"])

route = model.predict([[inj, size]])[0]
st.sidebar.write("Routing:", route)

# ======================
# 🔷 TOPOLOGY
# ======================
if topology == "Mesh":
    G = nx.grid_2d_graph(size, size)
else:
    G = nx.complete_graph(size)  # simplified flatfly

# ======================
# 🔥 TRAFFIC MODEL
# ======================
traffic = np.random.rand(size, size) * inj

# ======================
# 🔥 MULTI-PATH TRAFFIC (FIXED)
# ======================
num_packets = int(inj * 10) + 1
all_paths = []

for _ in range(num_packets):

    # ✅ FIX 1: NODE TYPE BASED ON TOPOLOGY
    if topology == "Mesh":
        s = (np.random.randint(0,size), np.random.randint(0,size))
        d = (np.random.randint(0,size), np.random.randint(0,size))
    else:
        s = np.random.randint(0, size)
        d = np.random.randint(0, size)

    while d == s:
        if topology == "Mesh":
            d = (np.random.randint(0,size), np.random.randint(0,size))
        else:
            d = np.random.randint(0, size)

    # ======================
    # ROUTING LOGIC (FIXED)
    # ======================
    if route == "RAN_MIN":
        if s in G.nodes and d in G.nodes:
            try:
                paths = list(nx.all_shortest_paths(G, s, d))
                if len(paths) > 0:
                    path = paths[np.random.randint(len(paths))]
                else:
                    continue
            except:
                continue
        else:
            continue

    elif route == "VALIANT":

        # ✅ FIX 2: MID NODE TYPE
        if topology == "Mesh":
            mid = (np.random.randint(0,size), np.random.randint(0,size))
        else:
            mid = np.random.randint(0, size)

        try:
            p1 = nx.shortest_path(G, s, mid)
            p2 = nx.shortest_path(G, mid, d)
            path = p1 + p2[1:]
        except:
            continue

    else:  # DOR
        try:
            path = nx.shortest_path(G, s, d)
        except:
            continue

    all_paths.append(path)

# ======================
# 🔷 DRAW NETWORK
# ======================
edge_x, edge_y = [], []
for e in G.edges():
    x0,y0 = e[0] if isinstance(e[0], tuple) else (e[0], 0)
    x1,y1 = e[1] if isinstance(e[1], tuple) else (e[1], 0)
    edge_x += [x0,x1,None]
    edge_y += [y0,y1,None]

edge_trace = go.Scatter(x=edge_x, y=edge_y, mode="lines")

node_x, node_y = [], []
for n in G.nodes():
    node_x.append(n[0] if isinstance(n, tuple) else n)
    node_y.append(n[1] if isinstance(n, tuple) else 0)

node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode="markers",
    marker=dict(size=10, color="lightblue")
)

# ======================
# 🔥 MULTI PATH VISUAL
# ======================
path_traces = []

for path in all_paths:
    px = [p[0] if isinstance(p, tuple) else p for p in path]
    py = [p[1] if isinstance(p, tuple) else 0 for p in path]

    path_traces.append(
        go.Scatter(x=px, y=py, mode="lines")
    )

fig = go.Figure(data=[edge_trace, node_trace] + path_traces)
fig.update_layout(title=f"{size}x{size} {topology} Traffic")

st.plotly_chart(fig, width='stretch')

# ======================
# 🔥 HEATMAP
# ======================
st.subheader("Traffic Congestion")

st.plotly_chart(
    go.Figure(data=go.Heatmap(z=traffic, colorscale='RdYlGn_r')),
    width='stretch'
)

# ======================
# 🔥 METRICS
# ======================
latency = np.mean(traffic) * size * 10
energy = np.sum(traffic) * 2
throughput = 1/(latency+1)

# ======================
# 🔥 METRIC GRAPH
# ======================
st.subheader("Performance Graph")

fig_perf = go.Figure()

fig_perf.add_trace(go.Bar(
    x=["Latency","Energy","Throughput"],
    y=[latency, energy, throughput]
))

st.plotly_chart(fig_perf, width='stretch')

c1,c2,c3 = st.columns(3)
c1.metric("Latency", round(latency,2))
c2.metric("Energy", round(energy,2))
c3.metric("Throughput", round(throughput,3))
>>>>>>> 830b243b2262255a572098fffbb088ffb579fb11
