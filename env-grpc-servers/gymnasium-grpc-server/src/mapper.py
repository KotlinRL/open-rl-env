import Env_pb2
import numpy as np
import gymnasium as gym

from Env_pb2 import (
    DType,
    NDArray,
    BoxSpace,
    Observation,
    DiscreteSpace,
    MultiDiscreteSpace,
    MultiBinarySpace,
    TupleSpace,
    DictSpace,
    Space,
    TupleObservation,
    MapObservation,
    Observation,
    TupleAction,
    MapAction,
    Action,
    Info,
    MakeResponse,
    SpaceRequest,
    SpaceResponse,
    ResetResponse,
    StepResponse,
    Info
)

# === DTYPE MAPPING HELPERS ===
DTYPE_MAPPING = {
    "float32": DType.float32,
    "float64": DType.float64,
    "int32": DType.int32,
    "int64": DType.int64,
    "bool": DType.bool,
    "uint8": DType.uint8,
}

REVERSE_DTYPE_MAPPING = {v: k for k, v in DTYPE_MAPPING.items()}

def get_proto_dtype(np_dtype):
    """
    Map numpy dtype to Protobuf DType.
    """
    dtype_name = np_dtype.name
    if dtype_name not in DTYPE_MAPPING:
        raise ValueError(f"Unsupported numpy dtype: {dtype_name}")
    return DTYPE_MAPPING[dtype_name]

def get_np_dtype(proto_dtype):
    """
    Map Protobuf DType to numpy dtype.
    """
    if proto_dtype not in REVERSE_DTYPE_MAPPING:
        raise ValueError(f"Unsupported Protobuf DType: {proto_dtype}")
    return np.dtype(REVERSE_DTYPE_MAPPING[proto_dtype])

# === NDARRAY CONVERSION HELPERS ===
def ndarray_to_proto(ndarray):
    """
    Convert numpy array to Protobuf NDArray message.
    """
    return NDArray(
        dtype=get_proto_dtype(ndarray.dtype),
        shape=list(ndarray.shape),
        data=ndarray.tobytes(),
    )

def proto_to_ndarray(proto):
    """
    Convert Protobuf NDArray to numpy array.
    """
    dtype = get_np_dtype(proto.dtype)
    return np.frombuffer(proto.data, dtype=dtype).reshape(proto.shape)

# === SPACE MAPPING ===
def gym_space_to_proto(space):
    """
    Convert Gym space to Protobuf Space message.
    """
    if isinstance(space, gym.spaces.Box):
        return Space(
            box=BoxSpace(
                low=ndarray_to_proto(space.low),
                high=ndarray_to_proto(space.high),
                shape=list(space.shape),
                dtype=get_proto_dtype(space.dtype),
            )
        )
    elif isinstance(space, gym.spaces.Discrete):
        return Space(
            discrete=DiscreteSpace(n=space.n, start=getattr(space, "start", 0))
        )
    elif isinstance(space, gym.spaces.MultiDiscrete):
        return Space(
            multidiscrete=MultiDiscreteSpace(nvec=list(space.nvec))
        )
    elif isinstance(space, gym.spaces.MultiBinary):
        return Space(
            multibinary=MultiBinarySpace(n=space.n)
        )
    elif isinstance(space, gym.spaces.Tuple):
        return Space(
            tuple=TupleSpace(
                spaces=[gym_space_to_proto(s) for s in space.spaces]
            )
        )
    elif isinstance(space, gym.spaces.Dict):
        return Space(
            dict=DictSpace(
                spaces={key: gym_space_to_proto(value) for key, value in space.spaces.items()}
            )
        )
    else:
        raise ValueError(f"Unsupported Gym space type: {type(space)}")

