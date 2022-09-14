import pandas as pd
import pandasql as ps

nodes = []


def create_df_from_rdf(filename: str, delimiter):
    print(filename)
    df = pd.read_csv(
        filename,
        sep=delimiter,
        header=None,
        usecols=[0, 1, 2],
        names=["subject", "predicate", "object"],
    )
    return df


def create_tsv_from_nt(nt_filename: str, tsv_filename: str):
    print(nt_filename)
    df = create_df_from_rdf(filename=nt_filename, delimiter=" ")
    df.to_csv(tsv_filename, sep="\t", index=False)


def create_tsv_from_df(df, tsv_filename: str):
    df.to_csv(tsv_filename, sep="\t", index=False, header=False)


def get_tsv_obj_prop(nt_filename: str, tsv_filename: str):
    df = create_df_from_rdf(filename=nt_filename, delimiter="\t")
    q = """SELECT subject, predicate, object
            FROM df
            WHERE (predicate != '<http://www.w3.org/2003/01/geo/wgs84_pos#lat>') and (predicate != '<http://www.w3.org/2003/01/geo/wgs84_pos#long>');
        """
    res = ps.sqldf(q, locals())
    create_tsv_from_df(res, tsv_filename)


def get_tsv_data_prop(nt_filename: str, tsv_filename: str):
    df = create_df_from_rdf(filename=nt_filename, delimiter="\t")
    q = """SELECT subject, predicate, object
            FROM df
            WHERE (predicate == '<http://www.w3.org/2003/01/geo/wgs84_pos#lat>') or (predicate == '<http://www.w3.org/2003/01/geo/wgs84_pos#long>');
        """
    res = ps.sqldf(q, locals())
    create_tsv_from_df(res, tsv_filename)


if __name__ == "__main__":
    # Creating new dataset with Data generator
    create_tsv_from_nt(
        "/dataset/dataset.nt",
        "dataset.tsv",
    )

    # Taking out the obj properties
    get_tsv_obj_prop("dataset.tsv", "dataset_obj_prop.tsv")
    # Taking out the data properties
    get_tsv_data_prop("dataset.tsv", "dataset_data_prop.tsv")
