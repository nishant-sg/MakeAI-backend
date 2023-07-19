from djoser import email
from djoser import utils
from djoser.conf import settings
from django.contrib.auth.tokens import default_token_generator

from django.core.mail import send_mail
from django.template.loader import render_to_string


class ActivationEmail(email.ActivationEmail):
    template_name = 'mail/activation.html'

    def get_context_data(self):
        # ActivationEmail can be deleted
        context = super().get_context_data()

        user = context.get("user")
        context['user'] = user.name
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.ACTIVATION_URL.format(**context)
        return context

    def send(self, to, *args, **kwargs):

        self.to = to
        self.cc = kwargs.pop('cc', [])
        self.bcc = kwargs.pop('bcc', [])
        self.reply_to = kwargs.pop('reply_to', [])
        # self.from_email = kwargs.pop(
        #     'from_email', settings.DEFAULT_FROM_EMAIL
        # )

        context = self.get_context_data()
        print("email sent ")
        html_mail = render_to_string(self.template_name, context=context)

        send_mail(subject=f"Complete your activation on {context.get('site_name', 'strings')}", 
                        message=f"Please go to the following page to activate account {context.get('protocol')}://{ context.get('domain') }/{context.get('url')}",
                        from_email=None, 
                        recipient_list=[self.to], 
                        html_message=html_mail,
                        fail_silently=True)

        # super().send()