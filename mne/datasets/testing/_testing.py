# Authors: Alexandre Gramfort <alexandre.gramfort@telecom-paristech.fr>
#          Martin Luessi <mluessi@nmr.mgh.harvard.edu>
#          Eric Larson <larson.eric.d@gmail.com>
# License: BSD Style.

import numpy as np

from ...utils import verbose, get_config
from ...fixes import partial
from ..utils import (has_dataset, _data_path, _data_path_doc,
                     _get_version, _version_doc)


has_testing_data = partial(has_dataset, name='testing')
has_spm_data = partial(has_dataset, name='spm')


@verbose
def data_path(path=None, force_update=False, update_path=True,
              download=True, verbose=None):
    # Make sure we don't do something stupid
    if download and \
            get_config('MNE_SKIP_TESTING_DATASET_TESTS', 'false') == 'true':
        raise RuntimeError('Cannot download data if skipping is forced')
    return _data_path(path=path, force_update=force_update,
                      update_path=update_path, name='testing',
                      download=download)

data_path.__doc__ = _data_path_doc.format(name='testing',
                                          conf='MNE_DATASETS_TESTING_PATH')


def get_version():
    return _get_version('testing')

get_version.__doc__ = _version_doc.format(name='testing')


# Allow forcing of testing dataset skip (for Debian tests) using:
# `make test-no-testing-data`
def _skip_testing_data():
    skip_testing = (get_config('MNE_SKIP_TESTING_DATASET_TESTS', 'false') ==
                    'true')
    skip = skip_testing or not has_testing_data()
    return skip

requires_testing_data = np.testing.dec.skipif(_skip_testing_data,
                                              'Requires testing dataset')


def _skip_spm_data():
    skip_testing = (get_config('MNE_SKIP_TESTING_DATASET_TESTS', 'false') ==
                    'true')
    skip = skip_testing or not has_spm_data()
    return skip

requires_spm_data = np.testing.dec.skipif(_skip_spm_data,
                                          'Requires spm dataset')
