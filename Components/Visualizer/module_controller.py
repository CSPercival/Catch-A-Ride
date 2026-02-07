import subprocess
import time
import requests
import os

class Visualizer_Module_Controller:
    def __init__(self, main_dir_absolute_path):
        self.main_dir = main_dir_absolute_path
        self.vis_dir = main_dir_absolute_path + "/Components/Visualizer"
        self.vis_run_file = self.vis_dir + "/run.py"
        self.vis_run_module = "Components.Visualizer.run"
        
        self.server_process = None
        # self.docker_file = self.map_dir + "/ors-docker/docker-compose.yml"

    def _run_server(self):
        if self.server_process is not None:
            print("Visualizer server is already running.")
            return
        print("Starting Visualizer server", flush=True)
        if os.path.isfile(self.vis_run_file):
            self.server_process = subprocess.Popen(['python3', '-m', self.vis_run_module], cwd=self.main_dir)
        else:
            print("Visualizer run.py file not found.")
            raise FileNotFoundError("Visualizer run.py file not found.")

    def _shutdown_server(self):
        if self.server_process is None:
            print("Visualizer server is not running.")
            return
        print("Shutting down Visualizer server", flush=True)
        self.server_process.terminate()
        self.server_process.wait()
        self.server_process = None
        print("Visualizer server has been shut down", flush=True)

    def _check_if_server_ready(self):
        test_url = "http://127.0.0.1:5000"
        response = requests.get(test_url, timeout = 2)
        return response.status_code == 200

    
    def _wait_for_service(self, timeout):
        start_time = time.time()
        while True:
            try:
                if self._check_if_server_ready():
                    return True
            except requests.RequestException:
                pass
            if time.time() - start_time > timeout:
                break
            time.sleep(1)
        return False
    
    def get_status(self):
        pass

    def run(self, timeout):
        self._run_server()
        available = self._wait_for_service(timeout)
        while not available:
            print(f"Service not responding after {timeout}s\n Restarting the procedure in 10sec")
            self._shutdown_server()
            time.sleep(10)
            self._run_server()
            timeout += 60
            available = self._wait_for_service(timeout)
        print("Application server is ready")

    def shutdown(self):
        self._shutdown_server()
        pass 