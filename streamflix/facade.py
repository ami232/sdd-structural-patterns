
from .payments import PaymentProcessor
from .catalog import Video


class StreamingFacade:
    """
    Simplified entry point for the mobile/web client: it never talks to
    payment processors or videos directly, only to this facade.
    """

    def __init__(self, payment_processor: PaymentProcessor):
      """Initialize the facade with a `PaymentProcessor` and start
      unsubscribed.
      """
      self._payment_processor = payment_processor
      self._subscribed = False

    def subscribe(self, monthly_fee: float) -> str:
      """Charge `monthly_fee` through the configured payment processor,
      mark the account as subscribed, and return the processor's receipt
      string.
      """
      receipt = self._payment_processor.pay(monthly_fee)
      self._subscribed = True
      return receipt

    def watch(self, video: Video) -> str:
      """If the account is subscribed, delegate to `video.play()` and
      return its result. Otherwise raise `PermissionError`.
      """
      if not self._subscribed:
          raise PermissionError("subscription required")
      return video.play()
