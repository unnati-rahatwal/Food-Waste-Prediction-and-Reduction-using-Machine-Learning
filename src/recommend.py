def generate_recommendations(row):
    recs = []

    if row['quantity_prepared'] > row['num_guests'] * 1.2:
        recs.append("Reduce food preparation quantity")

    if row.get('Preparation_Method_Buffet', 0) == 1:
        recs.append("Switch from buffet to portioned serving")

    if row.get('num_guests', 0) > 400:
        recs.append("Improve demand forecasting for large events")

    return recs
