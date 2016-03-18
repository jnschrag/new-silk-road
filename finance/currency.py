from iso4217 import Currency


CURRENCY_CHOICES = ((c.code, c.currency_name) for c in Currency)

DEFAULT_CURRENCY_CHOICE = Currency.usd.code
