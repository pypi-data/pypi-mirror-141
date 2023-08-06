from typing import Callable, Tuple, Mapping, Any
import uuid
import random
from inspect import getsource
import json
from loguru import logger

def uuid_from_seed(seed):
    rd = random.Random()
    rd.seed(seed)

    return uuid.UUID(int=rd.getrandbits(128))

Args = Tuple[Any, ...]
Kwargs = Mapping[str, Any]
Transform = Callable[[Any], str]
ArgIds = Mapping[int, Transform]
KwargIds = Mapping[str, Transform]

def transform_sequence(sequence, key_transforms):
    for key, transform in key_transforms:
        sequence[key] = transform(sequence[key])
    
    return sequence

class NotSerializable(Exception):
    pass

def serializable(value, debug_key=None):
    if debug_key is None:
        debug_key = str(value)

    try:
        value = json.dumps(value)
        return value
    except:
        logger.debug(f"Not json serializable {debug_key}")

    try:
        value = str(value)
    except:
        logger.error(f"Could not serialize {debug_key}")
        raise NotSerializable(f"Object not serializable {debug_key}")

    return value


def serialize_sequence(sequence, keys):
    for key in keys:
        sequence[key] = serializable(sequence[key], debug_key=f"{sequence.__name__}:{key}")

    return sequence
        

def uuid_from_func(
    func: Callable, 
    args: Args, 
    kwargs: Kwargs, 
    arg_ids: ArgIds, 
    kwarg_ids: KwargIds,
    metadata: str = ''
):
    args = list(tuple)
    kwargs = kwargs.copy()

    # transform parameters to json serializable based on user specification

    args = transform_sequence(args, arg_ids.items())
    kwargs = transform_sequence(kwargs, kwarg_ids.items())

    # transform parameters to json serializable based on object str
    
    args = serialize_sequence(args, range(len(args)))
    kwargs = serialize_sequence(kwargs, kwargs.keys())

    id_metadata = {
        'func': getsource(func),
        'args': args,
        'kwargs': kwargs,
        'metadata': metadata
    }

    id_metadata_serialized = json.dumps(id_metadata)

    return uuid_from_seed(id_metadata_serialized)
