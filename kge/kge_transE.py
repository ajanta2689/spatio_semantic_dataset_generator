import os
import pickle
import json
import torch
from pykeen.triples import TriplesFactory
from pykeen.pipeline import pipeline


class KGEmbedding:
    def __init__(self, param_file_path, data_file_path):
        self._param_file_path = param_file_path
        self._data_file_path = data_file_path
        self._tf = TriplesFactory.from_path(path=self._data_file_path)
        with open(self._param_file_path) as json_file:
            self._param_json = json.load(json_file)

    def train_embedding(self):
        training, testing, validation = self._tf.split(
            list(self._param_json["tf_split"].values())
        )
        resultsEmb = pipeline(
            training=training,
            testing=testing,
            validation=validation,
            **self._param_json["pipeline_param"]
        )
        results_location = "results/"
        resultsEmb.save_to_directory(results_location)
        os.listdir(results_location)

        with open(results_location + "triples_factory.pkl", "wb") as f:
            pickle.dump(self._tf, f)

        # Embeddings
        model = torch.load(results_location + "trained_model.pkl")
        entity_embeddings = model.entity_representations[0]

        entity_embedding = {}
        for entity in self._tf.entity_to_id.keys():
            if "<http://ex.com/point" in entity:
                entity_embedding[entity] = list(
                    entity_embeddings(torch.as_tensor(self._tf.entity_to_id[entity]))
                    .detach()
                    .numpy()
                )
        return entity_embedding


if __name__ == "__main__":
    kge_obj = KGEmbedding(
        param_file_path="param_transE.json",
        data_file_path="/dataset/dataset_obj_prop.tsv",
    )
    output_entity_emb = kge_obj.train_embedding()
    with open("dataset.json", "w") as f:
        json.dump(str(output_entity_emb), f)