import os
import subprocess
from pathlib import Path
import socket
import time
import requests
import time


# def wait_for_service(timeout=30):
#     start_time = time.time()
#     while True:
#         try:
#             result = check_if_ready()
#             if result:
#                 return result
#         except requests.RequestException:
#             pass
#         if time.time() - start_time > timeout:
#             raise TimeoutError(f"ORS not ready after {timeout}s")
#         time.sleep(1)
#     return False
    

# def _post(self, query_url: str, data: dict) -> dict:
#         url = f"{self.base_url}/{query_url}"
#         response = requests.post(url, json=data, timeout=self.timeout)
#         print(response, flush=True)
#         print(response.text, flush=True)
#         response.raise_for_status()
#         return response.json()

# def _snap(self, coordinate):
#     data = {
#         "locations": [reverse_coordinates(coordinate)],
#         "radius": radius
#     }
#     res = self._post(f"v2/snap/{self.profile}", data)
#     return reverse_coordinates(res['locations'][0]['location'])

# def check_if_ready():
#     data = {
#         "locations": [["17.03242", "51.10960"]],
#         "radius": 10
#     }
#     url = "http://localhost:8085/ors/v2/snap/foot-walking"
#     response = requests.post(url, json=data)
#     return response.status_code == 200

# def run():
#     """Start Docker Compose."""
#     # print("Starting Docker Compose...")
#     # subprocess.Popen(DOCKER_COMPOSE_CMD)
#     # print("Docker Compose started.")
#     print(wait_for_service())



class Map_Module_Starter:
    def __init__(self, main_dir_absolute_path):
        self.main_dir = main_dir_absolute_path
        self.map_dir = main_dir_absolute_path + "/Components/Map_Service"
        self.docker_file = self.map_dir + "/ors-docker/docker-compose.yml"

    def _docker_up(self):
        print("Initializing docker with ORS", flush=True)
        
        command_docker_up = [
            "docker", "compose",
            "-f", self.docker_file,
            "up", "-d"
        ]
        subprocess.run(command_docker_up, check=True)

    def _docker_down(self):
        print("Shutting down docker with ORS", flush=True)
        
        command_docker_down = [
            "docker", "compose",
            "-f", self.docker_file,
            "down"
        ]
        subprocess.run(command_docker_down, check=True)

    def _check_if_docker_ready(self):
        # data = {
        #     "locations": [["17.03242", "51.10960"]],
        #     "radius": 10
        # }
        # url = "http://localhost:8085/ors/v2/snap/foot-walking"
        # response = requests.post(url, json=data)
        # return response.status_code == 200
        test_url = "http://localhost:8085/ors/v2/health"
        response = requests.get(test_url, timeout = 2)
        return response.status_code == 200

    
    def _wait_for_service(self, timeout):
        start_time = time.time()
        while True:
            try:
                if self._check_if_docker_ready():
                    return True
            except requests.RequestException:
                pass
            if time.time() - start_time > timeout:
                break
                # raise TimeoutError(f"ORS not ready after {timeout}s")
            time.sleep(1)
        return False
    
    def prepare(self):
        pass

    def run(self, timeout):
        self._docker_up()
        available = self._wait_for_service(timeout)
        while not available:
            print(f"ORS not responding after {timeout}s\n Restarting the procedure in 10sec")
            timeout += 60
            self._docker_down()
            time.sleep(10)
            available = self._docker_up()
        print("ORS is ready")

    def shutdown(self):
        self._docker_down()
        pass 

# mms = Map_Module_Starter()