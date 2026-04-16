<<<<<<< HEAD
import pandas as pd
import numpy as np

data = []

sizes = [4,8,16]
routes = ['DOR','VALIANT','RAN_MIN']

for size in sizes:
    for inj in np.linspace(0.01,1.5,200):
        for route in routes:

            base_latency = inj * size * 10

            if route == 'DOR':
                latency = base_latency + np.random.uniform(5,10)
            elif route == 'VALIANT':
                latency = base_latency + np.random.uniform(3,8)
            else:
                latency = base_latency + np.random.uniform(1,5)

            throughput = (1/inj) * np.random.uniform(0.5,1.2)
            inflight = inj * size * np.random.uniform(5,10)

            data.append([size,inj,route,latency,throughput,inflight])

df = pd.DataFrame(data,columns=[
'Size','Injection_Rate','Routing',
'Latency','Throughput','Inflight'])

df.to_csv("noc_dataset.csv",index=False)
=======
import pandas as pd
import numpy as np

data = []

sizes = [4,8,16]
routes = ['DOR','VALIANT','RAN_MIN']

for size in sizes:
    for inj in np.linspace(0.01,1.5,200):
        for route in routes:

            base_latency = inj * size * 10

            if route == 'DOR':
                latency = base_latency + np.random.uniform(5,10)
            elif route == 'VALIANT':
                latency = base_latency + np.random.uniform(3,8)
            else:
                latency = base_latency + np.random.uniform(1,5)

            throughput = (1/inj) * np.random.uniform(0.5,1.2)
            inflight = inj * size * np.random.uniform(5,10)

            data.append([size,inj,route,latency,throughput,inflight])

df = pd.DataFrame(data,columns=[
'Size','Injection_Rate','Routing',
'Latency','Throughput','Inflight'])

df.to_csv("noc_dataset.csv",index=False)
>>>>>>> 830b243b2262255a572098fffbb088ffb579fb11
print("Dataset created")