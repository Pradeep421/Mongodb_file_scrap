import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from  dotenv  import load_dotenv
import os
load_dotenv()
sender=os.getenv("SENDER_EMAIL")
receiver=os.getenv("receiver_email")
passkey=os.getenv("password")


def send_report(matched, unmatched):   
    msg=MIMEMultipart()
    msg["From"]=sender
    msg["To"]=receiver
    msg["subject"]="GUID MATCHING DATA"
    # data = ["Value 1", "Value 2", "Value 3"]

    # Start the table
    body = """
    <table border="3 solid" style="border-color:black;">
    <tr style="background-color:blue; color:black;">GUID<th></th><th>Catrgory</th></tr>    """

    # Add rows dynamically
    for val in matched:
        body += f"<tr style='color:green;'><td>{val}</td><td>Matched</td></tr>"
    for val in unmatched:
        body += f"<tr style='color:red;'><td>{val}</td><td>unMatched</td></tr>"

    # Close the table
    body += "</table>"
    msg.attach(MIMEText(body,"html"))

    with smtplib.SMTP("smtp.gmail.com",587) as t:
        t.starttls()  # Encrypt the connection
        t.login(sender, passkey)  # Login using your email and app password
        t.send_message(msg)

def update_report(matched):
    lst=[]
    for i in matched:
        print(i)
    lst.append(matched)
    msg=MIMEMultipart()
    msg["From"]=sender
    msg["To"]=receiver
   
    msg["subject"]="GUID CLEARED DATA"

    # data = ["Value 1", "Value 2", "Value 3"]

    # Start the table
    body1 = """
    <table border="3 solid" style="border-color:black;">
    <tr style="background-color:blue; color:black;">GUID<th></tr>    """

    # Add rows dynamically
    for val in lst:
        body1 += f"<tr style='color:green;'><td>{val}</td></tr>"
   

    # Close the table
    body1 += "</table>"
    msg.attach(MIMEText(body1,"html"))

    with smtplib.SMTP("smtp.gmail.com",587) as t:
        t.starttls()  # Encrypt the connection
        t.login(sender, passkey)  # Login using your email and app password
        t.send_message(msg)
