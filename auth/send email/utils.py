from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import threading

# ✅ Custom thread to send email asynchronously
class SendEmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        # 🚀 Send the email in a separate thread
        self.email.send()

# ✅ Function to prepare and send activation email
def send_activation_email(recipient_email, activation_url):
    subject = "Activate your Job Portal Account"
    from_email = 'No_reply@demomailtrap.co'  # 🔧 Replace with your actual sender email
    to_email = [recipient_email]

    # 📄 Load the HTML email template and pass the activation URL to context
    html_content = render_to_string('account/activation_email.html', {
        'activation_url': activation_url,
    })

    # 🧾 Fallback plain text version (for email clients that don't support HTML)
    text_content = strip_tags(html_content)

    # 📬 Create the multi-alternative email (HTML + plain text)
    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, 'text/html')

    # 🚀 Send email asynchronously to prevent blocking the main thread
    SendEmailThread(email).start()
