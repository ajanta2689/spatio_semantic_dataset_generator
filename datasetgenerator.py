import random

import matplotlib.pyplot as plt

from classhierarchy import ClassHierarchyGenerator
from gaussian import Gaussian


def generate(
        num_points: int,
        num_classes: int,
        num_clusters: int,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float):

    class_hierarchy_genertor = \
        ClassHierarchyGenerator(num_classes, num_clusters)

    class_hierarchy = class_hierarchy_genertor.get_random_hierarchy()

    cluster_base_classes = \
        class_hierarchy.get_direct_subclasses(class_hierarchy.T)

    dist_lat = lat_max - lat_min
    dist_lon = lon_max - lon_min

    cluster_gaussians = []

    colors = list(plt.colormaps.get('Paired').colors)
    assert num_clusters <= len(colors)
    random.shuffle(colors)

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

    for i in range(num_points):
        # choose random cluster
        cluster_index = random.randint(0, num_clusters-1)
        point_clusters.append(cluster_index)
        cluster_gaussian = cluster_gaussians[cluster_index]
        color = cluster_gaussian.color
        point_colors.append(color)
        lat, lon = cluster_gaussian.get_point()
        points.append((lat, lon))
        plt.plot(lat, lon, 'o', color=color)

    plt.show()


if __name__ == '__main__':
    # Dresden area
    lon_min = 13.6301
    lon_max = 13.8615
    lat_min = 50.9815
    lat_max = 51.1158

    generate(100, 50, 4, lat_min, lat_max, lon_min, lon_max)
