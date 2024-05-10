import datetime

from database.connection import get_db_sessionmaker
from database.models.model_db import WalletModel
from sqlalchemy import select, and_, delete
from sqlalchemy.exc import DBAPIError
from exceptions.db_exceptions import DatabaseError, EmptyFieldError, LongFieldError
from exceptions.community_exceptions import BalanceLessZero


class WalletController:
    def __init__(self) -> None:
        self.db_session_maker = get_db_sessionmaker()

    def wallet_insert(self, user_name: str, password: str, cur_summ: float = 0):
        try:
            with self.db_session_maker.begin() as session:
                if user_name == '':
                    raise EmptyFieldError
                if password == '':
                    raise EmptyFieldError
                if len(user_name)>32 or len(password)>32:
                    raise LongFieldError
                session.add(WalletModel(id=user_name,
                                        password=password,
                                        balance=cur_summ))
                session.commit()
        except DBAPIError as e:
            session.rollback()
            raise DatabaseError() from e

    def wallet_balance_update(self, user_name: str, cur_summ: float = 0):
        try:
            with self.db_session_maker.begin() as session:
                if cur_summ<0:
                    raise BalanceLessZero
                session.query(WalletModel).filter(WalletModel.id == user_name).update({'balance': cur_summ})
                session.commit()
        except DBAPIError as e:
            session.rollback()
            raise DatabaseError() from e

    def wallet_select_balance(self, user_name: str):
        try:
            with self.db_session_maker.begin() as session:
                balance = session.scalar(select(WalletModel.balance).where(WalletModel.id == user_name))
                return balance

        except DBAPIError as e:
            raise DatabaseError() from e

    def wallet_select_account(self, user_name: str, password: str):
        try:
            with self.db_session_maker.begin() as session:
                acc = session.scalar(select(WalletModel).where(and_(WalletModel.id == user_name,
                                                                    WalletModel.password == password)))
                return acc
        except DBAPIError as e:
            raise DatabaseError() from e

    def wallet_select_account_by_name(self, user_name: str):
        try:
            with self.db_session_maker.begin() as session:
                acc = session.scalar(select(WalletModel).where(and_(WalletModel.id == user_name)))
                return acc
        except DBAPIError as e:
            raise DatabaseError() from e

    def wallet_delete_by_id(self, id: str):
        try:
            with self.db_session_maker.begin() as session:
                return session.execute(delete(WalletModel).where(WalletModel.id == id))
        except DBAPIError as e:
            raise DatabaseError() from e


