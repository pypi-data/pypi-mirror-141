from arkitekt.structures.registry import get_current_structure_registry
from arkitekt.widgets import *
from .schema import *

structure_reg = get_current_structure_registry()

structure_reg.register_as_structure(
    MultiScaleSampleFragment,
    expand=aexpand_multiscale,
)


structure_reg.register_as_structure(
    MultiScaleRepresentationFragment, expand=aget_multiscale_rep
)
