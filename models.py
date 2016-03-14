import datetime
import utils

from peewee import *

DATABASE = PostgresqlDatabase('hacktiv8-surl', user='postgres')

class Site(Model):
    url = CharField(unique=True)
    surl = CharField(unique=True)
    pixel_script = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    metadata = TextField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_surl(cls, url, pixel_script):
        return cls.create_or_get(
                url=url,
                surl=utils.generate_surl(url),
                pixel_script=pixel_script,
                metadata=utils.get_metadata(url))

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Site], safe=True)
    DATABASE.close()
