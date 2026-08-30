import platform
import time

import psutil


START_TIME = time.time()


def get_system_status():
    memory = psutil.virtual_memory()

    return {
        "core": "ACTIVE",
        "memory": "ACTIVE",
        "ai": "ACTIVE",

        "cpu_percent": psutil.cpu_percent(interval=0.1),

        "memory_percent": memory.percent,
        "memory_used_gb": round(
            memory.used / (1024 ** 3),
            2
        ),
        "memory_total_gb": round(
            memory.total / (1024 ** 3),
            2
        ),

        "python": platform.python_version(),
        "platform": platform.system(),

        "uptime_seconds": int(
            time.time() - START_TIME
        ),
    }