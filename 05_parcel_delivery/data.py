from parcel import Parcel
from courier import Courier


def create_parcels() -> list[Parcel]:
    return [
        Parcel("P001", "田中"),
        Parcel("P002", "Alice"),
        Parcel("P003", "ALICE Suzuki"),
        Parcel("P004", "佐藤"),
        Parcel("P005", "Bob"),
    ]


def create_couriers() -> list[Courier]:
    return [
        Courier("C01", "田中"),
        Courier("C02", "佐藤"),
    ]
