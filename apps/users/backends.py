from django.conf import settings
from django.core.mail import send_mail
from manager.models import Siteinfo
from django.template.loader import render_to_string
from urllib.parse import urljoin
from django.urls import reverse


def send_active_email(token, username, email):
    """
    发送激活邮件
    """
    info = Siteinfo.objects.first()
    _ = reverse('users:active', args=(token, ))
    active_url = urljoin(info.address, _)
    subject = '欢迎来到{}'.format(info.name)
    message = '{},感谢您加入我们!<br><br>您可以通过<a href="{}">这个激活链接</a>来激活您的账号，<br><br>激活后您就可以和社区其他人分享您的意见和知识'.format(
        username, active_url
    )
    sender = settings.FROM_EMAIL  # 发件人
    receiver = [email]  # 收件人列表
    html_message = render_to_string(template_name='email/base.html', context={'owska_settings': info,
                                                                              'subject': subject,
                                                                              'content': message
                                                                              })
    send_mail(subject, message, sender, receiver, html_message=html_message)


class OwskaEmail:
    def __init__(self, token, username, email):
        self.token = token
        self.username = username
        self.email = email

    def send_active_email(self):
        """
        发送激活邮件
        """
        info = Siteinfo.objects.first()
        _ = reverse('users:active', args=(self.token,))
        active_url = urljoin(info.address, _)
        subject = '欢迎来到{}'.format(info.name)
        message = '{},感谢您加入我们!<br><br>您可以通过<a href="{}">这个激活链接</a>来激活您的账号，<br><br>激活后您就可以和社区其他人分享您的意见和知识'.format(
            self.username, active_url
        )
        sender = settings.FROM_EMAIL
        receiver = [self.email]
        html_message = render_to_string(template_name='email/base.html', context={'owska_settings': info,
                                                                                  'subject': subject,
                                                                                  'content': message
                                                                                  })
        send_mail(subject, message, sender, receiver, html_message=html_message)

    def send_forget_email(self):
        """
        找回密码
        """
        info = Siteinfo.objects.first()
        _ = reverse('users:reset', args=(self.token,))
        active_url = urljoin(info.address, _)
        subject = '{}重置密码'.format(info.name)
        message = '{},<br><br>您可以通过<a href="{}">这个链接</a>来重置您的密码，<br><br>重置后您就可以和社区其他人分享您的意见和知识'.format(
            self.username, active_url
        )
        sender = settings.FROM_EMAIL
        receiver = [self.email]
        html_message = render_to_string(template_name='email/base.html', context={'owska_settings': info,
                                                                                  'subject': subject,
                                                                                  'content': message
                                                                                  })
        send_mail(subject, message, sender, receiver, html_message=html_message)


