import smtplib
from email.message import EmailMessage
import imghdr
import datetime as dt
import pandas_datareader as pdr
import time
import yfinance as yf
from graph import Graph

email_adresas = "snp500updatestest@gmail.com"
email_slaptazodis = "igzdlxkoftmrzcdg"

msg = EmailMessage()
yf.pdr_override()
pradzia = dt.datetime(2022, 2, 21)
dabar = dt.datetime.now()

success = False
while success != True:
    akcija = input("Įrašykite norimą akciją : ")
    success = Graph.drawGraph(akcija)


kaina = float(input("Įrašykite norimą akcijos kainą : "))

laikas = int(input("Įveskite norimą kainos tikrinimo intervalą (sekundėmis) : "))

print("Pranešti, kai dienos kaina bus : ")
print("1. Didesnė")
print("2. Mazesnė")
pasirinkimas = int(input("Įrašykite pasirinkimą : "))

graph_path = r"C:\Users\Anars\PycharmProjects\baigiamasis\pythonProject2\pythonProject\Images\graph1.png"

with open(graph_path, "rb") as f:
    file_data = f.read()
    file_type = imghdr.what(f.name)
    file_name = f.name

msg["Subject"] = f"Pranešimas apie {akcija} kainą"
msg["From"] = email_adresas
msg["To"] = "Arniakas@gmail.com"

pranesta = False

while 1:

    df = pdr.get_data_yahoo(akcija, pradzia, dabar)
    dienosKaina = df["Adj Close"][-1]

    match(pasirinkimas):
        case 1:
            salyga = dienosKaina >= kaina
        case 2:
            salyga = dienosKaina <= kaina
        case _:
            print("Netinkamas pasirinkimas")


    if salyga and pranesta == False:
        pranesta = True

        tekstas = akcija + " Pasiekė Jūsų pasirinktą kainos rodiklį : " + str(kaina) + \
                  "\nDabartinė kaina: " + str(dienosKaina)

        msg.set_content(tekstas)
        msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)

        text_part, attachment_part = msg.iter_parts()
        text_part.add_alternative("""\
        <!DOCTYPE html>
        <html>
            <body>
                <p>Sveiki,<br>
                <p>Norime Jums pranešti, kad  """+ str(tekstas) + """
                    </p>
                    <img src="cid:{image_cid}">
                    </p>
            </body>
        </html>
        """, subtype='html')

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email_adresas, email_slaptazodis)
            smtp.send_message(msg)

            print("completed")
    else:
        print("Naujų pranešimų nėra")

    time.sleep(laikas)

