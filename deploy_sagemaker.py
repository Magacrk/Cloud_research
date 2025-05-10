#bash command
#python3 deploy_sagemaker.py


# deploy_sagemaker.py
import time
import sagemaker
from sagemaker.tensorflow import TensorFlowModel
from sagemaker import image_uris

REGION        = 'us-east-1'
BUCKET        = 'research-bucket-bu'
S3_MODEL_PATH = f's3://{BUCKET}/cloud_model.tar.gz'
ROLE_ARN      = 'arn:aws:iam::423195867952:role/SageMakerExecutionRole'
INSTANCE_TYPE = 'ml.m5.large'   # or ml.c5.large, ml.t2.medium, etc.

# pick correct TF inference image
image_uri = image_uris.retrieve(
    framework='tensorflow',
    region=REGION,
    version='2.9',
    image_scope='inference',
    instance_type=INSTANCE_TYPE
)

sm = sagemaker.Session()
model = TensorFlowModel(
    model_data=S3_MODEL_PATH,
    role=ROLE_ARN,
    framework_version='2.9',
    image_uri=image_uri,
    sagemaker_session=sm
)

endpoint_name = f"dnn-endpoint-{int(time.time())}"
print("Deploying to:", endpoint_name)
predictor = model.deploy(
    initial_instance_count=1,
    instance_type=INSTANCE_TYPE,
    endpoint_name=endpoint_name
)
print("✅ Endpoint in service:", predictor.endpoint_name)
