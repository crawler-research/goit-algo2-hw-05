import json
import time
from hyperloglog import HyperLogLog

LOG_FILE_PATH = "lms-stage-access.log"
HLL_ERROR_RATE = 0.005

def load_ip_addresses_from_log(log_file_path):
    ip_addresses = []
    processed_lines = 0
    skipped_lines = 0
    with open(log_file_path, 'r', encoding='utf-8') as f:
        for line_number, line in enumerate(f, 1):
              log_entry = json.loads(line)
              if "remote_addr" in log_entry and isinstance(log_entry["remote_addr"], str):
                  ip_addresses.append(log_entry["remote_addr"])
              else:
                  skipped_lines += 1

  
    return ip_addresses, processed_lines, skipped_lines

def count_exact_unique_ips(ip_list):
    if not ip_list:
        return 0
    return len(set(ip_list))

def estimate_hll_unique_ips(ip_list, error_rate):
    if not ip_list:
        return 0
    hll = HyperLogLog(error_rate)
    for ip in ip_list:
        hll.add(ip)
    return len(hll)

ip_addresses, total_lines, skipped_lines = load_ip_addresses_from_log(LOG_FILE_PATH)

print(f"Всього {len(ip_addresses)} IP addresses.")

# --Exact Count 
start_time_exact = time.perf_counter()
exact_count = count_exact_unique_ips(ip_addresses)
end_time_exact = time.perf_counter()
time_taken_exact = end_time_exact - start_time_exact

#  HyperLogLog  
start_time_hll = time.perf_counter()
hll_estimate = estimate_hll_unique_ips(ip_addresses, HLL_ERROR_RATE)
end_time_hll = time.perf_counter()
time_taken_hll = end_time_hll - start_time_hll

print("результати:")

header = f" Точний підрахунок HyperLogLog"

separator = "----------------------------------------------------" 
unique_elements_row = f"Унікальні елементи {float(exact_count):.1f} {hll_estimate:.1f}"

print(header)
print(separator)
print(unique_elements_row)
print(f"Час виконання (сек.) {time_taken_exact:.4f} {time_taken_hll:.4f}")
