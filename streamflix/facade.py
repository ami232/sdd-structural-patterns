
from .payments import PaymentProcessor
from .catalog import Video


class StreamingFacade:
    def __init__(self, payment_processor: PaymentProcessor):
        self._payment_processor = payment_processor
        self._subscribed = False

    def subscribe(self, monthly_fee: float) -> str:
        receipt = self._payment_processor.pay(monthly_fee)
        self._subscribed = True
        return receipt

    def watch(self, video: Video) -> str:
        if not self._subscribed:
            raise PermissionError("subscription required")
        return video.play()