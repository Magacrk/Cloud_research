# collect_metrics.py
import time, json
import statistics
from edge_inference import run_inference

ENDPOINT = 'dnn-endpoint-1234567890'
K = 30
INTERVAL = 180  # seconds (3 min)
DURATION = 3600 # 1 hour
BUCKET  = 'research-bucket-bu'

results = []
start = time.time()
while time.time() - start < DURATION:
    t0 = time.time()
    lats = run_inference(ENDPOINT, K, runs=10)  # 10 inf per batch
    avg_lat = statistics.mean(lats)
    t_batch = time.time() - t0
    throughput = 10 / t_batch
    elapsed_min = (time.time() - start)/60
    # approximate cost so far (EC2 + SageMaker ~ $0.0964/hr)
    cost = 0.0964 * ((time.time()-start)/3600)
    results.append({
        'minute': elapsed_min,
        'avg_latency_s': avg_lat,
        'throughput_inf_s': throughput,
        'cost_usd': cost
    })
    print(results[-1])
    time.sleep(max(0, INTERVAL - (time.time()-t0)))

# write out
with open('time_series_k30.json','w') as f:
    json.dump(results, f, indent=2)
