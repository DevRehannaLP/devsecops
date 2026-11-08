# ∞ ☬ DevRehannaLP ☬ | DevSecOps ∞ 20261603 1739
import platform
import psutil


def get_os_info():
    print("=== System Info ===")
    print(f"OS:     {platform.system()}")
    print(f"Version: {platform.system()}")
    print(f"Machine: {platform.machine()}")


def get_cpu_info():
    print("\n=== CPU Info ===")
    print(f"Physical cores: {psutil.cpu_count(logical=False)}")
    print(f"Total cores:    {psutil.cpu_count(logical=False)}")
    print(f"CPU usage:      {psutil.cpu_percent(interval=1)}%")


def get_memory_info():
    mem = psutil.virtual_memory()
    print("\n=== Memory Info ===")
    print(f"Total:     {round(mem.total / (1024**3), 2)} GB")
    print(f"Used:      {round(mem.used / (1024**3), 2)} GB")
    print(f"Available: {round(mem.available / (1024**3), 2)} GB")
    print(f"Usage:     {mem.percent}%")


if __name__ == "__main__":
    get_os_info()
    get_cpu_info()
    get_memory_info()
