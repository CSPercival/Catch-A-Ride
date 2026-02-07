import zipfile
import os
import shutil

def main():
    resources_path = "./Components/Public_Transport/Resources"
    resources_zipped_path = "./Components/Public_Transport/Resources-zipped"

    if os.path.isdir(resources_path):
        shutil.rmtree(resources_path)
    os.makedirs(resources_path)

    for item in os.listdir(resources_zipped_path):
        if item.endswith(".zip"):
            folder_name = os.path.splitext(item)[0]
            
            target_dir = os.path.join(resources_path, folder_name)
            
            zip_file_path = os.path.join(resources_zipped_path, item)
            
            print(f"Extracting {item} to {target_dir}...")
            with zipfile.ZipFile(zip_file_path, 'r') as zip_res:
                zip_res.extractall(target_dir)

if __name__ == "__main__":
    main()