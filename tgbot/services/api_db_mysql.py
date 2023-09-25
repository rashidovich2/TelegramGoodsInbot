# - *- coding: utf- 8 - *-
from __future__ import annotations
import logging
from datetime import datetime
from typing import List
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import BigInteger
from sqlalchemy import Float
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import MetaData
from sqlalchemy import update, delete, and_
from sqlalchemy.exc import TimeoutError
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import func
from tenacity import retry, wait_exponential, stop_after_attempt
from dotenv import load_dotenv
import os


#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
load_dotenv()

# Get the database URI and track modifications value from environment variables
db_uri = os.getenv('SQLALCHEMY_DATABASE_FULL_URI')

my_server_string = "mysql+asyncmy://u95430_telegram_port:Aa876024311abc@185.253.34.81/u95430_telegram_port"
my_server_string2 = "mysql+asyncmy://z_dev_catalogue_bot:yB1aK2uF0iaU9oZ9eO7e@46.23.98.123/z_dev_catalogue_bot"

class Base(AsyncAttrs, DeclarativeBase):
    pass

# Create the database engine
#engine = create_engine('mysql+mysqlconnector://u95430_telegram_port:Aa876024311abc@185.253.34.81/u95430_telegram_port')

# Create a session factory
#Session = sessionmaker(bind=engine)

# Create a base class for declarative models
#Base = declarative_base()
# Получение текущей даты
def get_date():
    this_date = datetime.now().replace(microsecond=0)
    this_date = this_date.strftime("%d.%m.%Y %H:%M:%S")

    return this_date

class AsyncCustomSession:
    def __init__(self):
        self.session = Session()

    async def __aenter__(self):
        await asyncio.sleep(0)  # Create an awaitable to make the method asynchronous
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await asyncio.sleep(0)  # Create an awaitable to make the method asynchronous
        self.session.close()

# Define a model for the table
class Sended(Base):
    __tablename__ = 'telegram_positions_sending'
    send_id = Column(Integer, primary_key=True)
    chat_id = Column(String(50))
    position_id = Column(BigInteger)
    position_description = Column(String(1024))
    resultx = Column(String(50))
    datetime = Column(String(50))

'''class Position(Base):
    __tablename__ = 'positions'
    position_id = Column(Integer, primary_key=True),
    position_name = Column(String(50)),
    position_price = Column(Float(2)),
    position_type = Column(Integer),
    position_rest = Column(Integer),
    position_description = Column(String(1024)),
    position_photo = Column(String(50)),
    position_date = Column(String(50)),
    category_id = Column(BigInteger),
    position_city = Column(String(50)),
    store_id = Column(Integer),
    position_city_id = Column(BigInteger),
    position_user_id = Column(BigInteger),
    source = Column(String(50)),
    local = Column(Integer)'''

meta = MetaData()
sended = Table("telegram_positions_sending", meta, Column("sended_id", BigInteger, primary_key=True), Column("chat_id", String(255)), Column("position_id", BigInteger), Column("position_description", String(1024)), Column("resultx", String(255)), Column("datetime", String(50)))
position = Table("positions", meta, Column("position_id", Integer, primary_key=True), Column("position_name", String(50)), Column("position_price", Integer), Column("position_type", Integer), Column("position_rest", Integer), Column("position_description", String(1024)), Column("position_photo", String(100)), Column("position_date", String(50)), Column("category_id", BigInteger), Column("position_city", String(50)), Column("store_id", Integer), Column("position_city_id", BigInteger), Column("position_user_id", BigInteger), Column("bsource", String(50)), Column("blocal", Integer))
category = Table("category", meta, Column("increment", Integer, primary_key=True), Column("category_id", BigInteger), Column("level", Integer), Column("position_id", Integer), Column("category_name", String(255)))
chats = Table("chgrb", meta, Column('chat_id', Integer), Column('chat_name', String(100)), Column('chat_url', String(100)), Column('chat_admin_username', String(100)), Column('account_to_post', String(100)), Column('chat_state', String(100)), Column('chat_description', String(100)), Column('chat_user_id', Integer), Column('article_url', String(100)), Column('chat_photo', String(100)), Column('chat_type', String(100)))
user = Table("users", meta, Column('increment',  BigInteger), Column('user_id',  BigInteger), Column('user_login', Text), Column('user_name', Text), Column('user_lang', Text), Column('user_balance',  BigInteger), Column('user_hold', BigInteger), Column('user_refill', Integer), Column('user_date', String(255)), Column('user_unix',  Integer), Column('user_city', Text), Column('user_ads', Text), Column('user_phone', Text), Column('user_geocode', Text), Column('user_role', Text), Column('user_city_id',  BigInteger), Column('promocode', Text), Column('free_delivery_point',  BigInteger), Column('delivery_rate',  BigInteger), Column('new_prod_notify',  BigInteger))
crypto_payment_addresses = Table("crypto_payment_addresses", meta, Column('user_id', BigInteger), Column('tron_address', String(100)), Column('private_key', String(100)), Column('type_net', String(10)))


#time_created = Column(DateTime(timezone=True), server_default=func.now())
#time_updated = Column(DateTime(timezone=True), onupdate=func.now())

