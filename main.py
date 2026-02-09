import os
from Components.Map_Service.module_controller import Map_Module_Controller
from Components.Public_Transport.module_controller import PT_Module_Controller
from Components.Visualizer.module_controller import Visualizer_Module_Controller
import pkg_resources
import subprocess

def check_requirements():
    print("Checking Docker and required Python packages...", flush=True)
    try:
        subprocess.check_output(["docker", "info"], stderr=subprocess.STDOUT)
        print("Docker is installed and running", flush=True)
    except subprocess.CalledProcessError:
        print("Error: Docker is installed but the daemon is not running.", flush=True)
        exit(1)
    except FileNotFoundError:
        print("Error: The 'docker' command was not found in your PATH.", flush=True)
        exit(1)

    try:
        with open("requirements.txt", "r") as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        
        installed_packages = {pkg.key for pkg in pkg_resources.working_set}
        
        missing_packages = []
        for req in requirements:
            package_name = req.split("==")[0].split(">=")[0].split("<=")[0].split(">")[0].split("<")[0].replace("-", "_").lower()
            if package_name not in installed_packages:
                missing_packages.append(req)
        
        if missing_packages:
            print(f"Error: Missing packages: {', '.join(missing_packages)}", flush=True)
            exit(1)
        else:
            print("All required packages are installed", flush=True)
    except FileNotFoundError:
        print("Error: requirements.txt not found", flush=True)
        exit(1)
    except Exception as e:
        print(f"Error checking requirements: {e}", flush=True)
        exit(1)
    
    print("All requirements are satisfied!", flush=True)

def main():
    check_requirements()
    absolute_path = os.getcwd()
    # print(absolute_path)

    MMC = Map_Module_Controller(absolute_path)
    PTMC = PT_Module_Controller(absolute_path, MMC)
    VMC = Visualizer_Module_Controller(absolute_path)
    print("-------------------------------------------------------------------------------------")
    print("Checking Map Service", flush=True)
    MMC.run(20 * 60)
    MMC.shutdown()

    print("-------------------------------------------------------------------------------------")
    print("Checking Public Transport Service", flush=True)
    PTMC.run_processing()

    print("-------------------------------------------------------------------------------------")
    print("Checking Visualizer", flush=True)
    VMC.run(60)
    VMC.shutdown()

    print("-------------------------------------------------------------------------------------")
    print("All components checked successfully!", flush=True)
    
    print("Running the application...", flush=True)
    MMC.run(60)
    VMC.run(60)
    print("-------------------------------------------------------------------------------------")
    try:
        while True:
            user_input = input("Enter 'quit' or 'exit' to stop: ").strip().lower()
            if user_input in ('quit', 'exit'):
                break
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received.", flush=True)

    print("Shutting down the application...", flush=True)
    MMC.shutdown()
    VMC.shutdown()
    print("Application stopped successfully!", flush=True)

if __name__ == "__main__":
    main()
