************
Installation
************

Using `pip`
----------

    pip install openmesh

Prebuilt Binaries
-----------------

We provide prebuilt wheels for manual installation with `pip` for the following configurations:

Linux
^^^^^
* `Python 3.9 <https://gitlab.vci.rwth-aachen.de:9000/OpenMesh/openmesh-python/-/jobs/artifacts/master/browse/release?job=deploy-3.9-linux>`_

macOS
^^^^^^^^^^^
* `Python 3.9 X86 <https://gitlab.vci.rwth-aachen.de:9000/OpenMesh/openmesh-python/-/jobs/artifacts/master/browse/release?job=deploy-3.9-macos>`_
* `Python 3.9 ARM64 (M1) <https://gitlab.vci.rwth-aachen.de:9000/OpenMesh/openmesh-python/-/jobs/artifacts/master/browse/release?job=deploy-3.9-macos-m1>`_

Windows
^^^^^^^
* `Python 3.9 <https://gitlab.vci.rwth-aachen.de:9000/OpenMesh/openmesh-python/-/jobs/artifacts/master/browse/release?job=deploy-3.9-VS2017>`_

Building from source
^^^^^^^^^^^^^^^^^^^^
1. recursively clone the repo
2. `cd` to repo dir
3. ensure the correct virtualenv is activated
4. `pip install -e .`

..
    Running the tests
    #################
    
    In your cmake build directory (e.g. build/):
    
    .. code:: python
    
        ctest --verbose
