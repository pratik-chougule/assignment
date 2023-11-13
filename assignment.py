import io
import os
import shutil
import xml

from fastapi import FastAPI
from pydantic import BaseModel
from pydantic_xml import BaseXmlModel

from datetime import date
import requests
from starlette.responses import FileResponse, StreamingResponse


class bank_account_holder_deatils_model(BaseModel):
    transaction_date: date
    transaction_type: str
    vch_no: int
    reference_no: int
    reference_type: str
    reference_date: date
    debtor: str
    reference_amount: int
    amount: int
    particulars: str
    veh_type: str
    amount_ver: str


from fastapi import FastAPI, Response, Request, HTTPException, UploadFile

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
Upload_DIR = os.path.join(BASE_DIR, "uploads")
import pandas as pd
from io import BytesIO
@app.post("/submit")
async def submit(file: UploadFile):
    content_type = file.content_type
    upload_dir = os.path.join(os.getcwd(), "uploads")

    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    dest = os.path.join(upload_dir, file.filename)
    if content_type != "text/xml":
        raise HTTPException(status_code=400, detail="invalid file type")
    df = pd.DataFrame(file.file)
    # with open(dest, "wb") as buffer:
    #     shutil.copyfileobj(file.file, buffer)

    buffer = BytesIO()
    # return FileResponse(path=dest, filename=file.filename)
    with pd.ExcelWriter(buffer) as writer:
        df.to_excel(writer, index=False)
    return StreamingResponse(
        BytesIO(buffer.getvalue()),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={"Content-Disposition": f"attachment; filename=input.xls"}
    )