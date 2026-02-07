import os
import time
from Components.Map_Service.module_starter import Map_Module_Starter

def check_requierments():
    pass

def check_Map_Service():
    pass

def check_Public_Transport():
    pass

def check_Meeting_Point_Service():
    pass

def check_Visualizer():
    pass

def main():
    # check_requierments()
    absolute_path = os.getcwd()
    # print(absolute_path)

    MMS = Map_Module_Starter(absolute_path)
    MMS.run(20 * 60)
    time.sleep(10)
    MMS.shutdown()
    # check_Map_Service()
    # check_Public_Transport()
    # check_Meeting_Point_Service()
    # check_Visualizer()


if __name__ == "__main__":
    main()
