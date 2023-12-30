from __future__ import print_function
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from dotenv import load_dotenv
import os


async def send_transactional_email(subject, to, body):
    print(to)
    load_dotenv()

    API_KEY = os.getenv("API_KEY")
    SENDER = os.getenv("SENDER")
    REPLY_TO = os.getenv("REPLY_TO")
    NAME = os.getenv("NAME")

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = API_KEY

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    sender = {"name": NAME, "email": SENDER}
    reply_to = {"name": NAME, "email": REPLY_TO}
    html_content = """"""

    if "Email" in subject:
        html_content = f"""
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Email Verification</title>
    </head>

    <body style="font-family: Arial, sans-serif;">

        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ccc; border-radius: 5px;">

            <h2 style="text-align: center; color: #333;">{body['project_name']} - Email Verification</h2>

            <p>Hello {body['email']},</p>

            <p>Thank you for registering with {body['project_name']}. To complete your registration, please click the following link:</p>

            <p><a href="{ body['url']}" style="display: inline-block; padding: 10px 20px; background-color: #4CAF50; color: #fff; text-decoration: none; border-radius: 5px;">Verify Email</a></p>

            <p>If you didn't register on our platform, you can ignore this email.</p>

            <p>Best regards,<br>{body['project_name']} Team</p>

        </div>

    </body>

    </html>
    """

    if "Password" in subject:
        html_content = f"""<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Reset</title>
</head>

<body style="font-family: Arial, sans-serif;">

    <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ccc; border-radius: 5px;">

        <h2 style="text-align: center; color: #333;">Password Reset</h2>

        <p>Hello {body['email']},</p>

        <p>We received a request to reset your password. To set a new password, please click the following link:</p>

        <p><a href="{ body['url']}" style="display: inline-block; padding: 10px 20px; background-color: #4CAF50; color: #fff; text-decoration: none; border-radius: 5px;">Reset Password</a></p>

        <p>If you didn't request a password reset, you can ignore this email.</p>

        <p>Best regards,<br>Your Project Team</p>

    </div>

</body>

</html>
"""

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to, reply_to=reply_to, html_content=html_content, sender=sender, subject=subject
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)


