__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2023. All rights reserved."

from fastapi import FastAPI, Request, UploadFile, File
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import AnyStr, Optional, NoReturn


class FileOptions(BaseModel):
    """Models updatable field of a profile instance"""
    FileName: AnyStr
    FileDesc: AnyStr = "Upload PDF file"
    FileType: Optional[AnyStr]


"""
    Implement the web service to handle HTTP requests
    http://dns_name:8000/  for landing page defined as index.html
    http://dns_name:8000/upload for the upload page defined as response.html
"""


class WebFloorPlanApp(object):
    """
        Singleton for Http interface for GET and POST.
        This is static and therefore does not need a constructor __init__
        @version 0.1
    """
    app = FastAPI()
    app.mount(
        "/static",
        StaticFiles(directory=Path(__file__).parent.parent.absolute() / "./floorplan/web/static"),
        name="static",
    )
    """ Instantiate JinJa2 template for Request and Response a static variable"""
    templates = Jinja2Templates(directory="./web")

    @staticmethod
    @app.get("/", response_class=HTMLResponse)
    async def root():
        """
        Load the index/landing page code from a file
        :return: HTML content for the landing page
        """
        with open("web/index.html", 'r') as f:
            html_content = f.read()
        print("loaded index.html")
        return html_content

    @staticmethod
    @app.post('/upload', response_class=HTMLResponse)
    def upload(request: Request, file: UploadFile = File(...)):
        """
        Handle the request to upload a file
        :param request: Body of the request
        :param file: File object to upload
        :return: Response template
        """
        try:
            import shutil
            from smtpclient import SmtpClient

            print(f'Uploaded file: {file.filename}')
            new_file = f"floorplans/{file.filename}"
            with open(new_file, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            smtp_client = SmtpClient.build_from_conf('../test_input/test.csv')
            smtp_client.send_email_with_attachment('pnicolas57@yahoo.com', new_file)

            return WebFloorPlanApp.templates.TemplateResponse("response.html", {"request": request}, 200)
        except Exception as e:
            print(f'Error: {str(e)}')
            return WebFloorPlanApp.templates.TemplateResponse("response.html", {"request": request}, 400)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(WebFloorPlanApp.app, host='localhost', port=8000, log_level="debug")
