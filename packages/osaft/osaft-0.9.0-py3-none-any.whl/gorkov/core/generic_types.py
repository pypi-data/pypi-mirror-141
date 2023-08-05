from typing import Union

from gorkov.core.fluids import InviscidFluid, ViscoelasticFluid, ViscousFluid

t_fluid = Union[InviscidFluid, ViscousFluid, ViscoelasticFluid]
