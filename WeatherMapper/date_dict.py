from datetime import datetime, timedelta

nader_dict = {}

start_date = datetime(1950, 10, 1)
end_date = datetime(2022, 9, 9)
step = timedelta(days=1)

current_date = start_date
while current_date <= end_date:
    nader_dict[current_date.strftime("%Y-%m-%d")] = []
    current_date += step

print(nader_dict)
