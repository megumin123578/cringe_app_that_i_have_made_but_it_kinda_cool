from datetime import datetime
import pytz

iso_time = "2025-07-08T22:40:47Z"
def convert_time(iso_time):
    utc_time = datetime.strptime(iso_time, "%Y-%m-%dT%H:%M:%SZ")
    utc_time = utc_time.replace(tzinfo=pytz.UTC)

    local_tz = pytz.timezone("Asia/Ho_Chi_Minh")
    local_time = utc_time.astimezone(local_tz)

    return local_time.strftime("%Y-%m-%d %H:%M:%S").split(' ')


print(convert_time(iso_time))