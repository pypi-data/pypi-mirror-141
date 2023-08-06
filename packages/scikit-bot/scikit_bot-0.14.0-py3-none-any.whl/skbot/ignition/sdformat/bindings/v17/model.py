from dataclasses import dataclass, field
from typing import List, Optional
from .joint import Joint
from .link import Link

__NAMESPACE__ = "sdformat/v1.7/model.xsd"


@dataclass
class Model:
    """
    The model element defines a complete robot or any other physical object.

    Parameters
    ----------
    static: If set to true, the model is immovable; i.e., a dynamics
        engine will not       update its position. This will also
        overwrite this model's `@canonical_link`       and instead
        attach the model's implicit frame to the world's implicit frame.
        This holds even if this model is nested (or included) by another
        model       instead of being a direct child of `//world`.
    self_collide: If set to true, all links in the model will collide
        with each other (except those connected by a joint). Can be
        overridden by the link or collision element self_collide
        property. Two links within a model will collide if
        link1.self_collide OR link2.self_collide. Links connected by a
        joint will never collide.
    allow_auto_disable: Allows a model to auto-disable, which is means
        the physics engine can skip updating the model when the model is
        at rest. This parameter is only used by models with no joints.
    include: Include resources from a URI. This can be used to nest
        models.
    model: A nested model element
    enable_wind: If set to true, all links in the model will be affected
        by the wind. Can be overriden by the link wind property.
    frame: A frame of reference in which poses may be expressed.
    pose: A position(x,y,z) and orientation(roll, pitch yaw) with
        respect   to the frame named in the relative_to attribute.
    link: A physical link with inertia, collision, and visual
        properties. A link must be a child of a model, and any number of
        links may exist in a model.
    joint: A joint connects two links with kinematic and dynamic
        properties. By default, the pose of a joint is expressed in the
        child link frame.
    plugin: A plugin is a dynamically loaded chunk of code. It can exist
        as a child of world, model, and sensor.
    gripper:
    name: The name of the model and its implicit frame. This name must
        be unique       among all elements defining frames within the
        same scope, i.e., it must       not match another //model,
        //frame, //joint, or //link within the same       scope.
    canonical_link: The name of the model's canonical link, to which the
        model's implicit       coordinate frame is attached. If unset or
        set to an empty string, the       first `/link` listed as a
        direct child of this model is chosen as the       canonical
        link. If the model has no direct `/link` children, it will
        instead be attached to the first nested (or included) model's
        implicit       frame.
    """

    class Meta:
        name = "model"

    static: bool = field(
        default=False,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    self_collide: bool = field(
        default=False,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    allow_auto_disable: bool = field(
        default=True,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    include: List["Model.Include"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    model: List["Model"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    enable_wind: bool = field(
        default=False,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    frame: List["Model.Frame"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    pose: Optional["Model.Pose"] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )
    link: List[Link] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    joint: List[Joint] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    plugin: List["Model.Plugin"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    gripper: List["Model.Gripper"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    canonical_link: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

    @dataclass
    class Include:
        """Include resources from a URI.

        This can be used to nest models.

        Parameters
        ----------
        uri: URI to a resource, such as a model
        name: Override the name of the included model.
        static: Override the static value of the included model.
        pose: A position(x,y,z) and orientation(roll, pitch yaw) with
            respect   to the frame named in the relative_to attribute.
        plugin: A plugin is a dynamically loaded chunk of code. It can
            exist as a child of world, model, and sensor.
        """

        uri: str = field(
            default="__default__",
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        name: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        static: bool = field(
            default=False,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        pose: Optional["Model.Include.Pose"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
                "required": True,
            },
        )
        plugin: List["Model.Include.Plugin"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass
        class Pose:
            """
            Parameters
            ----------
            value:
            relative_to: If specified, this pose is expressed in the
                named frame. The named frame       must be declared
                within the same scope (world/model) as the element that
                has its pose specified by this tag.        If missing,
                the pose is expressed in the frame of the parent XML
                element       of the element that contains the pose. For
                exceptions to this rule and       more details on the
                default behavior, see
                http://sdformat.org/tutorials?tut=pose_frame_semantics.
                Note that @relative_to merely affects an element's
                initial pose and       does not affect the element's
                dynamic movement thereafter.
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

        @dataclass
        class Plugin:
            """A plugin is a dynamically loaded chunk of code.

            It can exist as a child of world, model, and sensor.

            Parameters
            ----------
            any_element: This is a special element that should not be
                specified in an SDFormat file. It automatically copies
                child elements into the SDFormat element so that a
                plugin can access the data.
            name: A unique name for the plugin, scoped to its parent.
            filename: Name of the shared library to load. If the
                filename is not a full path name, the file will be
                searched for in the configuration paths.
            """

            any_element: List[object] = field(
                default_factory=list,
                metadata={
                    "type": "Wildcard",
                    "namespace": "##any",
                },
            )
            name: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                },
            )
            filename: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                },
            )

    @dataclass
    class Frame:
        """
        A frame of reference in which poses may be expressed.

        Parameters
        ----------
        pose: A position(x,y,z) and orientation(roll, pitch yaw) with
            respect   to the frame named in the relative_to attribute.
        name: Name of the frame. It must be unique whithin its scope
            (model/world),       i.e., it must not match the name of
            another frame, link, joint, or model       within the same
            scope.
        attached_to: If specified, this frame is attached to the
            specified frame. The specified       frame must be within
            the same scope and may be defined implicitly, i.e.,
            the name of any //frame, //model, //joint, or //link within
            the same scope       may be used.        If missing, this
            frame is attached to the containing scope's frame. Within
            a //world scope this is the implicit world frame, and within
            a //model       scope this is the implicit model frame.
            A frame moves jointly with the frame it is @attached_to.
            This is different       from //pose/@relative_to.
            @attached_to defines how the frame is attached       to a
            //link, //model, or //world frame, while //pose/@relative_to
            defines       how the frame's pose is represented
            numerically. As a result, following       the chain of
            @attached_to attributes must always lead to a //link,
            //model, //world, or //joint (implicitly attached_to its
            child //link).
        """

        pose: Optional["Model.Frame.Pose"] = field(
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
        attached_to: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

        @dataclass
        class Pose:
            """
            Parameters
            ----------
            value:
            relative_to: If specified, this pose is expressed in the
                named frame. The named frame       must be declared
                within the same scope (world/model) as the element that
                has its pose specified by this tag.        If missing,
                the pose is expressed in the frame of the parent XML
                element       of the element that contains the pose. For
                exceptions to this rule and       more details on the
                default behavior, see
                http://sdformat.org/tutorials?tut=pose_frame_semantics.
                Note that @relative_to merely affects an element's
                initial pose and       does not affect the element's
                dynamic movement thereafter.
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
            movement thereafter.
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

    @dataclass
    class Plugin:
        """A plugin is a dynamically loaded chunk of code.

        It can exist as a child of world, model, and sensor.

        Parameters
        ----------
        any_element: This is a special element that should not be
            specified in an SDFormat file. It automatically copies child
            elements into the SDFormat element so that a plugin can
            access the data.
        name: A unique name for the plugin, scoped to its parent.
        filename: Name of the shared library to load. If the filename is
            not a full path name, the file will be searched for in the
            configuration paths.
        """

        any_element: List[object] = field(
            default_factory=list,
            metadata={
                "type": "Wildcard",
                "namespace": "##any",
            },
        )
        name: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            },
        )
        filename: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            },
        )

    @dataclass
    class Gripper:
        grasp_check: Optional["Model.Gripper.GraspCheck"] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )
        gripper_link: List[str] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
                "min_occurs": 1,
            },
        )
        palm_link: str = field(
            default="__default__",
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

        @dataclass
        class GraspCheck:
            detach_steps: int = field(
                default=40,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            attach_steps: int = field(
                default=20,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
            min_contact_count: int = field(
                default=2,
                metadata={
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                },
            )
