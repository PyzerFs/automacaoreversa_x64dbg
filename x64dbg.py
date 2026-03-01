from x64dbgpy import dbg
import requests, os, time

SERVER_URL = "http://sua.maquinaouservidor/upload"
EXECUTABLE = "C:\\testes\\malware.exe"
DUMP_FOLDER = "C:\\temp\\dumps"
BREAKPOINTS = ["main", "WinMain", "sub_401000"]
os.makedirs(DUMP_FOLDER, exist_ok=True)


def capture_registers():
    regs = dbg.regs()
    filepath = os.path.join(DUMP_FOLDER, f"regs_{int(time.time())}.txt")
    with open(filepath, "w") as f:
        for reg, val in regs.items(): f.write(f"{reg}: {val}\n")
    return filepath


def capture_memory(addr, size=0x100):
    data = dbg.dump_memory(addr, size)
    filepath = os.path.join(DUMP_FOLDER, f"mem_{int(time.time())}.bin")
    with open(filepath, "wb") as f: f.write(data)
    return filepath


def capture_stack(size=0x100):
    stack_data = dbg.dump_stack(size)
    filepath = os.path.join(DUMP_FOLDER, f"stack_{int(time.time())}.bin")
    with open(filepath, "wb") as f: f.write(stack_data)
    return filepath


def upload_file(file_path):
    try:
        with open(file_path, "rb") as f:
            requests.post(SERVER_URL, files={"file": f})
    except Exception as e: print(f"Erro: {e}")


def capture_flow():
    upload_file(capture_registers())
    upload_file(capture_memory(dbg.reg("rax"), 0x100))
    upload_file(capture_stack(0x100))


for bp in BREAKPOINTS:
    try: dbg.bp(bp)
    except: pass

dbg.run(EXECUTABLE)

while True:
    dbg.continuee()
    if dbg.breakpoint_hit():
        capture_flow()
        for bp in BREAKPOINTS: dbg.del_bp(bp)
        break

dbg.quit()
