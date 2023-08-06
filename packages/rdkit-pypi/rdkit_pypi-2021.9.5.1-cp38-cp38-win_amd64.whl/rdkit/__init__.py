

""""""# start delvewheel patch
def _delvewheel_init_patch_0_0_20():
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'rdkit_pypi.libs'))
    if sys.version_info[:2] >= (3, 8):
        conda_workaround = sys.version_info[:3] < (3, 9, 9) and os.path.exists(os.path.join(sys.base_prefix, 'conda-meta'))
        if conda_workaround:
            # backup the state of the environment variable CONDA_DLL_SEARCH_MODIFICATION_ENABLE
            conda_dll_search_modification_enable = os.environ.get('CONDA_DLL_SEARCH_MODIFICATION_ENABLE')
            os.environ['CONDA_DLL_SEARCH_MODIFICATION_ENABLE'] = '1'
        os.add_dll_directory(libs_dir)
        if conda_workaround:
            # restore the state of the environment variable CONDA_DLL_SEARCH_MODIFICATION_ENABLE
            if conda_dll_search_modification_enable is None:
                os.environ.pop('CONDA_DLL_SEARCH_MODIFICATION_ENABLE', None)
            else:
                os.environ['CONDA_DLL_SEARCH_MODIFICATION_ENABLE'] = conda_dll_search_modification_enable
    else:
        from ctypes import WinDLL
        with open(os.path.join(libs_dir, '.load-order-rdkit_pypi-2021.9.5.1')) as file:
            load_order = file.read().split()
        for lib in load_order:
            WinDLL(os.path.join(libs_dir, lib))


_delvewheel_init_patch_0_0_20()
del _delvewheel_init_patch_0_0_20
# end delvewheel patch

# Need to import rdBase to properly wrap exceptions                                                                                                         #  otherwise they will leak memory 
from . import rdBase

try:
  from .rdBase import rdkitVersion as __version__
except ImportError:
  __version__ = 'Unknown'
  raise

import logging
logger = logging.getLogger("rdkit")
# if we are running in a jupyter notebook, enable the extensions
try:
  kernel_name = get_ipython().__class__.__name__

  if kernel_name == 'ZMQInteractiveShell':
    from rdkit.Chem.Draw import IPythonConsole
    from rdkit.Chem import LogWarningMsg, WrapLogs
    WrapLogs()  
    logger.info("Enabling RDKit %s jupyter extensions"%__version__)
    
except:
  pass
