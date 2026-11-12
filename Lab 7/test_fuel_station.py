
from hypothesis import given, strategies as st
from fuel_station import (
    parse_purchase,
    volume_average,
    payable_bill
)


@given(st.text() | st.none())
def test_parse_purchase_no_crash(s):
    try:
        parse_purchase(s)
    except Exception as e:
        assert False, f"parse_purchase crashed with: {e}"


@given(st.text() | st.none())
def test_volume_average_no_crash(s):
    try:
        volume_average(s)
    except Exception as e:
        assert False, f"volume_average crashed with: {e}"


@given(st.text() | st.none())
def test_payable_bill_no_crash(s):
    try:
        payable_bill(s)
    except Exception as e:
        assert False, f"payable_bill crashed with: {e}"

