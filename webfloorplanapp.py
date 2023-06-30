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

    @staticmethod
    async def send_email_with_attachment(filename: AnyStr) -> bool:
        from email import encoders
        from email.mime.base import MIMEBase
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        try:
            from datetime import date

            context = ssl.create_default_context()
            smtp_server = "smtp.mail.yahoo.com"
            sender = "pnicolas57@yahoo.com"
            receiver = "pnicolas57@yahoo.com"
            password = "icytndijfrpshrwe"
            today_date = date.today()
            subject = f"""Subject: Floor plan {filename} uploaded!"""
            content = f"""A new floor plan has been uploaded as {filename} into directory floorplan/files\n\n"""

            message = MIMEMultipart()
            message["From"] = sender
            message["To"] = receiver
            message["Subject"] = subject
            message["Date"] = str(today_date)
            message.attach(MIMEText(content, "plain"))

            with open(filename, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={filename}",
            )

            # Add attachment to message and convert message to string
            message.attach(part)
            text = message.as_string()
            WebFloorPlanApp.__fire_email(smtp_server, context, password, sender, receiver, text)
            await asyncio.sleep(1)
            return True
        except Exception as e:
            print(str(e))
            return False

    @staticmethod
    def __fire_email(
            smtp_server: AnyStr,
            context,
            password: AnyStr,
            sender: AnyStr,
            receiver: AnyStr,
            text: AnyStr) -> NoReturn:
        try:
            with smtplib.SMTP(smtp_server, 587) as server:
                server.starttls(context=context)
                server.login('pnicolas57', password)
                server.sendmail(sender, receiver, text)
                server.quit()
        except Exception as e:
            print(str(e))
            raise e


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(WebFloorPlanApp.app, host='localhost', port=8000, log_level="debug")
