class EmailSender:
    @staticmethod
    def send_email(receiver_email, subject, body):
        print(f"Sending Email to {receiver_email}")
        print(f"Subject: {subject}")
        print(f"Message: {body}")