# Function to insert data into the database
async def insert_position(position_id, position_name, position_price, position_type, position_rest, position_description, position_photo, position_date, category_id, position_city, store_id, position_city_id, position_user_id, bsource, blocal) -> None:
    engine = create_async_engine(
        "mysql+asyncmy://u95430_telegram_port:Aa876024311abc@185.253.34.81/u95430_telegram_port",
        echo=True,
    )
    try:
        async with engine.begin() as conn:
            result = await conn.execute(
                position.insert(), [{"position_id": position_id, "position_name": position_name, "position_price": position_price, "position_type": position_type, "position_rest": position_rest, "position_description": position_description, "position_photo": position_photo, "position_date": get_date(), "category_id": category_id, "position_city": position_city, "store_id": store_id, "position_city_id": position_city_id, "position_user_id": position_user_id, "bsource": bsource, "blocal": blocal}]
            )
    except Exception as e:
        print(f"An error occurred: {e}")
        # handle your exception here
    finally:
        await engine.dispose()

#SELECT таблицы positions по словарю условий
#where_clauses = [position.c.position_price > 100]
async def fetch_positions(positions, where_clauses):
    engine = create_async_engine(
        my_server_string,
        echo=True,
    )
    try:
        async with AsyncSession(engine) as session:
            stmt = select(positions).where(*where_clauses)
            result = await session.execute(stmt)
            data = result.fetchall()
        return data
    except Exception as e:
        print(f"An error occurred: {e}")

#UPDATE таблицы positions с динамическими условиями и новыми значениями
#table - мета описание таблицы
#where_clauses = [position.c.position_id == 1]
#values = {"position_price": 200}
async def update_data(table, where_clauses, values):
    engine = create_async_engine(
        my_server_string,
        echo=True,
    )
    try:
        async with AsyncSession(engine) as session:
            stmt = (
                update(table).
                where(*where_clauses).
                values(**values)
            )
            await session.execute(stmt)
            await session.commit()
    except Exception as e:
        print(f"An error occurred: {e}")

#DELETE rows by keys values from table
#where_clauses = [position.c.position_id == 1]
async def delete_data(table, where_clauses):
    engine = create_async_engine(
        my_server_string,
        echo=True,
    )
    try:
        async with AsyncSession(engine) as session:
            stmt = delete(table).where(*where_clauses)
            await session.execute(stmt)
            await session.commit()
    except Exception as e:
        print(f"An error occurred: {e}")

#SELECT таблицы positions по словарю условий
#where_clauses = [position.c.position_price > 100]
async def fetch_data(table, where_clauses):
    engine = create_async_engine(
        my_server_string,
        echo=True,
    )
    if len(where_clauses) >= 2:
        stmtt = select(table).where(and_(*where_clauses))
    elif len(where_clauses) == 1:
        stmtt = select(table).where(*where_clauses)
    try:
        async with AsyncSession(engine) as session:
            stmt = stmtt
            result = await session.execute(stmt)
            data = result.fetchall()
            columns = result.keys()
            data_dict = [dict(zip(columns, row)) for row in data]

        return data_dict
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to insert data into the database
@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
async def insert_position_sended(chat_id, position_id, position_description, resultx, datetime) -> None:
    engine = create_async_engine(
        "mysql+asyncmy://u95430_telegram_port:Aa876024311abc@185.253.34.81/u95430_telegram_port?connect_timeout=60",
        echo=True, pool_size=10, max_overflow=20
    )
    async with engine.begin() as conn:
        await conn.execute(
            sended.insert(), [{"chat_id": chat_id, "position_id": position_id, "position_description": position_description, "resultx": resultx, "datetime": datetime}]
        )

    await engine.dispose()

# Function to insert data into the database
async def check_chat_resultx(chat_id) -> None:
    engine = create_async_engine(
        "mysql+asyncmy://u95430_telegram_port:Aa876024311abc@185.253.34.81/u95430_telegram_port",
        echo=True,
    )
    async with engine.connect() as conn:
        # select a Result, which will be delivered with buffered
        # results
        result = await conn.execute(select(sended).where(sended.c.chat_id == chat_id).where(sended.c.resultx != "Posted"))

        # Check if the query was executed correctly
        if result.is_insert:
            print("Query executed successfully")

        # Check if there are any matching rows
        rows = result.fetchall()
        if rows:
            print("Matching rows found!")
            for row in rows:
                print(row)
        else:
            print("No matching rows found")

        return rows

async def check_chat(chat_id) -> None:
    engine = create_async_engine(
        "mysql+asyncmy://u95430_telegram_port:Aa876024311abc@185.253.34.81/u95430_telegram_port",
        echo=True,
    )
    async with engine.connect() as conn:
        # select a Result, which will be delivered with buffered
        # results
        result = await conn.execute(select(sended).where(sended.c.chat_id == chat_id))

        # Check if the query was executed correctly
        if result.is_insert:
            print("Query executed successfully")

        # Check if there are any matching rows
        rows = result.fetchall()
        if rows:
            print("Matching rows found!")
            for row in rows:
                print(row)
        else:
            print("No matching rows found")

        return rows