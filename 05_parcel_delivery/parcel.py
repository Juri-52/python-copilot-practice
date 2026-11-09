class Parcel:
    def __init__(self, tracking_number: str, recipient: str):
        self.tracking_number = tracking_number
        self.recipient = recipient
        self.status = "受付済み"
        self.history = ["受付済み"]
        self.courier_id: str | None = None

    def dispatch(self) -> None:
        if self.status != "受付済み":
            raise ValueError("発送できない状態です")
        self.status = "配送中"
        self.history.append("配送中")

    def deliver(self) -> None:
        if self.status != "配送中":
            raise ValueError("配達できない状態です")
        self.status = "配達完了"
        self.history.append("配達完了")
