from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from shop.views import Customer


class AppTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, Customer , timestamp):
        return (text_type(Customer.is_active) + text_type(Customer.pk) + text_type(timestamp))


account_activation_token = AppTokenGenerator()