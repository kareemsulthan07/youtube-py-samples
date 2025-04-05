import subprocess
import re

def arch_code_to_str(code):
    """Convert architecture code into model"""
    lookup = {
        "0": "x86",
        "1": "MIPS",
        "2": "Alpha",
        "3": "PowerPC",
        "5": "ARM",
        "6": "Itanium",
        "9": "x64"
    }
    return lookup.get(code, f"Unknown ({code})")

def prettify_key(key):
    """Add space between each capital letter (but skip first letter)"""
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', key)


def get_processor_info():
    try:
        powershell_cmd = (
            "Get-CimInstance Win32_Processor | "
            "Select-Object Name, NumberOfCores, NumberOfLogicalProcessors, "
            "Architecture, SocketDesignation, MaxClockSpeed, L2CacheSize, L3CacheSize"
        )

        result = subprocess.run(
            ["powershell", "-Command", powershell_cmd],
            capture_output=True, text=True
        )

        lines = result.stdout.strip().splitlines()
        for line in lines:
            if ':' in line:
                key, value = map(str.strip, line.split(':',1))

                if key == "Architecture":
                    value = arch_code_to_str(value)

                print(f"{prettify_key(key=key)}: {value}")

    except Exception as e:
        return {"Error": str(e)}


if __name__ =="__main__":
    get_processor_info()