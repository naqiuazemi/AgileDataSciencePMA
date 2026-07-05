# duplicate_check.py

def check_duplicates(df):
    total_rows = len(df)
    duplicate_count = df.duplicated().sum()
    print("Total rows:", total_rows)
    print("Duplicate rows detected:", duplicate_count)
    if duplicate_count > 0:
        print("Percentage duplicates:", round((duplicate_count/total_rows)*100, 2), "%")
    else:
        print("No duplicates found.")
    return duplicate_count
