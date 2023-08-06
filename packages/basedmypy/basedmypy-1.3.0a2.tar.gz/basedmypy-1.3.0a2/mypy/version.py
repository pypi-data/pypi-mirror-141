import os

from mypy import git

# Base version.
# - Release versions have the form "0.NNN".
# - Dev versions have the form "0.NNN+dev" (PLUS sign to conform to PEP 440).
# - For 1.0 we'll switch back to 1.2.3 form.
__version__ = '0.940+dev'
base_version = __version__

# tuple[major, minor, patch, releaselevel, mypy version, mypy releaselevel, hash]
__based_version_info__ = (
    1,
    3,
    0,
    "alpha",
    __version__.split("+dev")[0],
    "dev" if "+dev" in __version__ else "release",
    None,
)

__based_version__ = "1.3.0a2"

mypy_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
if __based_version_info__[3] == 'dev' and git.is_git_repo(mypy_dir) and git.have_git():
    __based_version__ += '+dev.' + git.git_revision(mypy_dir).decode('utf-8')
    if git.is_dirty(mypy_dir):
        __based_version__ += '.dirty'
del mypy_dir
