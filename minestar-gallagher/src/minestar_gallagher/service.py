import win32serviceutil
import win32service
import win32event
import threading
import uvicorn
from minestar_gallagher.main import app   # Your FastAPI app

class MineStarGallagherService(win32serviceutil.ServiceFramework):
    _svc_name_ = "SEME-MineStar-Gallagher"
    _svc_display_name_ = "SEME MineStar–Gallagher Integration"
    _svc_description_ = "MineStar to Gallagher AOZ competency sync"

    def __init__(self, args):
        super().__init__(args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcDoRun(self):
        # Start health interface on localhost only
        def run_health():
            uvicorn.run(app, host="127.0.0.1", port=8765, log_level="info")   # ← localhost
        threading.Thread(target=run_health, daemon=True).start()

        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(MineStarGallagherService)