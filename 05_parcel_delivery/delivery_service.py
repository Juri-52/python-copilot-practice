from courier import Courier
from parcel import Parcel


class DeliveryService:
    def __init__(
        self, parcels: list[Parcel], couriers: list[Courier] | None = None
    ):
        self.parcels = list(parcels)
        self.couriers = list(couriers) if couriers is not None else []

    def get_parcel(self, tracking_number: str) -> Parcel:
        for parcel in self.parcels:
            if parcel.tracking_number == tracking_number:
                return parcel
        raise ValueError("荷物が見つかりません")

    def dispatch_parcel(self, tracking_number: str) -> None:
        self.get_parcel(tracking_number).dispatch()

    def deliver_parcel(self, tracking_number: str) -> None:
        self.get_parcel(tracking_number).deliver()

    def get_courier(self, courier_id: str) -> Courier:
        for courier in self.couriers:
            if courier.courier_id == courier_id:
                return courier
        raise ValueError("配達員が見つかりません")

    def assign_courier(self, tracking_number: str, courier_id: str) -> None:
        parcel = self.get_parcel(tracking_number)
        self.get_courier(courier_id)
        if parcel.status == "配達完了":
            raise ValueError("配達完了の荷物には割り当てできません")
        parcel.courier_id = courier_id

    def get_courier_parcels(self, courier_id: str) -> list[Parcel]:
        self.get_courier(courier_id)
        return [parcel for parcel in self.parcels if parcel.courier_id == courier_id]

    def search_parcels(self, keyword: str) -> list[Parcel]:
        normalized_keyword = keyword.strip().casefold()
        if not normalized_keyword:
            return []

        return [
            parcel
            for parcel in self.parcels
            if normalized_keyword in parcel.tracking_number.casefold()
            or normalized_keyword in parcel.recipient.casefold()
        ]
