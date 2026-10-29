import pytest

from fuel_station import fuel_bill, pump_allowed, session_status


# Tests for fuel_bill()

def test_fuel_bill_unknown_grade():
    with pytest.raises(ValueError, match="unknown fuel grade"):
        fuel_bill("kerosene", 20, "silver")


def test_fuel_bill_negative_litres():
    with pytest.raises(ValueError, match="invalid litres"):
        fuel_bill("regular", -1, "silver")


def test_fuel_bill_regular_fuel_fully_covered():
    assert fuel_bill("regular", 10, "silver") == 0


def test_fuel_bill_gold_regular_fuel():
    # Gold covers 10 + 5 litres; 20 - 15 = 5 extra litres.
    assert fuel_bill("regular", 20, "gold") == 5 * 105


def test_fuel_bill_premium_fuel():
    assert fuel_bill("premium", 20, "silver") == 5 * 105


def test_fuel_bill_diesel_fully_covered():
    assert fuel_bill("diesel", 20, "gold") == 0


def test_fuel_bill_diesel_extra_litres():
    assert fuel_bill("diesel", 25, "silver") == 5 * 90


def test_fuel_bill_regular_extra_litres():
    assert fuel_bill("regular", 20, "silver") == 10 * 105


def test_fuel_bill_large_extra_non_gold():
    # Extra = 50 - 10 = 40; rate = 105 - 6 = 99.
    assert fuel_bill("regular", 50, "silver") == 40 * 99


def test_fuel_bill_large_extra_gold():
    # Extra = 50 - 15 = 35; rate = 105 - 6 - 4 = 95.
    assert fuel_bill("regular", 50, "gold") == 35 * 95


def test_fuel_bill_large_extra_gold_diesel():
    # Gold does not add 5 covered litres for diesel.
    # Extra = 60 - 20 = 40; rate = 90 - 6 - 4 = 80.
    assert fuel_bill("diesel", 60, "gold") == 40 * 80


# Tests for pump_allowed()

def test_pump_allowed_fleet_within_limit():
    assert pump_allowed(200, 5, True) is True


def test_pump_rejected_fleet_over_limit():
    assert pump_allowed(201, 1, True) is False


def test_pump_rejected_non_fleet_over_60_litres():
    assert pump_allowed(61, 1, False) is False


def test_pump_allowed_non_fleet_one_container():
    assert pump_allowed(60, 1, False) is True


def test_pump_rejected_non_fleet_multiple_containers():
    assert pump_allowed(40, 2, False) is False


# Tests for session_status()

def test_session_active_card_payment_day():
    assert session_status(60, True, False) == "active"


def test_session_warning_card_payment_day():
    assert session_status(45, True, False) == "warning"


def test_session_timed_out_card_payment_day():
    assert session_status(44, True, False) == "timed_out"


def test_session_active_cash_payment_day():
    assert session_status(30, False, False) == "active"


def test_session_warning_cash_payment_night():
    assert session_status(45, False, True) == "warning"


def test_session_timed_out_cash_payment_night():
    assert session_status(44, False, True) == "timed_out"


def test_session_active_card_payment_night():
    assert session_status(90, True, True) == "active"