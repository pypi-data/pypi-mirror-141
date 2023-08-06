import os.path
__dir__ = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
data_location = os.path.join(__dir__, "system_verilog")
src = "https://github.com/openhwgroup/cv32e40x"

# Module version
version_str = "0.1.0.post185"
version_tuple = (0, 1, 0, 185)
try:
    from packaging.version import Version as V
    pversion = V("0.1.0.post185")
except ImportError:
    pass

# Data version info
data_version_str = "0.1.0.post59"
data_version_tuple = (0, 1, 0, 59)
try:
    from packaging.version import Version as V
    pdata_version = V("0.1.0.post59")
except ImportError:
    pass
data_git_hash = "6be51b7052888cad2f278b5fdbc9945e5b8b22cf"
data_git_describe = "0.1.0-59-g6be51b7"
data_git_msg = """\
commit 6be51b7052888cad2f278b5fdbc9945e5b8b22cf
Merge: a4829d1 9667651
Author: Arjan Bink <40633348+Silabs-ArjanB@users.noreply.github.com>
Date:   Mon Mar 7 17:47:54 2022 +0100

    Merge pull request #469 from silabs-halfdan/doc_deprecated_parameter
    
    Document USE_DEPRECATED_FEATURE_SET

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
