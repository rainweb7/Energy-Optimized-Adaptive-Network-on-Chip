<<<<<<< HEAD
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("noc_dataset.csv")

# Latency graph
for size in [4,8,16]:
    subset = df[df['Size']==size]
    plt.plot(subset['Injection_Rate'],subset['Latency'],label=f"{size}x{size}")

plt.legend()
plt.xlabel("Injection Rate")
plt.ylabel("Latency")
plt.title("Latency vs Injection Rate")
=======
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("noc_dataset.csv")

# Latency graph
for size in [4,8,16]:
    subset = df[df['Size']==size]
    plt.plot(subset['Injection_Rate'],subset['Latency'],label=f"{size}x{size}")

plt.legend()
plt.xlabel("Injection Rate")
plt.ylabel("Latency")
plt.title("Latency vs Injection Rate")
>>>>>>> 830b243b2262255a572098fffbb088ffb579fb11
plt.show()