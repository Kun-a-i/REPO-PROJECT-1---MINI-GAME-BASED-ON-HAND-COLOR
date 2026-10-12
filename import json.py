import json

# 1. Load all valid IDs from karung_lookup.txt into a set
with open("karung_lookup.txt", "r") as f:
    valid_keys = set(line.strip() for line in f if line.strip())

# 2. Load your original JSON data
with open("lookup.json", "r") as f:
    data = json.load(f)

pid_acc_lookup = data.get("pid_acc_lookup", {})

# 3. Filter pid_acc_lookup based on inner values matching valid_keys
filtered_pid_acc = {}

for pid, dates in pid_acc_lookup.items():
    if isinstance(dates, dict):
        # Keep PID if any inner value (e.g., "6404") matches a key in karung_lookup.txt
        if any(str(val) in valid_keys for val in dates.values()):
            filtered_pid_acc[pid] = dates
    elif isinstance(dates, list):
        # Handle list format if present
        if any(str(val) in valid_keys for item in dates for val in (item.values() if isinstance(item, dict) else [item])):
            filtered_pid_acc[pid] = dates

# 4. Update the structure and save to a new JSON file
data["pid_acc_lookup"] = filtered_pid_acc

with open("filtered_lookup.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"Done! Retained {len(filtered_pid_acc)} entries with matching values.")