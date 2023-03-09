from datetime import datetime
import peewee as pw

db = pw.SqliteDatabase('BotUsers.db')


class ModelBase(pw.Model):
    created_at = pw.DateField(default=datetime.now())

    class Meta:
        database = db


class Profile(ModelBase):
    user_id = pw.TextField()
    langs = pw.TextField()
    cur_lang = pw.TextField()
