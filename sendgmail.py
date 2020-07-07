import email, smtplib, ssl, datetime, os, glob

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#proxy = "http://192.168.6.80:8128"

#os.environ["http_proxy"] = proxy
#os.environ["HTTP_PROXY"] = proxy
#os.environ["https_proxy"] = proxy
#os.environ["HTTPS_PROXY"] = proxy

yesterday = datetime.datetime.now() - datetime.timedelta(days = 1)
today = datetime.datetime.now()
subject = "Report Notifying and Validation "+today.strftime("%Y-%m-%d")
body = "Dear All, \n \nBerikut terlampir report Notify and Validation, \n \nRegards, \nAutomation"
sender_email = "example@gmail.com" #fill with your email
receiver_email = ['example@example.com', 'example2@example.com', 'example3@example.com'] #fill with receiver email
password = "yourpassgmail" #fill with your password gmail

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = ", ".join(receiver_email)
message["Subject"] = subject
# message["Bcc"] = receiver_email  # Recommended for mass emails

# Add body to email
message.attach(MIMEText(body, "plain"))

path = "/$HOME/data/"  #path file want to attach to email
csvfile = glob.glob(os.path.join(path, "*"+today.strftime("%d%m%Y")+".tar.gz")) #if you want to send file with date auto generate with ext .tar.gz

for file in csvfile:
      part = MIMEBase("application", "octet-stream")
      part.set_payload( open(file, "rb").read() )

#Encode file in ASCII characters to send by email
      encoders.encode_base64(part)

# Add header as key/value pair to attachment part
      part.add_header("Content-Disposition", "attachment; filename= %s" % os.path.basename(file))

# Add attachment to message and convert message to string
      message.attach(part)
text = message.as_string()

# Log in to server using secure context and send email
context = ssl.create_default_context()
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls(context=context)
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)
    server.quit
