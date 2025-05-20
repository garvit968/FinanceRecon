from fastapi import APIRouter
import os
from uuid import uuid4

router = APIRouter()
UPLOAD_FOLDER = 'app/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/upload")
async def upload_files(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    saved_files = []
    for f in [file1, file2]:
        extension = os.path.splitext(f.filename)[-1]
        unique_name = f"{uuid4()}{extension}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_name)

        with open(file_path, 'wb') as out_file:
            content = await f.read()
            out_file.write(content)

        saved_files.append({
            "original_filename": f.filename,
            "stored_filename": unique_name,
            "size": len(content),
        })
    return {"message": "Files Uploaded Success", "files": saved_files}
