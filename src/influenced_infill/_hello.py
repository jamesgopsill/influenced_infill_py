from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .influenced_infill_generator import InfluencedInfillGenerator
    
def hello(self: InfluencedInfillGenerator):
    print("world")