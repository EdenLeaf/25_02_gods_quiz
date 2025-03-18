from datetime import date

calculations = [f'10.0°F is -12°C', '20.0°F is -7°C',
                '30.0°F is -1°C', '40.0°F is 4°C',
                '50.0°F is 10°C', '60.0°F is 16°C']

# **** Get current date for heading and filename
today = date.today()

# get day, month and year as individual strings
day = today.strftime("%d")
month = today.strftime("&m")
year = today.strftime("&Y")

file_name = f"temperatures_{year}_{month}_{day}"
write_to = f"{file_name}.txt"

with open(write_to, "w") as text_file:

    text_file.write("***** Temperature Calculations *****\n")
    text_file.write(f"Generated: {day}/{month}/{year}\n\n")
    text_file.write("Here is your calculation history (oldest to newest)...\n")

    # write the item to file
    for item in calculations:
        text_file.write(item)
        text_file.write("\n")
