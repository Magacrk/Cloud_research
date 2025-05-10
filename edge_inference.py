#run command
#python3 edge_inference.py --endpoint dnn-endpoint-1234567890 --k 30 --runs 100





# edge_inference.py
import time, boto3
import numpy as np
import tensorflow as tf
import argparse

def run_inference(endpoint, k, runs=100):
    # load edge model
    edge = tf.keras.models.load_model('edge_model.h5')
    client = boto3.client('sagemaker-runtime', region_name='us-east-1')

    latencies = []
    for _ in range(runs):
        # random sample
        img = np.random.random((1,224,224,3)).astype('float32')
        t0 = time.time()
        out = edge.predict(img)
        resp = client.invoke_endpoint(
            EndpointName=endpoint,
            ContentType='application/octet-stream',
            Body=out.tobytes()
        )
        _ = resp['Body'].read()  # final output
        latencies.append(time.time() - t0)
    return latencies

if __name__=='__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--endpoint', required=True)
    p.add_argument('--k', type=int, default=30)
    p.add_argument('--runs', type=int, default=50)
    args = p.parse_args()

    lats = run_inference(args.endpoint, args.k, args.runs)
    print(f"Avg latency @k={args.k}: {np.mean(lats):.3f}s  (n={args.runs})")
    # save to file
    import json
    with open(f"latencies_k{args.k}.json","w") as f:
        json.dump(lats, f)
