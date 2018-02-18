# TODO
# * find all un-tracked dists
# * proper CLI

import os.path

try:
    from distlib.database import DistributionPath
except:
    from pip._vendor.distlib.database import DistributionPath

from conda.models.prefix_record import PrefixRecord
from conda.core.link import UnlinkLinkTransaction
from conda.common.path import get_python_site_packages_short_path
try:
    from conda.core.prefix_data import PrefixData
except:
    from conda.core.linked_data import PrefixData

DEFAULT_BUILD_NUMBER = 0
DEFAULT_BUILD_STR = 'frompip_0'


def register_dist(dist_name, target_prefix):
    """ register a distribution with conda. """

    # build path to site-packages directory
    get_python_version = UnlinkLinkTransaction.get_python_version
    python_ver = get_python_version(target_prefix, [], [])
    sp_short_path = get_python_site_packages_short_path(python_ver)
    sp_full_path = os.path.join(target_prefix, sp_short_path)

    # find package details using distlib
    dist_path = DistributionPath([sp_full_path, ], include_egg=True)
    dist = dist_path.get_distribution(dist_name)

    # create a conda PrefixRecord
    files = [os.path.join(sp_short_path, file_path)
             for file_path, file_hash, file_size in dist.list_installed_files()]
    prefix_record = PrefixRecord.from_objects(
        name=dist.name,
        version=dist.version,
        files=files,
        build=DEFAULT_BUILD_STR,
        build_number=DEFAULT_BUILD_NUMBER,
    )
    # TODO: conda currently checks that prefix_record.fn ends with .tar.bz2.
    # This check should be supressed for prefix record entries which are not
    # derived from tarballs so that prefix_record.fn can be set to None.
    prefix_record.fn = prefix_record.fn + '.tar.bz2'

    print("creating linked package record for %s." % dist_name)
    PrefixData(target_prefix).insert(prefix_record)


if __name__ == "__main__":
    # TODO set these from the command line
    dist_name = 'imagesize'
    target_prefix = '/home/jhelmus/anaconda3/envs/pip_test'
    register_dist(dist_name, target_prefix)
