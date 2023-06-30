__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."

from fastapi import FastAPI, Request, UploadFile, File
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import smtplib, ssl
import asyncio
from pydantic import BaseModel
from typing import AnyStr, Optional, NoReturn



class FileOptions(BaseModel):
    """Models updatable field of a profile instance"""
    FileName: AnyStr
    FileDesc: AnyStr = "Upload PDF file"
    FileType: Optional[AnyStr]


class WebFloorPlanApp(object):
    """
        Singleton for Http interface for \GET and \POST. Note this is static and therefore does not
        need a constructor __init__
        @version 0.2
    """
    app = FastAPI()
    app.mount(
        "/static",
        StaticFiles(directory=Path(__file__).parent.parent.absolute() / "./floorplan/web/static"),
        name="static",
    )

    templates = Jinja2Templates(directory="./web")


    @staticmethod
    @app.get("/", response_class=HTMLResponse)
    async def root():
        with open("web/index.html", 'r') as f:
            content = f.read()
        print("loaded index.html")
        return content

    @staticmethod
    @app.post('/upload', response_class=HTMLResponse)
    def upload(request: Request, file: UploadFile = File(...)):
        try:
            import shutil
            from smtpclient import SmtpClient

            print(f'Uploaded file: {file.filename}')
            new_file = f"floorplans/{file.filename}"
            with open(new_file, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            smtp_client = SmtpClient.build_from_conf('test_input/test.csv')
            smtp_client.send_email_with_attachment('pnicolas57@yahoo.com', new_file)
            # asyncio.run(WebFloorPlanApp.send_email_with_attachment(new_file))

            return WebFloorPlanApp.templates.TemplateResponse("response.html", {"request": request}, 200)
        except Exception as e:
            print(f'Error: {str(e)}')
            return WebFloorPlanApp.templates.TemplateResponse("response.html", {"request": request}, 400)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(WebFloorPlanApp.app, host='localhost', port=8000, log_level="debug")
