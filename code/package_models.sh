#!/usr/bin/env bash
set -e

# 2.1 Convert cloud_model.h5 → TF SavedModel dir
python3 - << 'PYCODE'
import tensorflow as tf
model = tf.keras.models.load_model('cloud_model.h5')
# export as SavedModel under export/1/
tf.saved_model.save(model, 'export/1')
PYCODE

# 2.2 Package the SavedModel directory (export/1) into tar.gz
tar -czvf cloud_model.tar.gz -C export/1 .

# 2.3 Upload to your bucket
BUCKET=research-bucket-bu
aws s3 cp cloud_model.tar.gz s3://$BUCKET/cloud_model.tar.gz \
    --acl bucket-owner-full-control

echo "Uploaded cloud_model.tar.gz to s3://$BUCKET/"



Make executable & run:
//chmod +x package_models.sh
//./package_models.sh
