import pandas as pd
from duplicate_check import check_duplicates

def test_no_duplicates():
    df = pd.DataFrame({
        "InvoiceNo": [1, 2, 3],
        "Quantity": [10, 20, 30]
    })
    result = check_duplicates(df)
    assert result == 0
