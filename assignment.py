import io
import os
import xml

from fastapi import FastAPI
from pydantic import BaseModel
from pydantic_xml import BaseXmlModel

from datetime import date
import requests
from starlette.responses import FileResponse


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
BASE_DIR =  os.path.dirname(os.path.abspath(__file__))
Upload_DIR = os.path.join(BASE_DIR, "uploads")

@app.post("/submit")
async def submit(file: UploadFile, response_model=bank_account_holder_deatils_model):
    if file.conetent_type !="application/xml":
        raise HTTPException(400, detail="Invalid file type")
    else:
        xml_data = xml.load(file.file.read())
        new_filename = '{} {}.xls'.format(os.path.splitext(file.filename)[0])

        save_file_path = os.path.join(Upload_DIR, new_filename)
        with open(save_file_path, "w") as f:
            xls.dump(xml_data)
    return FileResponse(path=save_file_path, media_type="application/xls", filename=new_filename)