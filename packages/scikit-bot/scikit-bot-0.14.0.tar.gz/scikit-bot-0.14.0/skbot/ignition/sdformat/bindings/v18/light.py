from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "sdformat/v1.8/light.xsd"


@dataclass
class Light:
    """
    The light element describes a light source.

    Parameters
    ----------
    cast_shadows: When true, the light will cast shadows.
    intensity: Scale factor to set the relative power of a light.
    diffuse: Diffuse light color
    specular: Specular light color
    attenuation: Light attenuation
    direction: Direction of the light, only applicable for spot and
        directional lights.
    spot: Spot light parameters
    pose: A position (x,y,z) and orientation (roll, pitch yaw) with
        respect   to the frame named in the relative_to attribute.
    name: A unique name for the light.
    type: The light type: point, directional, spot.
    """

    class Meta:
        name = "light"

    cast_shadows: bool = field(
        default=False,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    intensity: float = field(
        default=1.0,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    diffuse: str = field(
        default="1 1 1 1",
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
            "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
        },
    )
    specular: str = field(
        default=".1 .1 .1 1",
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
            "pattern": r"(\s*\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){3}\+?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s*",
        },
    )
    attenuation: Optional["Light.Attenuation"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    direction: str = field(
        default="0 0 -1",
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
            "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){2}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
        },
    )
    spot: Optional["Light.Spot"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    pose: Optional["Light.Pose"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )

    @dataclass
    class Attenuation:
        """
        Light attenuation.

        Parameters
        ----------
        range: Range of the light
        linear: The linear attenuation factor: 1 means attenuate evenly
            over the distance.
        constant: The constant attenuation factor: 1.0 means never
            attenuate, 0.0 is complete attenutation.
        quadratic: The quadratic attenuation factor: adds a curvature to
            the attenuation.
        """

        range: float = field(
            default=10.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        linear: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        constant: float = field(
            default=1.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        quadratic: float = field(
            default=0.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )

    @dataclass
    class Spot:
        """
        Spot light parameters.

        Parameters
        ----------
        inner_angle: Angle covered by the bright inner cone
        outer_angle: Angle covered by the outer cone
        falloff: The rate of falloff between the inner and outer cones.
            1.0 means a linear falloff, less means slower falloff,
            higher means faster falloff.
        """

        inner_angle: float = field(
            default=0.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        outer_angle: float = field(
            default=0.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        falloff: float = field(
            default=0.0,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )

    @dataclass
    class Pose:
        """
        Parameters
        ----------
        value:
        relative_to: If specified, this pose is expressed in the named
            frame. The named frame       must be declared within the
            same scope (world/model) as the element that       has its
            pose specified by this tag.        If missing, the pose is
            expressed in the frame of the parent XML element       of
            the element that contains the pose. For exceptions to this
            rule and       more details on the default behavior, see
            http://sdformat.org/tutorials?tut=pose_frame_semantics.
            Note that @relative_to merely affects an element's initial
            pose and       does not affect the element's dynamic
            movement thereafter.        New in v1.8: @relative_to may
            use frames of nested scopes. In this case,       the frame
            is specified using `::` as delimiter to define the scope of
            the       frame, e.g.
            `nested_model_A::nested_model_B::awesome_frame`.
        """

        value: str = field(
            default="0 0 0 0 0 0",
            metadata={
                "required": True,
                "pattern": r"(\s*(-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+)\s+){5}((-|\+)?(\d+(\.\d*)?|\.\d+|\d+\.\d+[eE][-\+]?[0-9]+))\s*",
            },
        )
        relative_to: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )
