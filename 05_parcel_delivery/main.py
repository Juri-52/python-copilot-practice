from data import create_couriers, create_parcels
from delivery_service import DeliveryService
from report import (
    build_delivery_summary,
    build_history_report,
    build_report,
    build_search_report,
)


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


if __name__ == "__main__":
    main()
