"""
Manage n-dimensional coordinate transformations via directed graphs.

``skbot.transform`` allows you to change the representation of a vector from one
coordinate system to another, i.e., it transforms the basis of the vector.
Contrary to similar libraries, this is not limited to 3D or affine
transformations, but can transform in N dimensions and between different
dimensions, too. Additionally, you can create chains - more precisely directed
graphs - of transformations between different frames, which allows you to
express quite complicated transformations.

If you come from a robotics background, this module is analogous to ROS tf2,
but works in (and between) n-dimensions. This means it naturally includes
projections, e.g. world space to pixel space, and it allows you to use more
esoteric transformations like spherical coordinates, too.


Examples
--------

>>> import skbot.transform as tf
>>> import numpy as np

Forward kinematics on a 1 DoF robot arm in 2D

>>> # setup of the arm
>>> link = tf.Translation((1, 0))
>>> joint = tf.Rotation((1, 0), (0, 1))
>>> tool_frame = tf.Frame(2)
>>> joint_frame = link(tool_frame)
>>> world = joint(joint_frame)
>>> joint.angle = 0
>>> # FK of initial position
>>> tool_pos = tool_frame.transform((0, 0), to_frame=world)
>>> assert np.allclose(tool_pos, (1, 0))
>>> # Set new joint angle and compute new FK
>>> joint.angle = np.pi / 2
>>> tool_pos = tool_frame.transform((0, 0), to_frame=world)
>>> assert np.allclose(tool_pos, (0, 1))

Base Elements
-------------

.. autosummary::
    :template: transform_class.rst
    :toctree:

    Frame
    Link

Available Transformations
-------------------------

.. rubric:: nD Links

.. autosummary::
    :template: transform_class.rst
    :toctree:

    AffineSpace
    Translation
    Rotation
    PerspectiveProjection

.. rubric:: 3D Links

.. autosummary::
    :template: transform_class.rst
    :toctree:

    EulerRotation
    QuaternionRotation
    RotvecRotation
    FrustumProjection
    RotationalJoint
    PrismaticJoint

.. rubric:: 2D Links

.. autosummary::
    :template: transform_class.rst
    :toctree:

    Rotation2D
    AngleJoint
    AxialHexagonTransform
    HexagonAxisRound

.. rubric:: Other Links

.. autosummary::
    :template: transform_class.rst
    :toctree:

    CustomLink
    CompundLink
    InvertLink

Joints
------

Joints are a special subclass of links. On top of normal links, they are bounded, i.e. they have
an ``upper_limit`` and a ``lower_limit``, and their value can be accessed by the common name ``param``.
For example::

    import skbot.transform as tf
    import numpy as np

    joint = tf.AngleJoint()
    assert joint.param == joint.angle
    assert joint.lower_limit == 0
    assert joint.upper_limit == 2 * np.pi

    # setting param affects the angle
    joint.param = np.pi
    assert joint.angle == np.pi

.. rubric:: Available Joints

.. autosummary::
    
    RotationalJoint
    PrismaticJoint
    AngleJoint

.. rubric:: Custom Joints

You can create your own joints by inheriting from :class:`tf.Link
<skbot.transform.Link>` (to make the class a link) and from ``tf.Joint`` (to
mark the class as a joint)::

    class CustomJoint(tf.Link, tf.Joint):
        ...

        # Make sure to implement the required properties: 
        # param, lower_limit, upper_limit
        # and to implement a setter for param


Functions
---------

.. autosummary::
    :toctree:

    simplify_links


"""

from .base import (
    Frame,
    Link,
    CustomLink,
    InvertLink,
    CompundLink,
)

from .functions import (
    # basic transformations
    translate,
    rotate,
    reflect,
    shear,
    scale,
)

from .affine import Translation, Rotation, Inverse, AffineSpace
from .projections import PerspectiveProjection
from .utils3d import (
    FrustumProjection,
    EulerRotation,
    QuaternionRotation,
    RotvecRotation,
)
from .joints import RotationalJoint, PrismaticJoint, AngleJoint, Joint
from .utils2d import AxialHexagonTransform, Rotation2D, HexagonAxisRound

from . import metrics
from .simplfy import simplify_links

__all__ = [
    # Core Classes for Frame Management
    "Frame",
    "metrics",  # transform chain metrics
    "Link",
    # nD Links
    "AffineSpace",
    "Rotation",
    "Translation",
    "PerspectiveProjection",
    # 2D Links
    "AngleJoint",
    "AxialHexagonTransform",
    "Rotation2D",
    "HexagonAxisRound",
    # 3D Links
    "EulerRotation",
    "QuaternionRotation",
    "RotationalJoint",
    "PrismaticJoint",
    "RotvecRotation",
    "FrustumProjection",
    # Other Links
    "CustomLink",
    "InvertLink",
    "CompundLink",
    "Inverse",
    "Joint",
    # basic transformation functions
    "translate",
    "rotate",
    "reflect",
    "shear",
    "scale",
    "simplify_links",
]
