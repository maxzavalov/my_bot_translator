from data_base.utils.crud_utils import CRUDInteface
from data_base.common.models import db, Profile

db.connect()
db.create_tables([Profile])

crud = CRUDInteface()


