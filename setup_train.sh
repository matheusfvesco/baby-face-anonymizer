pip install -r requirements.txt --user

# GroundingDINO
git clone https://github.com/IDEA-Research/GroundingDINO.git

cd GroundingDINO && pip install -q -e . && pip install -q roboflow
mkdir ../weights
cd ../weights
wget -nc https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth
cd ..
pip install --upgrade transformers==4.49.0 # ensure transformers doesn't use torch.compile