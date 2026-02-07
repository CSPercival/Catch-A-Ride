import json
from Components.Public_Transport.Preprocessing_data.walk_preprocess.compute import compute_walk_matrix, compute_walk_isochrones

def get_walk_matrix():
    with open('Components/Public_Transport/Resources/Preprocessed_Data/Common/Stops.json', 'r') as f:
        stop_data = json.load(f)
    # walk_matrix = compute_walk_matrix(stop_data)
    walk_isochrones = compute_walk_isochrones(stop_data)
    # with open('Components/Public_Transport/Resources/Preprocessed_Data/Common/Walk_Matrix.json', 'w') as f:
    #     json.dump(walk_matrix, f, indent=4)
    with open('Components/Public_Transport/Resources/Preprocessed_Data/Common/Walk_Isochrones.json', 'w') as f:
        json.dump(walk_isochrones, f)

if __name__ == "__main__":
    get_walk_matrix()