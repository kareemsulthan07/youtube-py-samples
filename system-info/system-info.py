import subprocess
import re
import GPUtil
import wmi

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

def get_processor_details():
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

def get_memory_cards_details():
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

def get_grpahics_card_details():
    gpus = GPUtil.getGPUs()
    for gpu in gpus:
        print(f"GPU ID: {gpu.id}")
        print(f"GPU Name: {gpu.name}")
        print(f"GPU Memory Total: {gpu.memoryTotal} MB")
        print(f"GPU Memory Free: {gpu.memoryFree} MB")
        print(f"GPU Memory Used: {gpu.memoryUsed} MB")
        print(f"GPU Load: {gpu.load * 100}%")
        print(f"GPU Temperature: {gpu.temperature} °C")

def get_bios_details():
    c = wmi.WMI()
    bios = c.win32_bios()[0]
    print(f"BIOS Version: {bios.version}")
    print(f"Manufacturer: {bios.manufacturer}")
    print(f"Serial Number: {bios.serialnumber}")
    print(f"SMBIOS Version: {bios.smbiosmajorversion}.{bios.smbiosminorversion}")
    print(f"BIOS Characteristics: {bios.bioscharacteristics}")


if __name__ =="__main__":
    print("\nPorcessor Info:")
    print("-" *40)
    get_processor_details()

    print("\n\nMemory Info:")
    print("-" *40)
    get_memory_cards_details()
    
    print("\n\nGraphics Card Info:")
    print("-" *40)
    get_grpahics_card_details()
    
    print("\n\nBIOS Info:")
    print("-" *40)
    get_bios_details()