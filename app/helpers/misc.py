from django.utils import timezone
from datetime import timedelta


def get_local_time():
    return timezone.now().astimezone(timezone.get_current_timezone())


def ip_is_allowed(ip_patterns, ip):
    if not ip_patterns:
        return False
    if isinstance(ip_patterns, str):
        ips = ip_patterns.split(",")
    elif isinstance(ip_patterns, list):
        ips = ip_patterns
    else:
        return False
    for aip in ips:
        aip = aip.strip()
        if aip == "*":
            return True
        elif "-" in aip:
            ip_base, end = aip.split("-")
            allow_base_pattern, start = ip_base.rsplit(".", 1)
            req_base_pattern, to_check = ip.rsplit(".", 1)
            if (allow_base_pattern == req_base_pattern) and (
                int(start) <= int(to_check) <= int(end)
            ):
                return True
        else:
            if aip == ip:
                return True
    return False


def get_chunks(data_list, n):
    """Yield successive n-sized chunks from data list."""
    for i in range(0, len(data_list), n):
        yield data_list[i : i + n]  # noqa


def get_key_or_default(value_dict, key, default_value):
    return value_dict.get(key) or default_value


def get_start_and_end_of_week(date=None, weekday_name=None):
    date = date or get_local_time().date()
    weekday = date.weekday()
    start = date - timedelta(days=weekday)
    end = start + timedelta(days=6)
    return start, end
