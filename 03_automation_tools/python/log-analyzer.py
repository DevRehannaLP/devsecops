# ∞ ☬ DevRehannaLP ☬ | DevSecOps ∞ 20261603 1739
def read_log(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    return lines


lines = read_log("sample_system.log")


def analyze_log(lines):
    errors = []
    warnings = []
    criticals = []

    for line in lines:
        if "CRITICAL" in line:
            criticals.append(line.strip())
        elif "ERROR" in line:
            errors.append(line.strip())
        elif "WARNING" in line:
            warnings.append(line.strip())

    return criticals, errors, warnings


lines = read_log("sample_system.log")
criticals, errors, warnings = analyze_log(lines)

if len(criticals) > 0:
    status = "*** DANGER - CRITICAL EVENTS DETECTED***"
elif len(errors) > 0:
    status = "!! ATTENTION - Errors found, review needed"
elif len(warnings) > 0:
    status = "-- NOTICE - Warnings present, monitor closely"
else:
    status = "ALL CLEAR - System looks healthy"


def save_report(filename, criticals, errors, warnings, status):
    with open(filename, "w") as f:
        f.write("=== LOG ANALYSIS REPORT ===\n")
        f.write(status + "\n\n")
        f.write(f"CRITICALS: {len(criticals)}\n")
        for line in criticals:
            f.write(f"  {line}\n")
        f.write(f"\nERRORS: {len(errors)}\n")
        for line in errors:
            f.write(f"  {line}\n")
        f.write(f"\nWARNINGS: {len(warnings)}\n")
        for line in warnings:
            f.write(f"  {line}\n")


print("=== LOG ANALYSIS REPORT ===")
print(status)
print()

print(f"CRITICALS: {len(criticals)}")
for line in criticals:
    print(f" {line}")

print()
print(f"ERRORS: {len(errors)}")
for line in errors:
    print(f" {line}")

print()
print(f"WARNINGS: {len(warnings)}")
for line in warnings:
    print(f" {line}")

save_report("log_report.txt", criticals, errors, warnings, status)
print()
print("Report saved to log_report.txt")
