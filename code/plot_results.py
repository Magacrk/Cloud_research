# plot_results.py
import json, matplotlib.pyplot as plt

# 6.1 Latency vs split point
lat_data = {
    10:0.39, 19:0.35, 30:0.34, 40:0.35
}
ks = sorted(lat_data)
plt.plot(ks, [lat_data[k] for k in ks], marker='o')
plt.scatter([30],[0.34], color='red', zorder=5)
plt.title("Total Inference Latency vs. Split Point (k)")
plt.xlabel("Split Point k")
plt.ylabel("Latency (s)")
plt.grid(True, ls='--', alpha=0.5)
plt.savefig('latency_vs_k.png', dpi=200)
plt.clf()

# 6.2 Time series for k=30
ts = json.load(open('time_series_k30.json'))
mins = [r['minute'] for r in ts]
lats = [r['avg_latency_s'] for r in ts]
costs= [r['cost_usd']        for r in ts]
thrpt= [r['throughput_inf_s']for r in ts]

fig, ax1 = plt.subplots()
ax1.plot(mins, lats, 'b-', label='Latency (s)')
ax1.set_xlabel('Time (min)')
ax1.set_ylabel('Latency (s)', color='b')
ax2 = ax1.twinx()
ax2.plot(mins, costs, 'r--', label='Cost ($)')
ax2.set_ylabel('Cost ($)', color='r')
plt.title("Latency & Cost over Time (k=30)")
plt.savefig('time_series_k30.png', dpi=200)
