import json
import boto3
from sagemaker.huggingface import HuggingFaceModel, get_huggingface_llm_image_uri

try:
    iam = boto3.client('iam')
    role = iam.get_role(RoleName='vitaly-role-HF-modles-deploy')['Role']['Arn']
    print("role is: " + role)
except ValueError:
    iam = boto3.client('iam')
    role = iam.get_role(RoleName='sagemaker_execution_role')['Role']['Arn']

# Hub Model configuration. https://huggingface.co/models
hub = {
    'HF_MODEL_ID': 'codellama/CodeLlama-7b-hf',
    'SM_NUM_GPUS': json.dumps(8)
}

# create Hugging Face Model Class
huggingface_model = HuggingFaceModel(
    image_uri=get_huggingface_llm_image_uri("huggingface", version="1.4.2"),
    env=hub,
    role=role,
)

# deploy model to SageMaker Inference
predictor = huggingface_model.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.12xlarge",
    container_startup_health_check_timeout=1500,
)

# send request
predictor.predict({
    "inputs": "My name is Clara and I am",
})
