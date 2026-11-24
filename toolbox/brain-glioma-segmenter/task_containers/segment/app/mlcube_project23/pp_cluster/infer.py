import pandas as pd
import pickle
import argparse
from fops.load_store import load_json, save_json


def get_cluster(radiomics_df:pd.DataFrame, custer_arftifacts:dict)->list:
    normalizer = custer_arftifacts['normalizer']
    normal_values = normalizer.transform(radiomics_df.iloc[:, 1:].values)
    pca = custer_arftifacts['pca']
    scores_pca = pca.transform(normal_values)
    kmeans = custer_arftifacts['kmeans']
    # get the cluster assignment
    cluster_assignment = kmeans.predict(scores_pca)
    return cluster_assignment

def get_cluster_artifacts(task:str)->dict:
    if task == "MEN-RT":
        task = "MENRTw"
    pkl_path = f'/mlcube_project/kmeans-cluster-artifacts/{task}_cluster.pkl'
    with open(pkl_path, 'rb') as f:
        return pickle.load(f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_json", type=str)
    parser.add_argument("-o", "--output_json", type=str)
    parser.add_argument("-c", "--cluster_pickle", type=str)
    args = parser.parse_args()

    # df_radiomics = pd.read_csv('radiomics.csv')
    data = load_json(args.input_json) 
    df_radiomics = pd.DataFrame(data)
    with open(args.cluster_pickle, 'rb') as f:
        cluster_artifacts = pickle.load(f)
    cluster_assignment = get_cluster(df_radiomics, cluster_artifacts)

    for case, cluster in zip(data, cluster_assignment):
        case['cluster'] = int(cluster)
    save_json(args.output_json, data)