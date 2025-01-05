import atheris
import sys
import numpy as np
from pool import CSOAMMPool


@atheris.instrument_func
def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)
    pool = CSOAMMPool(100, 100)
    pool.add(0, 100, 10)

    try:
        # Fuzz min_claim and min_interest parameters
        max_quote = fdp.ConsumeFloat()
        max_interest = fdp.ConsumeFloat()

        if max_quote == 0 or max_interest == 0:
            return

        # Call add() with fuzzed inputs
        rate_before = pool.interest_rate()
        pool.add(0, max_quote, max_interest)
        rate_after = pool.interest_rate()

        assert rate_before == rate_after, f"{rate_before} != {rate_after}"

    # except (ValueError, ZeroDivisionError, OverflowError):
    #     # Expected exceptions we want to catch
    #     pass
    except Exception as e:
        # Re-raise unexpected exceptions
        raise e


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
