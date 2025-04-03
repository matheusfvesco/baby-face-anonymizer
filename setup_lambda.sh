pip install -t dependencies -r requirements.txt

zip aws_lambda_artifact.zip -r dependencies api.py runs/detect/train/weights/best.pt