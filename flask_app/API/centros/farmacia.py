from .centro  import Centro
from ...models import Farmacia as FarmaciaModel
from ...schemas import FarmaciaSchema 

class Farmacia(Centro):
   model = FarmaciaModel
   schema = FarmaciaSchema
