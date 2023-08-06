from .PyReplayBuffer import (ReplayBuffer,PrioritizedReplayBuffer,
                             MPReplayBuffer, MPPrioritizedReplayBuffer,
                             SelectiveReplayBuffer, ReverseReplayBuffer)

from .LaBER import LaBERmean, LaBERlazy, LaBERmax
from .HER import HindsightReplayBuffer

from .PyReplayBuffer import create_buffer, train

try:
    from .util import create_env_dict, create_before_add_func
except ImportError:
    # If gym is not installed, util functions are not defined.
    pass
