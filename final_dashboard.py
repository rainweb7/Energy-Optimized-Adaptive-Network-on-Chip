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
