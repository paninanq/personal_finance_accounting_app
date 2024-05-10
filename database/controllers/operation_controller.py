from database.connection import get_db_sessionmaker
from database.models.model_db import OperationModel
from sqlalchemy.exc import DBAPIError
from exceptions.db_exceptions import DatabaseError
from sqlalchemy import select, and_, desc, delete
from finances.accounting import Operation


class OperationController:
    def __init__(self) -> None:
        self.db_session_maker = get_db_sessionmaker()

    def operation_insert(self, id_wallet: str, operation: Operation):
        try:
            with self.db_session_maker.begin() as session:
                session.add(OperationModel(id_wallet=id_wallet,
                                           date_time=operation.date_time,
                                           type=operation.type,
                                           summ=operation.summ))
                session.commit()
        except DBAPIError as e:
            session.rollback()
            raise DatabaseError() from e

    def operation_select_by_acc(self, wallet_id: int):
        try:
            with (self.db_session_maker.begin() as session):
                return session.query(OperationModel).where(OperationModel.id_wallet == wallet_id
                                                           ).order_by(desc(OperationModel.id)).all()
        except DBAPIError as e:
            raise DatabaseError() from e

    def operation_select_by_type(self, wallet_id: int, type: str):
        try:
            with self.db_session_maker.begin() as session:
                return session.query(OperationModel).where(and_(OperationModel.id_wallet == wallet_id,
                                                                OperationModel.type == type).order_by(desc(OperationModel.id))).all()
        except DBAPIError as e:
            raise DatabaseError() from e

    def operation_select_by_day(self, wallet_id: int, day: int):
        try:
            with self.db_session_maker.begin() as session:
                return session.query(OperationModel).where(and_(OperationModel.id_wallet == wallet_id,
                                                                OperationModel.date_time.day == day)).all()
        except DBAPIError as e:
            raise DatabaseError() from e

    def operation_select_by_month(self, wallet_id: int, month: int):
        try:
            with self.db_session_maker.begin() as session:
                return session.query(OperationModel).where(and_(OperationModel.id_wallet == wallet_id,
                                                                OperationModel.date_time.month == month)).all()
        except DBAPIError as e:
            raise DatabaseError() from e

    def operation_select_by_year(self, wallet_id: int, year: int):
        try:
            with self.db_session_maker.begin() as session:
                return session.query(OperationModel).where(and_(OperationModel.id_wallet == wallet_id,
                                                                OperationModel.date_time.year == year)).all()
        except DBAPIError as e:
            raise DatabaseError() from e

    def operation_select_by_id(self, id: int):
        try:
            with self.db_session_maker.begin() as session:
                return session.scalar(select(OperationModel).where(OperationModel.id == id))
        except DBAPIError as e:
            raise DatabaseError() from e

    def operation_delete_last_by_wallet_id(self, wallet_id: str):
        try:
            with self.db_session_maker.begin() as session:
                operation = session.query(OperationModel).where(OperationModel.id_wallet == wallet_id).order_by(OperationModel.id.desc()).first()
                return session.execute(delete(OperationModel).where(OperationModel.id == operation.id))
        except DBAPIError as e:
            raise DatabaseError() from e
