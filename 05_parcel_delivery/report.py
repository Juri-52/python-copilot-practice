from delivery_service import DeliveryService


def build_report(service: DeliveryService) -> str:
    lines = ["荷物一覧:"]
    for parcel in service.parcels:
        lines.append(f"{parcel.tracking_number}: {parcel.recipient} [{parcel.status}]")
    return "\n".join(lines)


def build_search_report(service: DeliveryService, keyword: str) -> str:
    parcels = service.search_parcels(keyword)
    if not parcels:
        return "検索結果:\n該当する荷物はありません"

    lines = ["検索結果:"]
    for parcel in parcels:
        lines.append(f"{parcel.tracking_number}: {parcel.recipient} [{parcel.status}]")
    return "\n".join(lines)


def build_history_report(service: DeliveryService, tracking_number: str) -> str:
    parcel = service.get_parcel(tracking_number)
    return f"履歴: {parcel.tracking_number}\n{' → '.join(parcel.history)}"


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
