import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.1.0.post189"
version_tuple = (0, 1, 0, 189)
try:
    from packaging.version import Version as V
    pversion = V("0.1.0.post189")
except ImportError:
    pass

# Data version info
data_version_str = "0.1.0.post63"
data_version_tuple = (0, 1, 0, 63)
try:
    from packaging.version import Version as V
    pdata_version = V("0.1.0.post63")
except ImportError:
    pass
data_git_hash = "44dbee68ad28de87e080ffda0f790cf03d568a1a"
data_git_describe = "0.1.0-63-g44dbee6"
data_git_msg = """\
commit 44dbee68ad28de87e080ffda0f790cf03d568a1a
Merge: a4264f1 7b5b545
Author: silabs-oysteink <66771756+silabs-oysteink@users.noreply.github.com>
Date:   Tue Mar 8 09:54:56 2022 +0100

    Merge pull request #471 from Silabs-ArjanB/ArjanB_obiv14
    
    Changed SMCLIC_ID_WIDTH default to 5

"""

# Tool version info
tool_version_str = "0.0.post126"
tool_version_tuple = (0, 0, 126)
try:
    from packaging.version import Version as V
    ptool_version = V("0.0.post126")
except ImportError:
    pass


def data_file(f):
    """Get absolute path for file inside pythondata_cpu_cv32e40x."""
    fn = os.path.join(data_location, f)
    fn = os.path.abspath(fn)
    if not os.path.exists(fn):
        raise IOError("File {f} doesn't exist in pythondata_cpu_cv32e40x".format(f))
    return fn
