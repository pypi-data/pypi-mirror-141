# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['incdbscan', 'incdbscan.tests']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.5.1,<3.0.0',
 'numpy>=1.20.3,<2.0.0',
 'scikit-learn>=1.0,<2.0',
 'sortedcontainers>=2.4.0,<3.0.0',
 'xxhash>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'incdbscan',
    'version': '0.1.0',
    'description': 'Implementation of IncrementalDBSCAN clustering.',
    'long_description': '# IncrementalDBSCAN\n\n`incdbscan` is an implementation of IncrementalDBSCAN, the incremental version of the DBSCAN clustering algorithm.\n\nIncrementalDBSCAN lets the user update the clustering by inserting or deleting data points. The algorithm yields the same result as DBSCAN but without reapplying DBSCAN to the modified data set.\n\nThus, IncrementalDBSCAN is ideal to use when the size of the data set to cluster is so large that applying DBSCAN to the whole data set would be costly but for the purpose of the application it is enough to update an already existing clustering by inserting or deleting some data points.\n\nThe implementation is based on the following paper. To see what\'s new compared to the paper, jump to [Notes on the IncrementalDBSCAN paper](https://github.com/DataOmbudsman/incdbscan/blob/master/notes/notes-on-paper.md).\n\n> Ester, Martin; Kriegel, Hans-Peter; Sander, Jörg; Wimmer, Michael; Xu, Xiaowei (1998). *Incremental Clustering for Mining in a Data Warehousing Environment.* In: Proceedings of the 24rd International Conference on Very Large Data Bases (VLDB 1998).\n\n<p align="center">\n  <img src="./images/illustration_circles.gif" alt="indbscan illustration">\n</p>\n\n## Table of Contents\n\n- [Highlights](#Highlights)\n- [Installation](#installation)\n- [Usage](#usage)\n- [Performance](#Performance)\n\n## Highlights\n\nThe `incdbscan` package is an implementation of the IncrementalDBSCAN algorithm by Ester et al., with about 40 unit tests covering diverse cases, and with [additional corrections](https://github.com/DataOmbudsman/incdbscan/blob/master/notes/notes-on-paper.md) to the original paper.\n\n## Installation\n\n`incdbscan` is on PyPI, and can be installed with `pip`:\n```\npip install incdbscan\n```\n\nThe package requires at least Python 3.7.1.\n\n## Usage\n\nThe algorithm is implemented in the `IncrementalDBSCAN` class.\n\nThere are 3 methods to use:\n- `insert` for inserting data points into the clustering\n- `delete` for deleting data points from the clustering\n- `get_cluster_labels` for obtaining cluster labels\n\nAll methods take a batch of data points in the form of an array of shape `(n_samples, n_features)` (similar to the `scikit-learn` API).\n\n```python\nfrom sklearn.datasets import load_iris\nX = load_iris()[\'data\']\nX_1, X_2 = X[:100], X[100:]\n\nfrom incdbscan import IncrementalDBSCAN\nclusterer = IncrementalDBSCAN(eps=0.5, min_pts=5)\n\n# Insert 1st batch of data points and get their labels\nclusterer.insert(X_1)\nlabels_part1 = clusterer.get_cluster_labels(X_1)\n\n# Insert 2nd batch and get labels of all points in a one-liner\nlabels_all = clusterer.insert(X_2).get_cluster_labels(X)\n\n# Delete 1st batch and get labels for 2nd batch\nclusterer.delete(X_1)\nlabels_part2 = clusterer.get_cluster_labels(X_2)\n```\n\nFor a longer description of usage check out the [notebook](https://github.com/DataOmbudsman/incdbscan/blob/master/notebooks/incdbscan-usage.ipynb) developed just for that!\n\n## Performance\n\nPerformance has two components: insertion and deletion cost.\n\n<p align="left">\n  <img src="./images/performance.png" alt="indbscan performance">\n</p>\n\nThe cost of **inserting** a new data point into IncrementalDBSCAN is quite small and **grows slower** than the cost of applying (`scikit-learns`\'s) DBSCAN to a whole data set.  In other words, *given that* we have a data set _D_ clustered with IncrementalDBSCAN, and we want to see which cluster would a new object _P_ belong to, it is faster to insert _P_ into the current IncrementalDBSCAN clustering than to apply DBSCAN to the union of _D_ and _P_.\n\nThe cost of **deleting** a data point from IncrementalDBSCAN **grows faster** than the cost of applying (`scikit-learns`\'s) DBSCAN to the data set minus that data point. Thus, the cost of deletion in IncrementalDBSCAN is quite small below a certain data set size, but becomes larger as data set size grows.\n\nThese results do not imply that it is very efficient to cluster a whole data set with a series of IncrementalDBSCAN insertions. If we measure the time to cluster a data set with DBSCAN versus to cluster the data by adding the data points one by one to IncrementalDBSCAN, IncrementalDBSCAN will be slower compared to DBSCAN. A typical performance number is that clustering 8,000 data points takes about 10-20 seconds with this implementation.\n\nSee [this notebook](https://github.com/DataOmbudsman/incdbscan/blob/master/notebooks/performance.ipynb) about performance for more details.\n\n### Known shortcomings\n\n- **Batch insertion**: In the current implementation batch insertion of data points is not efficient, since pairwise distances between new points and existing points are not calculated with matrix multiplication.\n- **Deletion**: Data point deletion can take long in big data sets (big clusters), because there is a graph traversal step that can take long. Whether this can be sped up is not clear. \n',
    'author': 'Arpad Fulop',
    'author_email': 'data.ombudsman@tutanota.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DataOmbudsman/incdbscan',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
