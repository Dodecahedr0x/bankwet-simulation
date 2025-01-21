import sys
import numpy as np
from hypothesis import given, assume, strategies as st
from pool import CSOAMMPool


@given(input_quote=st.integers(1, 2**58), input_interest=st.integers(1, 2**58))
def test_interest_rate_invariance(input_quote, input_interest):
    pool = CSOAMMPool(100, 100)
    pool.add(0, 100, 10)

    rate_before = pool.interest_rate()
    pool.add(0, input_quote, input_interest)
    rate_after = pool.interest_rate()

    assert (
        rate_before == rate_after
    ), f"{rate_before} != {rate_after} ({input_quote}, {input_interest})"
