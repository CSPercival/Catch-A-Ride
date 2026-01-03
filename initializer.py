import zipfile
import os
import shutil

def main():
    # resources_to_unzip["GTFS.zip", "XML.zip"]
    resources_path = "./Components/Public_Transport/Resources"
    resources_zipped_path = "./Components/Public_Transport/Resources-zipped"

    if(os.path.isdir(resources_path)):
        shutil.rmtree(resources_path)

    for item in os.listdir(resources_zipped_path):
        with zipfile.ZipFile(resources_zipped_path + "/" + item, 'r') as zip_res:
            zip_res.extractall(resources_path)

if __name__ == "__main__":
    main()