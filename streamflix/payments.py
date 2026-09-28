
from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    """
    Target interface. StreamFlix only ever talks to this.
    """

    @abstractmethod
    def pay(self, amount: float) -> str:
        """Charge `amount` (in EUR) and return a human-readable receipt."""
        raise NotImplementedError


# --- Third-party SDKs (given, do not modify) --------------------------------
# These are stand-ins for real vendor libraries: their interfaces don't match
# `PaymentProcessor`, and we can't change them.

class StripeAPI:
    """Fake Stripe SDK. Works in integer cents and needs a merchant id."""

    def __init__(self, merchant_id: str):
        self.merchant_id = merchant_id

    def charge_cents(self, cents: int) -> dict:
        if cents <= 0:
            raise ValueError("cents must be positive")
        return {"id": f"ch_{cents}", "status": "succeeded"}


class PayPalClient:
    """Fake PayPal SDK. Works with string amounts and an account email."""

    def __init__(self, account_email: str):
        self.account_email = account_email

    def send_payment(self, amount_str: str, currency: str) -> str:
        if float(amount_str) <= 0:
            raise ValueError("amount must be positive")
        return f"PP-{amount_str}-{currency}"


# --- Adapters (implement these) ---------------------------------------------

class StripeAdapter(PaymentProcessor):
    def __init__(self, stripe: StripeAPI):
      self.stripe = stripe
      pass

    def pay(self, amount: float) -> str:
      if amount < 0:
          raise ValueError("Amount must be positive")
      
      amount_cents = int(amount * 100)
      self.stripe.charge_cents(amount_cents)
      return f'paid {amount:.2f} EUR via stripe ({self.stripe.merchant_id})'


class PayPalAdapter(PaymentProcessor):
    def __init__(self, paypal: PayPalClient):
      self.paypal = paypal

    def pay(self, amount: float) -> str:
      if amount < 0:
          raise ValueError("Amount must be positive")
      
      self.paypal.send_payment(str(amount), 'EUR')
      return f"paid {amount:.2f} EUR via paypal ({self.paypal.account_email})"
