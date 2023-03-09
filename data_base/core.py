from data_base.models import db, Profile

db.connect()
db.create_tables([Profile])




