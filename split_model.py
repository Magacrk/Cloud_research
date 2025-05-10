# split_model.py
import tensorflow as tf
import argparse

def split_and_save(k):
    model = tf.keras.applications.ResNet50(weights='imagenet')
    # edge: layers 0..k
    edge = tf.keras.Model(inputs=model.input, outputs=model.layers[k].output)
    # cloud: layers k+1..end
    cloud = tf.keras.Model(inputs=model.layers[k+1].input, outputs=model.output)
    edge.save('edge_model.h5')
    cloud.save('cloud_model.h5')
    print(f"Saved edge_model.h5 and cloud_model.h5 with k={k}")

if __name__=='__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--k', type=int, default=30, help='Split point layer index')
    args = p.parse_args()
    split_and_save(args.k)
