from .centro  import Centro
from ...models import FarmaciaHospitalaria as FarmaciaHospitalariaModel
from ...schemas import FarmaciaHospitalariaSchema 

class FarmaciaHospitalaria(Centro):
   model = FarmaciaHospitalariaModel
   schema = FarmaciaHospitalariaSchema
