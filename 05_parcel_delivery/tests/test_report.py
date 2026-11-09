import pytest

from courier import Courier
from parcel import Parcel
from delivery_service import DeliveryService
from report import (
    build_delivery_summary,
    build_history_report,
    build_report,
    build_search_report,
)


def test_report_returns_text_without_changing_status():
    parcel = Parcel("P001", "田中")
    parcel.dispatch()
    assert build_report(DeliveryService([parcel])) == "荷物一覧:\nP001: 田中 [配送中]"
    assert parcel.status == "配送中"


def test_report_for_empty_service():
    assert build_report(DeliveryService([])) == "荷物一覧:"


def test_search_report_returns_exact_matching_text():
    service = DeliveryService([Parcel("P002", "Alice"), Parcel("P003", "ALICE Suzuki")])

    assert build_search_report(service, "alice") == (
        "検索結果:\n"
        "P002: Alice [受付済み]\n"
        "P003: ALICE Suzuki [受付済み]"
    )


def test_search_report_for_no_matches():
    assert build_search_report(DeliveryService([]), "alice") == (
        "検索結果:\n該当する荷物はありません"
    )


def test_history_report_returns_history_without_trailing_newline():
    parcel = Parcel("P001", "田中")
    parcel.dispatch()
    parcel.deliver()

    assert build_history_report(DeliveryService([parcel]), "P001") == (
        "履歴: P001\n受付済み → 配送中 → 配達完了"
    )


def test_history_report_propagates_unknown_tracking_number_error():
    service = DeliveryService([Parcel("P001", "田中")])

    with pytest.raises(ValueError, match="^荷物が見つかりません$"):
        build_history_report(service, "UNKNOWN")


def test_delivery_summary_counts_completed_and_incomplete_parcels():
    completed = Parcel("P001", "田中")
    assigned = Parcel("P002", "Alice")
    unassigned = Parcel("P003", "Bob")
    courier = Courier("C01", "配達員1")
    service = DeliveryService([completed, assigned, unassigned], [courier])
    service.assign_courier("P001", "C01")
    service.assign_courier("P002", "C01")
    service.dispatch_parcel("P001")
    service.deliver_parcel("P001")

    assert build_delivery_summary(service) == (
        "配送サマリー:\n"
        "C01: 配達員1 — 未完了 1件\n"
        "未割り当て — 未完了 1件"
    )


def test_delivery_summary_includes_couriers_with_no_parcels():
    service = DeliveryService([], [Courier("C01", "配達員1")])

    assert build_delivery_summary(service) == (
        "配送サマリー:\n"
        "C01: 配達員1 — 未完了 0件\n"
        "未割り当て — 未完了 0件"
    )


def test_delivery_summary_excludes_completed_unassigned_parcels():
    parcel = Parcel("P001", "田中")
    service = DeliveryService([parcel])
    service.dispatch_parcel("P001")
    service.deliver_parcel("P001")

    assert build_delivery_summary(service) == (
        "配送サマリー:\n未割り当て — 未完了 0件"
    )


def test_delivery_summary_for_empty_service():
    assert build_delivery_summary(DeliveryService([])) == (
        "配送サマリー:\n未割り当て — 未完了 0件"
    )


def test_delivery_summary_does_not_change_parcel_data_or_order():
    first = Parcel("P001", "田中")
    second = Parcel("P002", "Alice")
    courier = Courier("C01", "配達員1")
    service = DeliveryService([first, second], [courier])
    service.assign_courier("P001", "C01")
    service.dispatch_parcel("P001")
    before = [
        (parcel.status, parcel.courier_id, parcel.history.copy())
        for parcel in service.parcels
    ]
    parcel_order = list(service.parcels)
    courier_order = list(service.couriers)

    build_delivery_summary(service)

    assert [
        (parcel.status, parcel.courier_id, parcel.history)
        for parcel in service.parcels
    ] == before
    assert service.parcels == parcel_order
    assert service.couriers == courier_order
