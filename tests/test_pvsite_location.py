from pvsite_forecast import calculate_penalty
import pandas as pd
import numpy as np
import pytest


def test_calculate_penalty():
    """
    Test the calculate_penalty function with mock data, ensuring it matches the implementation.
    """
    # Mock input DataFrame
    df = pd.DataFrame(
        {
            "datetime": pd.date_range("2021-01-01", periods=5, freq="D"),
            "forecast_power_kw": [0.1, 0.2, 0.3, 0.4, 0.5],
            "generation_power_kw": [0.2, 0.3, 0.5, 0.5, 1.0],
        }
    )

    region = "Karnataka"
    asset_type = "solar"
    capacity_kw = 2.0

    penalty_df, total_penalty = calculate_penalty(df, str(region), str(asset_type), capacity_kw)

    # For Karnataka solar:
    # - 10-20%: 0.25 penalty rate
    # - 20-30%: 0.50 penalty rate
    # - >30%: 0.75 penalty rate

    # Calculate for each row:
    # Row 1: (0.2 - 0.1)/2 * 100 = 5% -> No penalty
    # Row 2: (0.3 - 0.2)/2 * 100 = 5% -> No penalty
    # Row 3: (0.5 - 0.3)/2 * 100 = 10% -> 0.25 rate * abs(0.5-0.3) = 0.05
    # Row 4: (0.5 - 0.4)/2 * 100 = 5% -> No penalty
    # Row 5: (1.0 - 0.5)/2 * 100 = 25% -> 0.50 rate * abs(1.0-0.5) = 0.25

    expected_penalty_df = pd.Series([0.0, 0.0, 0.05, 0.0, 0.25], index=df.index)
    expected_total_penalty = 0.3

    # Assertions
    np.testing.assert_almost_equal(total_penalty, expected_total_penalty, decimal=2)
    pd.testing.assert_series_equal(
        penalty_df,
        expected_penalty_df,
        check_dtype=False,
        check_exact=False,
    )