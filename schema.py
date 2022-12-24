from peewee import SqliteDatabase, Model, TextField, ForeignKeyField, IntegerField, PrimaryKeyField

db = SqliteDatabase("Tester.db")


class BaseTable(Model):
    class Meta:
        database = db


class User(BaseTable):
    user_id = PrimaryKeyField()
    chat_id = IntegerField()
    name = TextField()
    surname = TextField()
    isPlaying = IntegerField()


class Dish(BaseTable):
    dish_id = PrimaryKeyField()
    name = TextField()
    types = TextField()  # _ separates types
    descriptions = TextField()  # _ separates different descriptions


class GameInProgress(BaseTable):
    game_id = PrimaryKeyField()
    user_id = ForeignKeyField(User)
    dish1 = ForeignKeyField(Dish)
    dish1_type = IntegerField()
    dish2 = ForeignKeyField(Dish)
    dish2_type = IntegerField()
    dish3 = ForeignKeyField(Dish)
    dish3_type = IntegerField()
    dish4 = ForeignKeyField(Dish)
    dish4_type = IntegerField()
    dish5 = ForeignKeyField(Dish)
    dish5_type = IntegerField()
    dish6 = ForeignKeyField(Dish)
    dish6_type = IntegerField()
    current_dish = IntegerField()  # numeration from 1 to 6
    score = IntegerField()  # number of times you died


class Reaction(BaseTable):
    dish_type = TextField()
    silver_dust = TextField()
    golden_dust = TextField()
    tripotassium_phosphate = TextField()
    sodium_chloride = TextField()
    oxalic_acid = TextField()
    hydrogen_peroxide = TextField()
    rose = TextField()


class Result(BaseTable):
    result_id = PrimaryKeyField()
    user_id = ForeignKeyField(User)
    highscore = IntegerField()
