from collections import OrderedDict
from dataclasses import dataclass
from typing import List

import numpy as np
from marshmallow import Schema, fields, post_load

from navability.entities.factor.distributions import Categorical, Distribution


@dataclass
class InferenceType:
    """
    Base type for all factor classes.
    """

    pass


@dataclass
class Prior(InferenceType):
    Z: Distribution

    def __repr__(self):
        return f"<{self.__class__.__name__}(Z={str(self.Z)})>"

    def dump(self):
        return ZSchema().dump(self)

    def dumps(self):
        return ZSchema().dumps(self)

    # TODO: Deserializing this.


class ZSchema(Schema):
    Z = fields.Method("get_Z", "set_Z", required=True)

    class Meta:
        ordered = True

    def get_Z(self, obj):
        return obj.Z.dump()

    def set_Z(self, obj):
        raise Exception("This has not been implemented yet.")

    # @post_load
    # def load(self, data, **kwargs):
    #     return PriorPose2(**data)


@dataclass
class LinearRelative(InferenceType):
    Z: Distribution

    def __repr__(self):
        return f"<{self.__class__.__name__}(Z={str(self.Z)})>"

    def dump(self):
        return ZSchema().dump(self)

    def dumps(self):
        return ZSchema().dumps(self)

    # TODO: Deserializing this.


@dataclass
class PriorPose2(InferenceType):
    Z: Distribution

    def __repr__(self):
        return f"<{self.__class__.__name__}(Z={str(self.Z)})>"

    def dump(self):
        return ZSchema().dump(self)

    def dumps(self):
        return ZSchema().dumps(self)

    # TODO: Deserializing this.


@dataclass
class Pose2Pose2(InferenceType):
    Z: Distribution

    def __repr__(self):
        return f"<{self.__class__.__name__}(Z={str(self.Z)})>"

    def dump(self):
        return ZSchema().dump(self)

    def dumps(self):
        return ZSchema().dumps(self)

    # TODO: Deserializing this.


@dataclass
class Pose2AprilTag4Corners(InferenceType):
    corners: np.ndarray
    homography: np.ndarray
    K: np.ndarray
    taglength: float
    id: int
    _type: str = "/application/JuliaLang/PackedPose2AprilTag4Corners"

    def dump(self):
        return Pose2AprilTag4CornersSchema().dump(self)

    def dumps(self):
        return Pose2AprilTag4CornersSchema().dumps(self)

    # TODO: Deserializing this.


class Pose2AprilTag4CornersSchema(Schema):
    corners = fields.List(fields.Float, required=True)
    homography = fields.List(fields.Float, required=True)
    K = fields.List(fields.Float, required=True)
    taglength = fields.Float(required=True)
    id = fields.Int(required=True)
    _type = fields.String(default="/application/JuliaLang/PackedPose2AprilTag4Corners")

    class Meta:
        ordered = True

    @post_load
    def marshal(self, data, **kwargs):
        return Pose2AprilTag4Corners(**data)


@dataclass
class Mixture(InferenceType):
    mechanics: type
    components: "OrderedDict[str, Distribution]"
    diversity: Categorical
    dims: int  # Internal factor dimensions

    def __init__(
        self,
        mechanics: type,
        components: "OrderedDict[str, Distribution]",
        probabilities: List[float],
        dims,
    ):
        """Create a Mixture factor type with an underlying factor type, a named set of
         distributions that should be mixed, the probabilities of each distribution
        (the mix), and the dimensions of the underlying factor (e.g.
        ContinuousScalar=1, Pose2Pose2=3, etc.).

        Args:
            mechanics (type): The underlying factor type.
            components (OrderedDict[Distribution]): The named set of distributions that
            should be mixed, e.g. probabilities (List[float]): The probabilities of each
            distribution (the mix)
            dims (int): The dimensions of the
        """  # noqa: E501, B950
        self.mechanics = mechanics
        self.components = components
        self.diversity = Categorical(probabilities)
        self.dims = dims

    def dump(self):
        return MixtureSchema().dump(self)

    def dumps(self):
        return MixtureSchema().dumps(self)

    # TODO: Deserializing this.


class MixtureSchema(Schema):
    N = fields.Method("get_N")
    # TODO: Need to deserialize these at some point in the future.
    F_ = fields.Method("get_F_")
    S = fields.Method("get_S")
    components = fields.Method("get_components")
    diversity = fields.Method("get_diversity")

    class Meta:
        ordered = True

    def get_N(self, obj):
        return len(obj.components)

    def get_F_(self, obj):
        # Not certain this is correct, we will need to validate as we use it.
        return f"Packed{obj.mechanics.__name__}"

    def get_S(self, obj):
        return list(obj.components.keys())

    def get_components(self, obj):
        return list(c.dump() for c in obj.components.values())

    def get_diversity(self, obj):
        return obj.diversity.dump()

    @post_load
    def marshal(self, data, **kwargs):
        return Mixture(**data)
