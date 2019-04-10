from django.conf import settings
from django.core.mail import send_mail
from manager.models import Siteinfo


def send_active_email(token, username, email):
    """发送激活邮件"""
    subject = '欢迎您注册{}'.format(Siteinfo.objects.first().title)  # 标题
    message = '12'
    sender = settings.FROM_EMAIL  # 发件人
    receiver = [email]  # 收件人列表
    html_message = '<a href="http://127.0.0.1:8000/users/active/%s/">http://127.0.0.1:8000/users/active/</a>' % token
    send_mail(subject, message, sender, receiver, html_message=html_message)


def send_forget_email(token, email):
    pass


