import pytest
from courier import Courier
from parcel import Parcel
from delivery_service import DeliveryService


def test_get_parcel_returns_same_object():
    parcel = Parcel("P001", "田中")
    assert DeliveryService([parcel]).get_parcel("P001") is parcel


def test_delivery_does_not_change_other_parcel():
    first, second = Parcel("P001", "田中"), Parcel("P002", "Alice")
    service = DeliveryService([first, second])
    service.dispatch_parcel("P001")
    service.deliver_parcel("P001")
    assert first.status == "配達完了"
    assert second.status == "受付済み"


def test_unknown_tracking_number_preserves_data():
    parcel = Parcel("P001", "田中")
    service = DeliveryService([parcel])
    with pytest.raises(ValueError, match="^荷物が見つかりません$"):
        service.dispatch_parcel("UNKNOWN")
    assert service.parcels == [parcel]
    assert parcel.status == "受付済み"


def test_delivery_does_not_change_other_parcel_history():
    first, second = Parcel("P001", "田中"), Parcel("P002", "Alice")
    service = DeliveryService([first, second])
    service.dispatch_parcel("P001")
    service.deliver_parcel("P001")

    assert first.history == ["受付済み", "配送中", "配達完了"]
    assert second.history == ["受付済み"]


def test_one_courier_can_have_multiple_parcels_in_original_order():
    first = Parcel("P001", "田中")
    second = Parcel("P002", "Alice")
    third = Parcel("P003", "Bob")
    courier = Courier("C01", "配達員1")
    service = DeliveryService([first, second, third], [courier])

    service.assign_courier("P003", "C01")
    service.assign_courier("P001", "C01")

    assigned = service.get_courier_parcels("C01")
    assert assigned == [first, third]
    assert assigned[0] is first
    assert assigned[1] is third


def test_courier_can_be_reassigned_before_delivery():
    parcel = Parcel("P001", "田中")
    first = Courier("C01", "配達員1")
    second = Courier("C02", "配達員2")
    service = DeliveryService([parcel], [first, second])

    service.assign_courier("P001", "C01")
    service.assign_courier("P001", "C01")
    service.assign_courier("P001", "C02")

    assert parcel.courier_id == "C02"
    assert service.get_courier_parcels("C01") == []
    assert service.get_courier_parcels("C02") == [parcel]
    assert parcel.status == "受付済み"
    assert parcel.history == ["受付済み"]


def test_get_courier_returns_same_object_and_unknown_id_fails():
    courier = Courier("C01", "配達員1")
    service = DeliveryService([], [courier])

    assert service.get_courier("C01") is courier
    with pytest.raises(ValueError, match="^配達員が見つかりません$"):
        service.get_courier("UNKNOWN")


def test_unknown_parcel_has_priority_over_unknown_courier():
    service = DeliveryService([], [Courier("C01", "配達員1")])

    with pytest.raises(ValueError, match="^荷物が見つかりません$"):
        service.assign_courier("UNKNOWN", "UNKNOWN")


def test_unknown_courier_does_not_change_parcel_assignment():
    parcel = Parcel("P001", "田中")
    service = DeliveryService([parcel], [Courier("C01", "配達員1")])

    with pytest.raises(ValueError, match="^配達員が見つかりません$"):
        service.assign_courier("P001", "UNKNOWN")

    assert parcel.courier_id is None
    assert parcel.status == "受付済み"
    assert parcel.history == ["受付済み"]


def test_completed_parcel_rejects_assignment_without_changing_data():
    parcel = Parcel("P001", "田中")
    first = Courier("C01", "配達員1")
    second = Courier("C02", "配達員2")
    service = DeliveryService([parcel], [first, second])
    service.assign_courier("P001", "C01")
    service.dispatch_parcel("P001")
    service.deliver_parcel("P001")

    status = parcel.status
    history = parcel.history.copy()
    with pytest.raises(
        ValueError, match="^配達完了の荷物には割り当てできません$"
    ):
        service.assign_courier("P001", "C02")

    assert parcel.courier_id == "C01"
    assert parcel.status == status
    assert parcel.history == history
    assert service.get_courier_parcels("C01") == [parcel]
    assert service.get_courier_parcels("C02") == []


def test_get_courier_parcels_for_unassigned_courier_is_empty():
    courier = Courier("C01", "配達員1")
    service = DeliveryService([Parcel("P001", "田中")], [courier])

    assert service.get_courier_parcels("C01") == []


def test_courier_assignment_does_not_require_courier_for_dispatch():
    parcel = Parcel("P001", "田中")
    service = DeliveryService([parcel])

    service.dispatch_parcel("P001")
    service.deliver_parcel("P001")

    assert parcel.status == "配達完了"


@pytest.mark.parametrize(
    ("keyword", "expected_tracking_numbers"),
    [
        (" ALICE ", ["P002", "P003"]),
        ("p00", ["P001", "P002", "P003", "P004", "P005"]),
        ("田", ["P001"]),
        ("   ", []),
        ("UNKNOWN", []),
    ],
)
def test_search_parcels_matches_keyword_cases(keyword, expected_tracking_numbers):
    parcels = [
        Parcel("P001", "田中"),
        Parcel("P002", "Alice"),
        Parcel("P003", "ALICE Suzuki"),
        Parcel("P004", "佐藤"),
        Parcel("P005", "Bob"),
    ]

    results = DeliveryService(parcels).search_parcels(keyword)

    assert [parcel.tracking_number for parcel in results] == expected_tracking_numbers


def test_search_parcels_returns_same_objects_without_duplicates():
    matching_parcel = Parcel("P00", "P00 recipient")
    other_parcel = Parcel("P001", "Other")
    service = DeliveryService([matching_parcel, other_parcel])

    results = service.search_parcels("p00")

    assert results == [matching_parcel, other_parcel]
    assert results[0] is matching_parcel
    assert results[1] is other_parcel


def test_search_parcels_includes_delivered_parcels_without_changing_status():
    parcel = Parcel("P001", "田中")
    parcel.dispatch()
    parcel.deliver()
    service = DeliveryService([parcel])

    results = service.search_parcels("田")

    assert results == [parcel]
    assert parcel.status == "配達完了"


def test_search_parcels_for_empty_service():
    assert DeliveryService([]).search_parcels("P001") == []
