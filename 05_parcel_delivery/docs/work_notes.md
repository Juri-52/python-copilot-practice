# 変更内容
delivery_service.py/DeliveryService.search_parcels()
```
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
```
report.py/build_search_parcels()
```
def build_search_report(service: DeliveryService, keyword: str) -> str:
    parcels = service.search_parcels(keyword)
    if not parcels:
        return "検索結果:\n該当する荷物はありません"

    lines = ["検索結果:"]
    for parcel in parcels:
        lines.append(f"{parcel.tracking_number}: {parcel.recipient} [{parcel.status}]")
    return "\n".join(lines)
```
main.py
```
def main() -> None:
    service = DeliveryService(create_parcels())
    service.dispatch_parcel("P001")
    print(build_report(service))
    service.deliver_parcel("P001")
    print("\n配達後:")
    print(build_report(service))
    print("\n" + build_search_report(service, "alice"))
```
tests/test_delivery_service.py

tests/test_report.py

parcel.py
```
class Parcel:
    def __init__(self, tracking_number: str, recipient: str):
        self.tracking_number = tracking_number
        self.recipient = recipient
        self.status = "受付済み"
        self.history = ["受付済み"]

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
```
report.py
```
def build_history_report(service: DeliveryService, tracking_number: str) -> str:
    parcel = service.get_parcel(tracking_number)
    return f"履歴: {parcel.tracking_number}\n{' → '.join(parcel.history)}"
```

test_parcel.py

test_delivery_service.py

test_report.py

courier.py(新規作成)
```
class Courier:
    def __init__(self, courier_id: str, name: str):
        self.courier_id = courier_id
        self.name = name
```
parcel.py
```
class Parcel:
    def __init__(self, tracking_number: str, recipient: str):
        self.tracking_number = tracking_number
        self.recipient = recipient
        self.status = "受付済み"
        self.history = ["受付済み"]
        self.courier_id: str | None = None
```
data.py
```
def create_couriers() -> list[Courier]:
    return [
        Courier("C01", "田中"),
        Courier("C02", "佐藤"),
    ]
```
delivery_service.py
```
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
```
main.py
```
def main() -> None:
    service = DeliveryService(create_parcels(), create_couriers())
    service.assign_courier("P002", "C01")
    service.assign_courier("P003", "C01")
    service.dispatch_parcel("P001")
    print(build_report(service))
    service.deliver_parcel("P001")
    print("\n配達後:")
    print(build_report(service))
    print("\n" + build_search_report(service, "alice"))
    print("\n" + build_history_report(service, "P001"), end="")
    assigned_parcels = service.get_courier_parcels("C01")
    print(
        "\n担当荷物: C01\n"
        + "\n".join(parcel.tracking_number for parcel in assigned_parcels),
        end="",
    )
```

test_delivery_service.py

report.py
```
def build_delivery_summary(service: DeliveryService) -> str:
    lines = ["配送サマリー:"]
    for courier in service.couriers:
        incomplete_count = sum(
            parcel.status != "配達完了"
            for parcel in service.get_courier_parcels(courier.courier_id)
        )
        lines.append(f"{courier.courier_id}: {courier.name} — 未完了 {incomplete_count}件")

    unassigned_count = sum(
        parcel.courier_id is None and parcel.status != "配達完了"
        for parcel in service.parcels
    )
    lines.append(f"未割り当て — 未完了 {unassigned_count}件")
    return "\n".join(lines)
```
main.py
```
def main() -> None:
    service = DeliveryService(create_parcels(), create_couriers())
    service.assign_courier("P002", "C01")
    service.assign_courier("P003", "C01")
    service.dispatch_parcel("P001")
    print(build_report(service))
    service.deliver_parcel("P001")
    print("\n配達後:")
    print(build_report(service))
    print("\n" + build_search_report(service, "alice"))
    print("\n" + build_history_report(service, "P001"), end="")
    assigned_parcels = service.get_courier_parcels("C01")
    print(
        "\n担当荷物: C01\n"
        + "\n".join(parcel.tracking_number for parcel in assigned_parcels),
        end="",
    )
    print("\n" + build_delivery_summary(service), end="")
```

test_report.py