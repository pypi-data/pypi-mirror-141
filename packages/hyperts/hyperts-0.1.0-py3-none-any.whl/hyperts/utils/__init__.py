from . import consts
from . import tstoolbox
from . import metrics
from . import transformers
from .tstoolbox import TSToolBox
from ._base import register_tstoolbox, get_tool_box

register_tstoolbox(TSToolBox, None)

try:
    from .dask_ex._ts_toolbox import TSDaskToolBox
    register_tstoolbox(TSDaskToolBox, None)
except ImportError:
    print("Import TSDaskToolBox Error")

try:
    from .cuml_ex._ts_toolbox import TSCumlToolBox
    register_tstoolbox(TSCumlToolBox, None)
except ImportError:
    print("Import TSCumlToolBox Error")


def set_random_state(seed=9527, mode=consts.Mode_STATS):
    import os, random
    import numpy as np

    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    os.environ['TF_DETERMINISTIC_OPS'] = '0'
    np.random.seed(seed)

    if mode != consts.Mode_DL:
        import tensorflow as tf
        tf.random.set_seed(seed)