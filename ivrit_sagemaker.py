import sagemaker
import boto3
from sagemaker.huggingface import HuggingFaceModel
from sagemaker.serializers import DataSerializer

try:
    iam = boto3.client('iam')
    role = iam.get_role(RoleName='vitaly-role-HF-modles-deploy')['Role']['Arn']
    print("role is: " + role)
except ValueError:
    iam = boto3.client('iam')
    role = iam.get_role(RoleName='sagemaker_execution_role')['Role']['Arn']

hub = {
    'HF_MODEL_ID': 'ivrit-ai/whisper-large-v2-tuned',
    'HF_TASK': 'automatic-speech-recognition'
}

# create Hugging Face Model Class
huggingface_model = HuggingFaceModel(
    transformers_version='4.37.0',
    pytorch_version='2.1.0',
    py_version='py310',
    env=hub,
    role=role,
)

# deploy model to SageMaker Inference
# predictor = huggingface_model.deploy(
#     initial_instance_count=1,
#     instance_type='ml.g4dn.xlarge'  # ec2 instance type
# )

# predictor.serializer = DataSerializer(content_type='audio/x-audio')

# Specify the endpoint name
endpoint_name = 'huggingface-pytorch-inference-2024-05-28-07-15-20-859'

# Initialize a HuggingFacePredictor object with the endpoint name
predictor = sagemaker.predictor.Predictor(
    endpoint_name=endpoint_name,
    serializer=sagemaker.serializers.DataSerializer(content_type='audio/x-audio')
)

with open("reuven_oved.mp3", "rb") as f:
    data = f.read()


result = predictor.predict(data)
result_decoded = result.decode('utf-8')
print(result_decoded)

# predictor.delete_model()
# predictor.delete_endpoint()
