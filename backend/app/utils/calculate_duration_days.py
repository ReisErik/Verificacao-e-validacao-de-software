def calculate_duration_days(start_date, end_date):
    total_days = max((end_date - start_date).days + 1, 1)
    return total_days