import win32serviceutil
import win32service
import win32event
import servicemanager
import time

from agent_it.client.eventlog import check_events


class AgentService(win32serviceutil.ServiceFramework):

    _svc_name_ = "AgentIT"
    _svc_display_name_ = "Agent IT Monitoring"
    _svc_description_ = "Detects workstation boot and shutdown events"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.running = True

    def SvcStop(self):
        self.running = False
        win32event.SetEvent(self.stop_event)
        servicemanager.LogInfoMsg("AgentIT service stopped")

    def SvcDoRun(self):
        servicemanager.LogInfoMsg("AgentIT service started")

        while self.running:

            try:
                check_events()
            except Exception as e:
                servicemanager.LogErrorMsg(str(e))

            time.sleep(5)