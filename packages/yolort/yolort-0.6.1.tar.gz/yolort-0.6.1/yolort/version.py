__version__ = '0.6.1'
git_version = 'b321ad09b1c904c482a8dba52d9f7abc7e50ef9a'
from torchvision.extension import _check_cuda_version
if _check_cuda_version() > 0:
    cuda = _check_cuda_version()
