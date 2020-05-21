#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import logging
import os
import random

from sqlalchemy.sql import text

import db
import settings
from db.models import SQLAlchemyBase, User, GenereEnum, UserToken, Favour, EventTypeEnum, Opinion, FavourTypeEnum
from settings import DEFAULT_LANGUAGE

# LOGGING
mylogger = logging.getLogger(__name__)
settings.configure_logging()


def execute_sql_file(sql_file):
    sql_folder_path = os.path.join(os.path.dirname(__file__), "sql")
    sql_file_path = open(os.path.join(sql_folder_path, sql_file), encoding="utf-8")
    sql_command = text(sql_file_path.read())
    db_session.execute(sql_command)
    db_session.commit()
    sql_file_path.close()


if __name__ == "__main__":
    settings.configure_logging()

    db_session = db.create_db_session()

    # -------------------- REMOVE AND CREATE TABLES --------------------
    mylogger.info("Removing database...")
    SQLAlchemyBase.metadata.drop_all(db.DB_ENGINE)
    mylogger.info("Creating database...")
    SQLAlchemyBase.metadata.create_all(db.DB_ENGINE)




    # -------------------- CREATE USERS --------------------
    mylogger.info("Creating default users...")
    # noinspection PyArgumentList
    user_admin = User(
        created_at=datetime.datetime(2020, 1, 1, 0, 1, 1),
        username="admin",
        email="admin@damcore.com",
        name="Administrator",
        surname="DamCore",
        genere=GenereEnum.male,
    )
    user_admin.set_password("DAMCoure")

    # noinspection PyArgumentList
    user_1= User(
        created_at=datetime.datetime(2020, 1, 1, 0, 1, 1),
        username="usuari1",
        email="usuari1@gmail.com",
        name="usuari",
        surname="1",
        birthdate=datetime.datetime(1989, 1, 1),
        genere=GenereEnum.male,
        stars = 1.3,
        favoursDone=23,
        location= "08700 Catalunya, Igualada"

    )
    user_1.set_password("asdasd1")
    user_1.tokens.append(UserToken(token="656e50e154865a5dc469b80437ed2f963b8f58c8857b66c9bf"))

    # noinspection PyArgumentList
    user_2 = User(
        created_at=datetime.datetime(2020, 1, 1, 0, 1, 1),
        username="user2",
        email="user2@gmail.com",
        name="user",
        surname="2",
        birthdate=datetime.datetime(2017, 1, 1),
        genere=GenereEnum.male,
    )
    user_2.set_password("r45tgt")
    user_2.tokens.append(UserToken(token="0a821f8ce58965eadc5ef884cf6f7ad99e0e7f58f429f584b2"))

    db_session.add(user_admin)
    db_session.add(user_1)
    db_session.add(user_2)
    db_session.commit()

    # -------------------- CREATE FAVOURS --------------------
    mylogger.info("Creating default favours...")


    tags = ["Necessito ajuda en ", "Ofereixo ajuda en "]
    tasks = ["jardineria", "informatica", "cuina", "montar mobles", "llimpiar el pis"]
    amount = [5,10,15,20,25,30,35,30,50]
    start_lat = 41.000000
    stop_lat = 42.000000
    start_lon = 1.20000
    stop_lon = 2.200000



    for i in range (32):
        type = random.choice(list(FavourTypeEnum))
        if type == FavourTypeEnum.necessito:
            name = tags[0] + random.choice(list(tasks))
        else:
            name = tags[1] + random.choice(list(tasks))

        favour = Favour(
            user="usuari1",
            category=random.choice(list(EventTypeEnum)),
            type=type,
            name = name,
            desc="Lore ipsum hemini hemono",
            amount=random.choice(list(amount)),
            owner_id=3,
            latitude= random.uniform(start_lat, stop_lat),
            longitude = random.uniform(start_lon, stop_lon)
        )
        db_session.add(favour)
    db_session.commit()

    favour1 = Favour(
        user="usuari1",
        category=EventTypeEnum.favourxfavour,
        name="Favor1",
        desc="heyyyyyyyyyyyyyy",
        amount=10,
        type=FavourTypeEnum.necessito,
        selected_id=1,
        owner_id=2,
        latitude=random.uniform(start_lat, stop_lat),
        longitude=random.uniform(start_lon, stop_lon)
    )

    favour2 = Favour(
        user="usuari1",
        category=EventTypeEnum.reparation,
        name="Favor2",
        desc="Lore ipsum hemini hemono",
        amount=10,
        type=FavourTypeEnum.necessito,
        owner_id=3,
        selected_id=1,
        latitude=random.uniform(start_lat, stop_lat),
        longitude=random.uniform(start_lon, stop_lon)
    )
    favour3 = Favour(
        user="usuari2",
        category=EventTypeEnum.others,
        name="Favor1",
        desc="Hey this is a example text lelelel",
        amount=10,
        type=FavourTypeEnum.necessito,
        owner_id=3,
        selected_id=1,
        latitude=random.uniform(start_lat, stop_lat),
        longitude=random.uniform(start_lon, stop_lon)
    )

    db_session.add(favour1)
    db_session.add(favour2)
    db_session.add(favour3)
    db_session.commit()

    # -------------------- CREATE OPINIONS --------------------
    mylogger.info("Creating default opinions...")

    opinion_1 = Opinion(

        description="Esto es un prueba de opinión 1 ",
        mark=3,
        avaluator_id = 1,
        user_id = 2
    )

    opinion_2 = Opinion(
        description="Esto es un prueba de opinión 2",
        mark=5,
        avaluator_id=1,
        user_id=3
    )

    opinion_3 = Opinion(
        description="Esto es un prueba de opinión 3",
        mark=2,
        avaluator_id=2,
        user_id=3
    )

    db_session.add(opinion_1)
    db_session.add(opinion_2)
    db_session.add(opinion_3)
    db_session.commit()



    db_session.close()
