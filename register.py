# TODO
# * find all un-tracked dists
# * proper CLI

import os.path

try:
    from distlib.database import DistributionPath
except:
    from pip._vendor.distlib.database import DistributionPath

from conda.models.prefix_record import PrefixRecord
try:
    from conda.core.prefix_data import PrefixData
except:
    from conda.core.linked_data import PrefixData


DEFAULT_BUILD_NUMBER = 0
DEFAULT_BUILD_STR = 'frompip_0'


# TODO set these from the command line
pip_pkg_name = 'imagesize'
target_prefix = '/home/jhelmus/anaconda3/envs/pip_test'
sp_short_path = 'lib/python3.6/site-packages'
sp_full_path = os.path.join(target_prefix, sp_short_path)

# find package details using distlib
dist_path = DistributionPath([sp_full_path, ], include_egg=True)
dist = dist_path.get_distribution(pip_pkg_name)

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

print("creating linked package record for %s." % pip_pkg_name)
PrefixData(target_prefix).insert(prefix_record)
