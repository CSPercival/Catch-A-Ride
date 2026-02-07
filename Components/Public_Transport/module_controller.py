import os
import subprocess
import zipfile
import os
import shutil


class PT_Module_Controller:
    def __init__(self, main_dir_absolute_path, Map_Module_Controller):
        self.main_dir = main_dir_absolute_path
        self.pt_dir = main_dir_absolute_path + "/Components/Public_Transport"
        self.resources_dir = self.pt_dir + "/Resources"
        self.zipped_resources_dir = self.pt_dir + "/Resources-zipped"
        self.preprocessing_dir = self.pt_dir + "/Preprocessing_data" 
        self.client_dir = self.pt_dir + "/Client" 

        self.map_model_controller = Map_Module_Controller

    def _unpack_resources(self):
        if os.path.isdir(self.resources_dir):
            shutil.rmtree(self.resources_dir)
        os.makedirs(self.resources_dir)

        for item in os.listdir(self.zipped_resources_dir):
            if item.endswith(".zip"):
                folder_name = os.path.splitext(item)[0]
                
                target_dir = os.path.join(self.resources_dir, folder_name)
                
                zip_file_path = os.path.join(self.zipped_resources_dir, item)
                
                print(f"Extracting {item} to {target_dir}...")
                with zipfile.ZipFile(zip_file_path, 'r') as zip_res:
                    zip_res.extractall(target_dir)

    def _make_programs_ready(self):
        makefile_path = os.path.join(self.preprocessing_dir, 'Makefile')
        if os.path.isfile(makefile_path):
            print("Running make to build C++ programs...")
            subprocess.run(['make', '-C', self.preprocessing_dir], check=True)
        else:
            print("Makefile not found in preprocessing directory.")
            raise FileNotFoundError("Makefile not found in preprocessing directory.")
        print("Make process completed.")

    def _run_ingestor(self):
        print("Running ingestor...")
        ingestor_path = os.path.join(self.preprocessing_dir, 'ingestor')
        if os.path.isfile(ingestor_path):
            subprocess.run([ingestor_path], check=True)
            pass
        else:
            print("Ingestor executable not found.")
            raise FileNotFoundError("Ingestor executable not found.")
        print("Ingestor process completed.")
    
    def _run_walk_calculation(self):
        print("Running walk calculation...")
        self.map_model_controller.run(60)
        walk_calc_path = os.path.join(self.preprocessing_dir, 'walk_preprocess', 'run.py')
        if os.path.isfile(walk_calc_path):
            print("Estimated time for walk calculation: 5-6 hours")
            subprocess.run(['python', walk_calc_path], check=True)
        else:
            print("Walk calculation executable not found.")
            raise FileNotFoundError("Walk calculation executable not found.")
        self.map_model_controller.shutdown()
        print("Walk calculation process completed.")


    def _run_travel_data_calculation(self):
        print("Running transit engine...")
        transit_engine_path = os.path.join(self.preprocessing_dir, 'transit_engine')
        if os.path.isfile(transit_engine_path):
            print("Estimated time for transit calculation: 5-6 hours")
            subprocess.run([transit_engine_path], check=True)
        else:
            print("Transit engine executable not found.")
            raise FileNotFoundError("Transit engine executable not found.")
        print("Travel engine process completed.")


    def get_status(self):
        status = {}
        if os.path.isfile(self.zipped_resources_dir + "/GTFS.zip"):
            status["GTFS-zipped"] = "present"
        else:
            status["GTFS-zipped"] = "missing"

        if os.path.isdir(self.resources_dir + "/GTFS"):
            status["GTFS"] = "present"
        else:
            status["GTFS"] = "missing"

        if os.path.isdir(self.resources_dir + "/Preprocessed_Data"):
            status["Preprocessed_Data"] = "present"
        else:
            status["Preprocessed_Data"] = "missing"

        if os.path.isfile(self.resources_dir + "/Preprocessed_Data/Common/Stops.json"):
            status["Stops"] = "present"
        else:
            status["Stops"] = "missing"
        if os.path.isfile(self.resources_dir + "/Preprocessed_Data/Common/Walk_Isochrones.json"):
            status["Walk_Isochrones"] = "present"
        else:
            status["Walk_Isochrones"] = "missing"
        if os.path.isfile(self.resources_dir + "/Preprocessed_Data/Common/Walk_Matrix.json"):
            status["Walk_Matrix"] = "present"
        else:
            status["Walk_Matrix"] = "missing"

        if os.path.isfile(self.resources_dir + "/Preprocessed_Data/Monday/Trips.json"):
            status["Monday_Trips"] = "present"
        else:
            status["Monday_Trips"] = "missing"
        if os.path.isfile(self.resources_dir + "/Preprocessed_Data/Monday/Travel_Data.bin"):
            status["Monday_Travel_Data"] = "present"
        else:
            status["Monday_Travel_Data"] = "missing"

        return status
        
    def run_processing(self, status=None):
        if status is None:
            status = self.get_status()
        print("Running preprocessing for Public Transport module...")
        print("GTFS-zipped:", status["GTFS-zipped"])
        if status["GTFS-zipped"] == "missing":
            # print("GTFS-zipped is missing. Please provide the GTFS.zip file in the Resources-zipped directory.")
            raise FileNotFoundError("GTFS-zipped is missing. Please provide the GTFS.zip file in the Resources-zipped directory.")
        print("GTFS:", status["GTFS"])
        if status["GTFS"] == "missing":
            self._unpack_resources()

        print("Preprocessed_Data:", status["Preprocessed_Data"])
        if status["Preprocessed_Data"] == "missing":
            self._make_programs_ready()
            self._run_ingestor()
            self._run_walk_calculation()
            self._run_travel_data_calculation()
            return

        print("Stops:", status["Stops"])
        print("Trips", status["Monday_Trips"])        
        if status["Stops"] == "missing" or status["Monday_Trips"] == "missing":
            self._make_programs_ready()
            self._run_ingestor()
            self._run_walk_calculation()
            self._run_travel_data_calculation()
            return

        print("Walk_Isochrones:", status["Walk_Isochrones"])
        print("Walk_Matrix:", status["Walk_Matrix"])
        if status["Walk_Isochrones"] == "missing" or status["Walk_Matrix"] == "missing":
            self._make_programs_ready()
            self._run_walk_calculation()
            self._run_travel_data_calculation()
            return

        print("Travel_Data:", status["Monday_Travel_Data"])
        if status["Monday_Travel_Data"] == "missing":
            self._make_programs_ready()
            self._run_travel_data_calculation()
            return

# mms = Map_Module_Starter()