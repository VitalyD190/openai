import json

import sagemaker
import boto3
from sagemaker.huggingface import HuggingFaceModel

try:
    iam = boto3.client('iam')
    role = iam.get_role(RoleName='vitaly-role-HF-modles-deploy')['Role']['Arn']
    print("role is: " + role)
except ValueError:
    iam = boto3.client('iam')
    role = iam.get_role(RoleName='sagemaker_execution_role')['Role']['Arn']

# Hub Model configuration. https://huggingface.co/models
hub = {
    'HF_MODEL_ID': 'nlptown/bert-base-multilingual-uncased-sentiment',
    'HF_TASK': 'text-classification'
}

# create Hugging Face Model Class
huggingface_model = HuggingFaceModel(
    transformers_version='4.37.0',
    pytorch_version='2.1.0',
    py_version='py310',
    env=hub,
    role=role,
)

# Specify the endpoint name
endpoint_name = 'huggingface-pytorch-inference-2024-05-09-10-47-36-380'

# Get the predictor class
predictor_cls = huggingface_model.predictor_cls

# Instantiate the predictor with the existing endpoint name
predictor = predictor_cls(endpoint_name)

# deploy model to SageMaker Inference
# predictor = huggingface_model.deploy(
#     initial_instance_count=1,  # number of instances
#     instance_type='ml.g4dn.xlarge'  # ec2 instance type
# )

# with open('test.json', 'r') as file:
#     data = json.load(file)

response = predictor.predict({
    "inputs": "happy",
})

print(response)

# 1: Very negative
# 2: Negative
# 3: Neutral
# 4: Positive
# 5: Very positive
