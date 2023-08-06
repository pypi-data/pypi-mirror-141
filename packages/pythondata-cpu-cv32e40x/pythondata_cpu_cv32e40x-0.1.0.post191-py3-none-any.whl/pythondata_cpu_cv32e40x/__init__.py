import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.1.0.post191"
version_tuple = (0, 1, 0, 191)
try:
    from packaging.version import Version as V
    pversion = V("0.1.0.post191")
except ImportError:
    pass

# Data version info
data_version_str = "0.1.0.post65"
data_version_tuple = (0, 1, 0, 65)
try:
    from packaging.version import Version as V
    pdata_version = V("0.1.0.post65")
except ImportError:
    pass
data_git_hash = "f6656cd080d70c1288ae7fa2be6e20d44d98d890"
data_git_describe = "0.1.0-65-gf6656cd"
data_git_msg = """\
commit f6656cd080d70c1288ae7fa2be6e20d44d98d890
Merge: 44dbee6 86e2ab1
Author: silabs-oysteink <66771756+silabs-oysteink@users.noreply.github.com>
Date:   Tue Mar 8 11:01:06 2022 +0100

    Merge pull request #473 from Silabs-ArjanB/ArjanB_nmivec
    
    Removed mention of deprecated nmi_addr_i signal from user manual. Def…

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
