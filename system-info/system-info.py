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

def memory_type_to_str(code):
    types = {
        20: "DDR",
        21: "DDR2",
        22: "DDR2 FB-DIMM",
        24: "DDR3",
        26: "DDR4",
        34: "DDR5",
        0: "Unknown"
    }
    return types.get(code, "Unknown")

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

def get_memory_cards_info():
    try:
        powershell_cmd = (
            "Get-CimInstance -ClassName Win32_PhysicalMemory | "
            "Select-Object Manufacturer, Capacity, Speed, PartNumber, SMBIOSMemoryType"
        )

        result = subprocess.run(
            ["powershell", "-Command", powershell_cmd],
            capture_output=True, text=True
        )

        lines = result.stdout.strip().splitlines()
        for line in lines:
            if ':' in line:
                key, value = map(str.strip, line.split(':',1))
                if(key == "SMBIOSMemoryType"):
                    key = "Memory Type"
                    value = f"{memory_type_to_str(int(value.strip()))}\n"
                
                print(f"{prettify_key(key=key)}: {value}")

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ =="__main__":
    print("\nPorcessor Info:")
    print("-----------------------------")
    get_processor_info()

    print("\n\nMemory Info:")
    print("-----------------------------")
    get_memory_cards_info()