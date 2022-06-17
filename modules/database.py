"""
    @Author: ImYrS Yang
    @Date: 2022/6/17
    @Copyright: ImYrS Yang
    @Description: 
"""

from peewee import *

from config import db_name


db = SqliteDatabase(db_name)


class BaseModel(Model):
    class Meta:
        database = db


class Token(BaseModel):
    id = PrimaryKeyField()
    token = TextField()
    created_at = IntegerField()
