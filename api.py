from ultralytics import YOLO
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from mangum import Mangum
from PIL import Image
from io import BytesIO
import numpy as np
import cv2
import io
import av
import os

app = FastAPI()

model = YOLO("runs/detect/train/weights/best.pt")


def anonymize(image, boxes):
    arr = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    for box in boxes:
        x1, y1, x2, y2 = box
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)

        # Extract the region of interest (ROI)
        roi = arr[y1:y2, x1:x2]

        # Apply Gaussian blur to the ROI
        # Shrink drastically
        small = cv2.resize(roi, (10, 10), interpolation=cv2.INTER_LINEAR)
        blurred_roi = cv2.resize(
            small, (x2 - x1, y2 - y1), interpolation=cv2.INTER_NEAREST)  # Blow up
        arr[y1:y2, x1:x2] = blurred_roi

    image_out = Image.fromarray(cv2.cvtColor(arr, cv2.COLOR_BGR2RGB))
    return image_out


def anonymize_av(input_path, output_path):

    input_ = av.open(input_path)
    output = av.open(output_path, "w")

    # Make an output stream using the input as a template. This copies the stream
    # setup from one to the other.
    in_stream = input_.streams.video[0]
    out_stream = output.add_stream_from_template(in_stream)

    for frame in input_.decode(in_stream):

        img = frame.to_image()

        results = model([img])

        boxes = results[0].boxes.xyxy.tolist()

        out_img = anonymize(img, boxes)

        out_frame = av.VideoFrame.from_image(out_img)
        for packet in out_stream.encode(out_frame):
            output.mux(packet)

    input_.close()
    output.close()


@app.get("/")
def root():
    return {
        "name": "Baby Faces Anonymizer",
        "author": "matheusfvesco"
    }


@app.post("/anonymize/image")
async def anonymize_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        image_buffer = BytesIO(contents)
        pil_image = Image.open(image_buffer)

        if pil_image.mode in ("RGBA", "P"):
            pil_image = pil_image.convert("RGB")

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


@app.post("/anonymize/video/")
def anonymize_video(file: UploadFile = File(...)):
    try:
        original_filename = file.filename
        if '.' in original_filename:
            ext = original_filename.split('.')[-1]
        else:
            ext = 'mp4'

        input_filename = f"video.{ext}"
        with open(input_filename, 'wb') as buffer:
            # Read in 1MB chunks (synchronous read)
            while content := file.file.read(1024 * 1024):
                buffer.write(content)

        output_filename = input_filename.replace("video", "result")
        anonymize_av(input_filename, output_filename)

        with open(output_filename, 'rb') as result_file:
            video_bytes = result_file.read()
            video_buffer = io.BytesIO(video_bytes)

        os.remove(input_filename)
        os.remove(output_filename)

        return StreamingResponse(
            video_buffer,
            media_type="video/mp4",
            headers={
                "Content-Disposition": "attachment; filename=anonymized_video.mp4"}
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing video: {str(e)}"
        )


handler = Mangum(app)
