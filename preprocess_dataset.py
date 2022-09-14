import json
import pandas as pd
import pandasql as ps
from collections import defaultdict


type = "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>"
lat = "<http://www.w3.org/2003/01/geo/wgs84_pos#lat>"
long = "<http://www.w3.org/2003/01/geo/wgs84_pos#long>"
cluster_label = "<http://www.w3.org/2000/01/rdf-schema#comment>"


def dump_json(filename, data_as_json):
    with open(filename, "w") as f:
        json.dump(data_as_json, fp=f)


def load_json(filename):
    with open(filename) as f:
        input_nodes = json.load(f)
        return input_nodes


def read_dataset(filename: str):
    df = pd.read_csv(
        filename,
        sep="\t",
        header=None,
        usecols=[0, 1, 2],
        names=["subject", "predicate", "object"],
    )
    q = """select subject, predicate, object from df"""
    res = ps.sqldf(q, locals())
    return res


def create_json_from_rdf(filename):
    count = 0
    ignored_list = []
    sql_result = read_dataset(filename=filename)
    dict_node_types = defaultdict(list)
    dict_node_location = defaultdict(dict)
    dict_node_cluster_label = {}
    for index, row in sql_result.iterrows():
        count += 1
        node_name = row[0].split("/")[-1].replace(">", "")
        if row[1] == type and "<http://ex.com/point" in row[0]:
            type_str = row[2].split("/")[-1].replace(">", "")
            if type_str == "Node" or type_str == "spatial#Feature":
                continue
            else:
                dict_node_types[node_name].append(type_str)
        elif row[1] == lat:
            lat_val = row[2].split("^^", 1)[0]
            dict_node_location[node_name]["lat"] = lat_val
        elif row[1] == long:
            long_val = row[2].split("^^", 1)[0]
            dict_node_location[node_name]["long"] = long_val
        elif row[1] == cluster_label:
            label = row[2].split(" ")[3]
            dict_node_cluster_label[node_name] = label
        else:
            ignored_list.append(node_name)

    return (
        dict(sorted(dict_node_types.items())),
        dict(sorted(dict_node_location.items())),
        dict(sorted(dict_node_cluster_label.items())),
    )


if __name__ == "__main__":
    node_types, node_locations, cluster_labels = create_json_from_rdf(
        "dataset/dataset.tsv"
    )
    dump_json(filename="dataset/dataset_type.json", data_as_json=node_types)
    dump_json(
        filename="dataset/dataset_cluster_label.json", data_as_json=cluster_labels
    )
    # Further processed the node_locations to have the values of the map as (lat, long) pair
    node_loc_json = defaultdict(tuple)
    for key, value in node_locations.items():
        value["lat"] = float(value["lat"])
        value["long"] = float(value["long"])
        (lat_val, long_val) = (value["lat"], value["long"])
        if key in node_types.keys():
            node_loc_json[key] = (lat_val, long_val)
    dump_json(filename="dataset/dataset_loc.json", data_as_json=node_loc_json)
