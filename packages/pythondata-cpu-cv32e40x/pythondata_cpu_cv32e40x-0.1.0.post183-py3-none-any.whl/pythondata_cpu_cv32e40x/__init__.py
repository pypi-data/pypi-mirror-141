import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.1.0.post183"
version_tuple = (0, 1, 0, 183)
try:
    from packaging.version import Version as V
    pversion = V("0.1.0.post183")
except ImportError:
    pass

# Data version info
data_version_str = "0.1.0.post57"
data_version_tuple = (0, 1, 0, 57)
try:
    from packaging.version import Version as V
    pdata_version = V("0.1.0.post57")
except ImportError:
    pass
data_git_hash = "a4829d10977941de1c1bbc73a39e420b81ec9582"
data_git_describe = "0.1.0-57-ga4829d1"
data_git_msg = """\
commit a4829d10977941de1c1bbc73a39e420b81ec9582
Merge: b4edeee d3813b0
Author: Arjan Bink <40633348+Silabs-ArjanB@users.noreply.github.com>
Date:   Fri Mar 4 14:30:04 2022 +0100

    Merge pull request #468 from silabs-halfdan/relative_nmi_address
    
    NMI address update

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
