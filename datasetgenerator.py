import random

import matplotlib.pyplot as plt
from rdflib import Graph, URIRef, RDF, RDFS, Literal, XSD

from classhierarchy import ClassHierarchyGenerator
from gaussian import Gaussian

GEOSPARQL_NS = "http://www.opengis.net/ont/geosparql#"
FEATURE_CLS = URIRef(GEOSPARQL_NS + "Feature")
GEOMETRY_CLS = URIRef(GEOSPARQL_NS + "Geometry")
HAS_GEOMETRY = URIRef(GEOSPARQL_NS + "hasGeometry")
AS_WKT = URIRef(GEOSPARQL_NS + "asWKT")
WKT_TYPE = URIRef(GEOSPARQL_NS + "wktLiteral")
LAT = URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#lat")
LON = URIRef("http://www.w3.org/2003/01/geo/wgs84_pos#long")


def generate(
    num_points: int,
    num_classes: int,
    num_clusters: int,
    lat_min: float,
    lat_max: float,
    lon_min: float,
    lon_max: float,
    output_file_path: str,
):

    while True:
        class_hierarchy_genertor = ClassHierarchyGenerator(num_classes, num_clusters)

        class_hierarchy = class_hierarchy_genertor.get_random_hierarchy()
        print(class_hierarchy)

        cluster_base_classes = list(
            class_hierarchy.get_direct_subclasses(class_hierarchy.T)
        )

        dist_lat = lat_max - lat_min
        dist_lon = lon_max - lon_min

        cluster_gaussians = []

        colors = list(plt.colormaps.get("Paired").colors)
        assert num_clusters <= len(colors)
        random.shuffle(colors)

        # create random Gaussian distributions
        for i in range(num_clusters):
            mu_lat = random.uniform(lat_min, lat_max)
            mu_lon = random.uniform(lon_min, lon_max)

            sigma_lon = random.uniform(dist_lon / (num_classes - 1), dist_lon / 3)
            sigma_lat = random.uniform(dist_lat / (num_classes - 1), dist_lat / 3)

            angle = random.uniform(0, 180)

            color = colors.pop()

            gaussian = Gaussian(mu_lat, mu_lon, sigma_lat, sigma_lon, angle, color)

            cluster_gaussians.append(gaussian)

        points = []
        point_clusters = []  # maybe not needed
        point_colors = []
        point_classes = []
        fig_cluster = plt.figure()
        for i in range(num_points):
            # choose random cluster
            cluster_index = random.randint(0, num_clusters - 1)
            point_clusters.append(cluster_index)
            cluster_gaussian = cluster_gaussians[cluster_index]
            color = cluster_gaussian.color
            point_colors.append(color)
            lat, lon = cluster_gaussian.get_point()
            points.append((lat, lon))
            cluster_base_cls = cluster_base_classes[cluster_index]
            cls = class_hierarchy.get_random_subclass_of(cluster_base_cls)
            point_classes.append(cls)
            plt.plot(lat, lon, "o", color=color)

        plt.show()
        fig_cluster.savefig("clustered_points.png")
        answer = input("Keep this random dataset? (y/n)").lower()

        if answer == "y":
            break

    # write dataset to file
    g = Graph()

    g += class_hierarchy.as_graph()

    for i in range(len(points)):
        point = URIRef("http://ex.com/point%03i" % i)
        geometry = URIRef("http://ex.com/geometry%03i" % i)
        lat, lon = points[i]
        cls = point_classes[i]
        cluster = point_clusters[i]

        g.add((point, RDF.type, FEATURE_CLS))
        g.add((point, RDF.type, cls))
        g.add((point, RDFS.comment, Literal(f"Belongs to cluster {cluster}")))
        g.add((point, LAT, Literal(lat, None, XSD.double)))
        g.add((point, LON, Literal(lon, None, XSD.double)))
        g.add((point, HAS_GEOMETRY, geometry))
        g.add((geometry, AS_WKT, Literal(f"POINT({lon} {lat})", None, WKT_TYPE)))

    g.serialize(output_file_path, format="ntriples")


# call example:
if __name__ == "__main__":
    # Dresden area
    lon_min = 13.6301
    lon_max = 13.8615
    lat_min = 50.9815
    lat_max = 51.1158
    generate(100, 50, 4, lat_min, lat_max, lon_min, lon_max, "dataset/dataset.nt")
