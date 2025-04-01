import torch
from pathlib import Path
import argparse
import os
from groundingdino.util.inference import load_model, load_image, predict
from tqdm import tqdm

CLASSES = ["eye", "mouth"]
CLASS_IDS = {class_name:idx for idx, class_name in enumerate(CLASSES)}

WEIGHTS_PATH = "weights/groundingdino_swint_ogc.pth"
CONFIG_PATH = "GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py"

model = load_model(CONFIG_PATH, WEIGHTS_PATH)

def save_yolo_annotation(image_path: str, save_dir: str, boxes: torch.Tensor, class_names: list[str]):
    image_path = Path(image_path)
    save_dir = Path(save_dir)
    txt_path = save_dir / f"{image_path.stem}.txt"
    
    lines = []
    for box, class_name in zip(boxes, class_names):
        cx, cy, w, h = box.tolist()  # Already normalized
        lines.append(f"{CLASS_IDS[class_name]} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}")
    
    with open(txt_path, 'w') as f:
        f.write('\n'.join(lines))

def infer(image_path):

    image_path = Path(image_path)

    image_source, image = load_image(image_path)

    TEXT_PROMPT = "mouth, eye"
    BOX_TRESHOLD = 0.30
    TEXT_TRESHOLD = 0.25

    boxes, logits, phrases = predict(
        model=model,
        image=image,
        caption=TEXT_PROMPT,
        box_threshold=BOX_TRESHOLD,
        text_threshold=TEXT_TRESHOLD
    )
    return boxes, logits, phrases

def main(image_root, save_root):
    image_root = Path(image_root)
    save_root = Path(save_root)

    save_root.mkdir(parents=True, exist_ok=True)

    pbar = tqdm(list(image_root.iterdir()))
    for image_path in pbar:
        pbar.set_description(image_path.name)
        boxes, _, phrases = infer(image_path)
        if len(phrases) < 3:
            #os.remove(image_path)
            continue
        save_yolo_annotation(image_path, save_root, boxes, phrases)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("image_root")
    parser.add_argument("save_root")
    args = parser.parse_args()

    image_root = Path(args.image_root)
    save_root = Path(args.save_root)
    main(image_root, save_root)