import pandas as pd

df = pd.read_csv("DQC_v2.tsv", delimiter="\t", encoding="cp1252")

output_rows = []

years = [ "S", "1652", "1742", "1755", "1885", "1949", "1950", "1999", "2003" ]

def get_year_value(year, row):
    return row[year]

def output():
    # But only if it is not None
    if current_set is None:
        return
        
    for key in current_set:
        year_dict = current_set[key]
        output_rows.append(year_dict)

current_set = None

for index, row in df.iterrows():
    # Upon a new full record, push the current record to the output list
    if row["lt"] == "a - text":
        output()

        current_set = {}
            
        for year in years:
            current_set[year] = {}
            current_set[year]["year"] = year
            current_set[year]["corpus_text"] = get_year_value(year, row)
            current_set[year]["#r"] = row["#r"]
            current_set[year]["#"] = row["#"]
            current_set[year]["chapter"] = row["chapter"]
            current_set[year]["text"] = row["text"]
            current_set[year]["ref"] = row["ref"]
            current_set[year]["pos"] = row["pos"]
    elif row["lt"] == "b - strategy":
        for year in years:
            current_set[year]["strategy"] = get_year_value(year, row)
    elif row["lt"] == "c - strategy type":
        for year in years:
            current_set[year]["strategy_type"] = get_year_value(year, row)
    elif row["lt"] == "d - tense":
        for year in years:
            current_set[year]["tense"] = get_year_value(year, row)
    elif row["lt"] == "e - context":
        for year in years:
            current_set[year]["context"] = get_year_value(year, row)
    elif row["lt"] == "f - situation type":
        for year in years:
            current_set[year]["situation_type"] = get_year_value(year, row)
    elif row["lt"] == "g - comment":
        for year in years:
            current_set[year]["comment"] = get_year_value(year, row)

output()

output_df = pd.DataFrame.from_records(output_rows)
output_df.fillna('', inplace=True)
output_df.head()

output_df.to_csv("juliette_table.tsv", sep="\t", index=None)
output_df.to_excel("juliette_table.xlsx")