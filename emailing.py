from email.message import EmailMessage
import smtplib
import filetype

password = "epnpanqngtewxbfl"
username = "lakshmiaravind.atom@gmail.com"
receviver = "lakshmiaravind.atom@gmail.com"


def send_email(img_path):
    email_message = EmailMessage()
    email_message["Subject"] = "New object is being detected "
    email_message.set_content("Hey , we saw a new object in your area ..!")

    with open(img_path, "rb") as file:
        content = file.read()
        content1 = filetype.guess(content)

    email_message.add_attachment(content, maintype="image", subtype=content1.extension)
    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(username, password)
    gmail.sendmail(username, receviver, email_message.as_string())
    gmail.quit()
    print("email sent succesfully")


if __name__ == "__main__":
    send_email(img_path="images/19.png")