def proto_to_gym_space(proto):
    """
    Convert Protobuf Space message to Gym space.
    """
    space_type = proto.WhichOneof("type")
    if space_type == "box":
        box = proto.box
        low = proto_to_ndarray(box.low)
        high = proto_to_ndarray(box.high)
        return gym.spaces.Box(
            low=low, high=high, shape=tuple(box.shape), dtype=get_np_dtype(box.dtype)
        )
    elif space_type == "discrete":
        return gym.spaces.Discrete(n=proto.discrete.n, start=proto.discrete.start)
    elif space_type == "multidiscrete":
        return gym.spaces.MultiDiscrete(nvec=proto.multidiscrete.nvec)
    elif space_type == "multibinary":
        return gym.spaces.MultiBinary(n=proto.multibinary.n)
    elif space_type == "tuple":
        return gym.spaces.Tuple(
            [proto_to_gym_space(s) for s in proto.tuple.spaces]
        )
    elif space_type == "dict":
        return gym.spaces.Dict(
            {key: proto_to_gym_space(value) for key, value in proto.dict.spaces.items()}
        )
    else:
        raise ValueError(f"Unsupported Protobuf space type: {space_type}")

# === OBSERVATION MAPPING ===
def gym_to_proto_observation(obs):
    """
    Convert Gym observation to Protobuf Observation message.
    """
    if isinstance(obs, np.ndarray):
        return Observation(array=ndarray_to_proto(obs))
    elif isinstance(obs, int):
        return Observation(int32=obs)
    elif isinstance(obs, float):
        return Observation(float=obs)
    elif isinstance(obs, str):
        return Observation(string=obs)
    elif isinstance(obs, tuple):
        return Observation(
            tuple=TupleObservation(
                items=[gym_to_proto_observation(item) for item in obs]
            )
        )
    elif isinstance(obs, dict):
        return Observation(
            map=MapObservation(
                items={key: gym_to_proto_observation(value) for key, value in obs.items()}
            )
        )
    else:
        raise ValueError(f"Unsupported observation type: {type(obs)}")

def proto_to_gym_observation(proto):
    """
    Convert Protobuf Observation message to Gym observation.
    """
    field = proto.WhichOneof("value")
    if field == "array":
        return proto_to_ndarray(proto.array)
    elif field == "int32":
        return proto.int32
    elif field == "float":
        return proto.float
    elif field == "string":
        return proto.string
    elif field == "tuple":
        return tuple(proto_to_gym_observation(item) for item in proto.tuple.items)
    elif field == "map":
        return {item.key: proto_to_gym_observation(item.value) for item in proto.map.items}
    else:
        raise ValueError(f"Unsupported Protobuf observation field: {field}")

# === ACTION MAPPING ===
def gym_to_proto_action(action):
    """
    Convert Gym action to Protobuf Action message.
    """
    if isinstance(action, np.ndarray):
        return Action(array=ndarray_to_proto(action))
    elif isinstance(action, int):
        return Action(int32=action)
    elif isinstance(action, float):
        return Action(float=action)
    elif isinstance(action, str):
        return Action(string=action)
    elif isinstance(action, tuple):
        return Action(
            tuple=TupleAction(
                items=[gym_to_proto_action(item) for item in action]
            )
        )
    elif isinstance(action, dict):
        return Action(
            map=MapAction(
                items={key: gym_to_proto_action(value) for key, value in action.items()}
            )
        )
    else:
        raise ValueError(f"Unsupported action type: {type(action)}")

def proto_to_gym_action(proto):
    """
    Convert Protobuf Action message to Gym action.
    """
    field = proto.WhichOneof("value")
    if field == "array":
        return proto_to_ndarray(proto.array)
    elif field == "int32":
        return proto.int32
    elif field == "float":
        return proto.float
    elif field == "string":
        return proto.string
    elif field == "tuple":
        return tuple(proto_to_gym_action(item) for item in proto.tuple.items)
    elif field == "map":
        return {item.key: proto_to_gym_action(item.value) for item in proto.map.items}
    else:
        raise ValueError(f"Unsupported Protobuf action field: {field}")

def gym_to_proto_info(info):
    return Info(data=[Info.DataEntry(key=str(k), value=str(v)) for k, v in info.items()])
