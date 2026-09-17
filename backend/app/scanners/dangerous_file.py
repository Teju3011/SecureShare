import io
import zipfile
from typing import Tuple, Optional


DANGEROUS_EXTENSIONS = {
    # Windows executables
    "exe", "dll", "scr", "com", "msi", "sys", "drv", "pif", "cpl",
    # Scripts
    "bat", "cmd", "ps1", "psm1", "sh", "bash", "zsh", "vbs", "vbe", "js", "jse", "wsf", "wsh", "hta",
    # Java
    "jar", "class",
    # Macro documents
    "docm", "xlsm", "pptm", "dotm", "xltm",
}


def check_dangerous_file(data: bytes, filename: str) -> Tuple[bool, str, Optional[str]]:
    """
    Analyzes raw file bytes and filename for dangerous content:
    - Executables (PE / ELF / Mach-O)
    - Shell / Batch / PowerShell scripts
    - Macro-enabled Office files containing VBA project streams
    - Dangerous extensions
    Returns:
        (is_dangerous, threat_category, details)
    """
    ext = filename.split(".")[-1].lower() if "." in filename else ""

    # 1. Binary executable detection by magic header
    if data.startswith(b"MZ"):
        return True, "EXECUTABLE_WINDOWS_PE", "Windows Executable or DLL binary detected via MZ header."

    if data.startswith(b"\x7fELF"):
        return True, "EXECUTABLE_LINUX_ELF", "Linux ELF executable binary detected via 7F 45 4C 46 signature."

    if (
        data.startswith(b"\xfe\xed\xfa\xce") or
        data.startswith(b"\xfe\xed\xfa\xcf") or
        data.startswith(b"\xce\xfa\xed\xfe") or
        data.startswith(b"\xcf\xfa\xed\xfe")
    ):
        return True, "EXECUTABLE_MACHO", "Apple macOS Mach-O executable binary detected."

    # 2. Extension check
    if ext in DANGEROUS_EXTENSIONS:
        return True, "DANGEROUS_EXTENSION", f"Disallowed executable or script file extension (.{ext})."

    # 3. Script contents and Shebang detection
    prefix_sample = data[:1024].lower()
    if prefix_sample.startswith(b"#!") and (b"bash" in prefix_sample or b"sh" in prefix_sample or b"python" in prefix_sample):
        return True, "SCRIPT_SHEBANG", "Executable shell script detected via Unix shebang."

    if b"@echo off" in prefix_sample or b"setlocal enabledelayedexpansion" in prefix_sample:
        return True, "SCRIPT_BATCH", "Windows batch script commands detected."

    if b"powershell" in prefix_sample or b"invoke-expression" in prefix_sample or b"start-process" in prefix_sample:
        return True, "SCRIPT_POWERSHELL", "PowerShell script command execution syntax detected."

    # 4. Office VBA Macro Detection (inside ZIP files)
    if data.startswith(b"PK\x03\x04"):
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as zf:
                namelist = [n.lower() for n in zf.namelist()]
                if any("vbaproject.bin" in name for name in namelist):
                    return True, "MACRO_ENABLED_DOCUMENT", "Embedded VBA macro binary (vbaProject.bin) detected inside Office document."
        except Exception:
            pass  # Not a valid zip or corrupted; standard parsers will reject

    return False, "CLEAN", None
