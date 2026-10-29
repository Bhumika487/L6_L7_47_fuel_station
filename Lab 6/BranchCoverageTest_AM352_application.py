
import pytest

from fuel_station import fuel_bill, pump_allowed, session_status


def test_fuel_bill_invalid_grade():
    with pytest.raises(ValueError):
        fuel_bill("unknown", 10, "silver")


def test_fuel_bill_negative_litres():
    with pytest.raises(ValueError):
        fuel_bill("regular", -1, "silver")


def test_fuel_bill_covered_and_extra_litres():
    assert fuel_bill("regular", 10, "silver") == 0
    assert fuel_bill("regular", 20, "silver") == 1050


def test_fuel_bill_gold_and_diesel():
    assert fuel_bill("regular", 20, "gold") == 525
    assert fuel_bill("diesel", 25, "gold") == 450


def test_fuel_bill_large_extra():
    assert fuel_bill("regular", 50, "silver") == 3960
    assert fuel_bill("regular", 50, "gold") == 3325
    assert fuel_bill("diesel", 60, "gold") == 3200


def test_pump_fleet_branches():
    assert pump_allowed(200, 2, True) is True
    assert pump_allowed(201, 2, True) is False


def test_pump_non_fleet_branches():
    assert pump_allowed(61, 1, False) is False
    assert pump_allowed(60, 1, False) is True
    assert pump_allowed(40, 2, False) is False


def test_session_status_card_day():
    assert session_status(60, True, False) == "active"
    assert session_status(45, True, False) == "warning"
    assert session_status(44, True, False) == "timed_out"


def test_session_status_cash_night():
    assert session_status(60, False, True) == "active"
    assert session_status(45, False, True) == "warning"
    assert session_status(44, False, True) == "timed_out"
