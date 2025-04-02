from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from mangum import Mangum
from PIL import Image
from io import BytesIO
import numpy as np
import cv2
import io

app = FastAPI()


def anonymize(image, boxes):
    arr = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    for box in boxes:
        x1, y1, x2, y2 = box
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)

        cv2.rectangle(arr, (x1, y1), (x2, y2), (0, 0, 0), -1)

    image_out = Image.fromarray(cv2.cvtColor(arr, cv2.COLOR_BGR2RGB))
    return image_out


@app.get("/")
def root():
    return {
        "name": "Baby Faces Anonymizer",
        "author": "matheusfvesco"
    }


@app.post("/anonymize/")
async def upload_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        image_buffer = BytesIO(contents)
        pil_image = Image.open(image_buffer)

        if pil_image.mode in ("RGBA", "P"):
            pil_image = pil_image.convert("RGB")

        from ultralytics import YOLO

        model = YOLO("runs/detect/train/weights/best.pt")

        results = model([pil_image])

        boxes = results[0].boxes.xyxy.tolist()

        anom_img = anonymize(pil_image, boxes)
        pil_image.close()

        img_buffer = io.BytesIO()
        anom_img.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        anom_img.close()

        return StreamingResponse(
            img_buffer,
            media_type="image/png",
            headers={
                "Content-Disposition": "attachment; filename=generated_image.png"}
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error processing image: {str(e)}"
        )


handler = Mangum(app)
