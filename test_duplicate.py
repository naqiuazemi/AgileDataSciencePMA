
import pandas as pd
import pytest
from duplicate_check import check_duplicates

def test_no_duplicates():
    # Create a sample DataFrame with no duplicates
    df = pd.DataFrame({
        "InvoiceNo": [1, 2, 3],
        "Quantity": [10, 20, 30]
    })
    result = df.duplicated().sum()
    assert result == 0
