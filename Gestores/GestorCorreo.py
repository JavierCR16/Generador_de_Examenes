from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.multipart import MIMEBase
from email.encoders import encode_base64
import smtplib

def enviarExamen(asunto,cuerpo,listaExamenes,listaCorreos):
    msg = MIMEMultipart()
    msg['Subject'] = asunto
    msg['From'] = "gema.teccr@gmail.com"
    msg['To'] = ', '.join(listaCorreos)

    body = MIMEText(cuerpo)
    msg.attach(body)

    for examen in listaExamenes:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(examen.read())
        encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename=' + examen.filename)

        msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com')
    server.connect('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('gema.teccr@gmail.com','gematec03examenes') #CREDENCIALES CORREO GEMA
    server.sendmail(msg['From'], msg['To'], msg.as_string())
