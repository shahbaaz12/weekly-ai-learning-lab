# What this file does: tests the three compensation rules directly, with no chain and no LLM call.

from tools import (
    calculate_damage_compensation,
    calculate_delay_compensation,
    calculate_lost_compensation,
    read_damage_percent,
    read_days_late,
)


def show(title: str, result: dict) -> None:
    """Print one calculator result as readable lines."""
    print(f"\n--- {title} ---")
    for key, value in result.items():
        print(f"{key}: {value}")


def main() -> None:
    # 1. Delay pays a daily rate: 2% of 400 for two days is 16.
    mild = calculate_delay_compensation(400, days_late=2)
    show("delay, $400 shipment, 2 days late", mild)
    assert mild["compensation"] == 16.0

    # The cap stops a long delay from costing more than a quarter of the load.
    long_delay = calculate_delay_compensation(400, days_late=60)
    show("delay, $400 shipment, 60 days late", long_delay)
    assert long_delay["compensation"] == 100.0

    # The floor keeps a tiny claim worth processing.
    tiny = calculate_delay_compensation(50, days_late=1)
    show("delay, $50 shipment, 1 day late", tiny)
    assert tiny["compensation"] == 10.0

    # 2. Damage pays the damaged share, with a floor.
    minor = calculate_damage_compensation(300, damage_percent=10)
    show("damage, $300 shipment, 10% damaged", minor)
    assert minor["compensation"] == 30.0

    total = calculate_damage_compensation(1000, damage_percent=100)
    show("damage, $1000 shipment, 100% damaged", total)
    assert total["compensation"] == 1000.0

    # 3. Lost pays the whole shipment plus the service credit.
    lost = calculate_lost_compensation(8000)
    show("lost, $8000 shipment", lost)
    assert lost["compensation"] == 8800.0
    assert lost["service_credit"] == 800.0

    # 4. The readers pull severity out of the report text.
    assert read_days_late("It arrived 4 days late.") == 4
    assert read_days_late("It was late.") == 1
    assert read_damage_percent("About 45% of the crate was wet.") == 45
    assert read_damage_percent("There is a minor scuff on one box.") == 10
    assert read_damage_percent("Something happened to it.") == 30
    print("\nText readers returned the expected severities.")

    print("\nAll compensation checks passed.")


if __name__ == "__main__":
    main()
