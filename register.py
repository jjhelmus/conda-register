import os.path
from pprint import pprint

from pip._vendor.distlib.database import DistributionPath
#from distlib.database import DistributionPath

from conda.models.prefix_record import PrefixRecord
from conda.core.linked_data import PrefixData

path = ['/home/jhelmus/anaconda3/envs/pip_test/lib/python3.6/site-packages']
name = 'imagesize'
target_prefix = '/home/jhelmus/anaconda3/envs/pip_test'
short_path = 'lib/python3.6/site-packages'

# find package details using distlib
dist_path = DistributionPath(path, include_egg=True)
dist = dist_path.get_distribution(name)
files = [os.path.join(short_path, p) for p, h, s in dist.list_installed_files()]

# create a conda PrefixRecord
prefix_record = PrefixRecord.from_objects(
    name=dist.name,
    version=dist.version,
    build='frompip_0',
    files=files,
    build_number=0,
)
# TODO: conda currently checks that prefix_record.fn ends with .tar.bz2.
# This check should be supressed for prefix record entries which are not
# derived from tarballs so that prefix_record.fn can be set to None.
prefix_record.fn = prefix_record.fn + '.tar.bz2'
pprint(prefix_record.dump())

print("creating linked package record.")
PrefixData(target_prefix).insert(prefix_record)
