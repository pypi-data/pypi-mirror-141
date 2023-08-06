from pkg_resources import DistributionNotFound, get_distribution

try:
    __version__ = get_distribution("drf_simple-auth-jwt").version
except DistributionNotFound:
    # package is not installed
    __version__ = None