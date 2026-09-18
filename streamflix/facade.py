
from .payments import PaymentProcessor
from .catalog import Video


class StreamingFacade:
    """
    Simplified entry point for the mobile/web client: it never talks to
    payment processors or videos directly, only to this facade.
    """

    def __init__(self, payment_processor: PaymentProcessor) -> None:
        self._payment_processor : PaymentProcessor = payment_processor
        self._subscribed        : bool             = False

    def subscribe(self, monthly_fee: float) -> str:
        receipt: str = self._payment_processor.pay(monthly_fee)
        self._subscribed = True

        return receipt

    def watch(self, video: Video) -> str:
        if not self._subscribed:
            raise PermissionError("subscription required")

        return video.play()
