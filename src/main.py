__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2023. All rights reserved."

from fastapi import FastAPI, Request, UploadFile, File, Form
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import AnyStr, Optional
from src.configutil import configuration_parameters
from src.gmailclient import GmailClient


class FileOptions(BaseModel):
    """Models updatable field of a profile instance"""
    FileName: AnyStr
    FileDesc: AnyStr = "Upload PDF file"
    FileType: Optional[AnyStr]




"""
    Implement the web service to handle HTTP requests
    http://dns_name:{port}/  for landing page defined as index.html
    http://dns_name:{port}/upload for the upload page defined as response.html
"""

app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "./src/web/static"),
    name="static",
)
""" Instantiate JinJa2 template for Request and Response a static variable"""
templates = Jinja2Templates(directory="./web")


@app.get("/", response_class=HTMLResponse)
async def root():
    import os

    print(f'Current directory: {os.getcwd()}')
    web_path = configuration_parameters['web_path']
    with open(f"{web_path}/index.html", 'r') as f:
        html_content = f.read()
    print("loaded index.html")
    return html_content


@app.post('/upload', response_class=HTMLResponse)
async def upload(
        request: Request,
        username: str = Form(...),
        email: str = Form(...),
        file: UploadFile = File(...)):
    """
        @param request  Request meta data
        @param username User name file defined in the form (INPUT text)
        @param email Email addressed defined in the HTML form (Input email)
        @param file Handle to the uploaded file.
    """
    try:
        import shutil
        from smtpclient import SmtpClient

        print(f'Uploaded file: {file.filename} User name {username} Email: {email}')
        floor_plans_path = configuration_parameters['floor_plans_path']
        new_file = f"{floor_plans_path}/{file.filename}"
        with open(new_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Send the notification message and attachment to SMTP server
        gmail_client = GmailClient()
        email_sender = configuration_parameters['test_sender'] if configuration_parameters['is_test'] \
            else configuration_parameters['email_sender']
        gmail_client.send(email_sender, username, email, new_file)

        return templates.TemplateResponse("response.html", {"request": request}, 200)
    except Exception as e:
        print(f'ERROR: {str(e)}')
        return templates.TemplateResponse("response.html", {"request": request}, 400)


if __name__ == '__main__':
    import uvicorn
    port_num = int(configuration_parameters['port'])
    uvicorn.run(app, host='localhost', port=port_num, log_level="debug")
