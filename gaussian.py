import math
import random


class Gaussian:
    def __init__(self, mu_lat, mu_lon, sigma_lat, sigma_lon, angle, color):
        self.mu_lat = mu_lat
        self.mu_lon = mu_lon
        self.sigma_lat = sigma_lat
        self.sigma_lon = sigma_lon
        self.angle_degree = angle
        self.angle = math.radians(angle)
        self.color = color

    def get_point(self):
        lon = random.gauss(self.mu_lon, self.sigma_lon)
        lat = random.gauss(self.mu_lat, self.sigma_lat)

        lon = lon - self.mu_lon
        lat = lat - self.mu_lat

        lon_rotated = \
            (lon * math.cos(self.angle)) - (lat * math.sin(self.angle))
        lat_rotated = \
            (lon * math.sin(self.angle)) + (lat * math.cos(self.angle))

        lon = lon_rotated + self.mu_lon
        lat = lat_rotated + self.mu_lat

        return lon, lat
