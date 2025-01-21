import numpy as np

INTEREST_RATE_PRECISION = 10**6


class CSOAMMPool:
    def __init__(self, strike_price, maturity) -> None:
        self.reserve_quote = 0
        self.reserve_base = 0
        self.reserve_claim = 0
        self.reserve_interest = 0
        self.strike_price = strike_price
        self.maturity = maturity
        pass

    def token_liquidity(self):
        return self.reserve_base * self.strike_price + self.reserve_quote

    def lending_liquidity(self):
        return np.sqrt(self.token_liquidity() * self.reserve_interest)

    def interest_rate(self):
        return int(
            (INTEREST_RATE_PRECISION - 1)  # For numerical precision
            * self.reserve_interest
            / self.token_liquidity()
        )

    def add(self, max_base, max_quote, max_interest):
        if (max_base > 0 and self.reserve_quote != 0) or (
            max_quote > 0 and self.reserve_base != 0
        ):
            raise ValueError("Trying to rebalance the pool while adding liquidity")
        elif self.lending_liquidity() == 0:
            self.reserve_base += max_base
            self.reserve_quote += max_quote
            self.reserve_interest += max_interest

            return (max_base, max_quote, max_interest)
        else:
            # (interest / claim) = (interest + delta_i) / (claim + delta_c)
            # claim + delta_c = (r_base + delta_base) * strike + r_quote + delta_quote
            self_ratio = self.reserve_interest / self.token_liquidity()
            input_ratio = max_interest / (max_base * self.strike_price + max_quote)
            if input_ratio > self_ratio:
                self.reserve_base += max_base
                self.reserve_quote += max_quote

                ri_before = self.reserve_interest
                self.reserve_interest = self_ratio * self.token_liquidity()

                return (max_base, max_quote, self.reserve_interest - ri_before)
            else:
                self.reserve_interest += max_interest
                if max_quote > 0:
                    reserve_quote_before = self.reserve_quote
                    self.reserve_quote = self.reserve_interest / self_ratio
                    return (0, self.reserve_quote - reserve_quote_before, max_interest)
                else:
                    reserve_base_before = self.reserve_base
                    self.reserve_base = (
                        self.reserve_interest / self_ratio / self.strike_price
                    )
                    return (self.reserve_base - reserve_base_before, 0, max_interest)
