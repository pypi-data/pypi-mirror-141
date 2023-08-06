__version__ = '0.12.0'
git_version = '2662797414e18c350c83817d5b712bd0c0c2c52a'
from torchvision.extension import _check_cuda_version
if _check_cuda_version() > 0:
    cuda = _check_cuda_version()
