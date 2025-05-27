from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
import os
from uuid import uuid4
import pandas as pd
from app.core.reconciler import reconcile_files

router = FastAPI()
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

@router.post('/reconcile')
async def reconcile_endpoint(file1: str = Query(...), file2: str = Query(...),col_product: str = Query(...),col_amount: str = Query(...),col_transaction_id: Optional[str] = Query(None)):
    path1 = os.path.join(UPLOAD_FOLDER, file1)
    path2 = os.path.join(UPLOAD_FOLDER, file2)

    # Check if files exist
    if not os.path.exists(path1):
        raise HTTPException(status_code=404, detail=f"File {file1} not found")
    if not os.path.exists(path2):
        raise HTTPException(status_code=404, detail=f"File {file2} not found")
    
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    result = reconcile_files(df1,df2,col_product = col_product, col_amount = col_amount, col_transaction_id = col_transaction_id)

    return JSONResponse(content=result)
