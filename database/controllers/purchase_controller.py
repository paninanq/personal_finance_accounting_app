from database.connection import get_db_sessionmaker
from database.models.model_db import PurchaseModel
from finances.accounting import Purchase
from sqlalchemy.exc import DBAPIError
from exceptions.db_exceptions import DatabaseError, LongFieldError, EmptyFieldError
from exceptions.community_exceptions import PriceLessZero
from sqlalchemy import select, delete, and_, desc



class PurchasesController:
    def __init__(self) -> None:
        self.db_session_maker = get_db_sessionmaker()

    def purchases_insert(self, id_wallet: str, purchase: Purchase):
        try:
            with self.db_session_maker.begin() as session:
                if len(purchase.name) == 0:
                    raise EmptyFieldError
                if len(purchase.name) > 32:
                    raise LongFieldError
                if purchase.price <= 0:
                    raise PriceLessZero

                session.add(PurchaseModel(wallet_id=id_wallet,
                                           name=purchase.name,
                                           category=purchase.category,
                                           date=purchase.date_purchase,
                                           price=purchase.price)
                            )
                session.commit()
        except DBAPIError as e:
            session.rollback()
            raise DatabaseError() from e

    def purchase_select_by_id(self, id: int):
        try:
            with self.db_session_maker.begin() as session:
                return session.scalar(select(PurchaseModel).where(PurchaseModel.id == id))
        except DBAPIError as e:
            raise DatabaseError() from e

    def purchase_select_by_day(self, wallet_id: str, day: int):
        try:
            with self.db_session_maker.begin() as session:
                return session.query(PurchaseModel).where(and_(PurchaseModel.date.day == day,
                                                                  PurchaseModel.wallet_id == wallet_id)).order_by(desc(PurchaseModel.id)).all()
        except DBAPIError as e:
            raise DatabaseError() from e

    def purchase_select_by_month(self, wallet_id: str, month: int):
        try:
            with self.db_session_maker.begin() as session:
                return session.query(PurchaseModel).where(and_(PurchaseModel.date.month == month,
                                                                  PurchaseModel.wallet_id == wallet_id)).order_by(desc(PurchaseModel.id)).all()
        except DBAPIError as e:
            raise DatabaseError() from e

    def purchase_select_by_year(self, wallet_id: str, year: int):
        try:
            with self.db_session_maker.begin() as session:
                return session.query(PurchaseModel).where(and_(PurchaseModel.date.year == year,
                                                                  PurchaseModel.wallet_id == wallet_id)).order_by(desc(PurchaseModel.id)).all()
        except DBAPIError as e:
            raise DatabaseError() from e

    def purchase_select_by_category(self, wallet_id: str, category: str):
        try:
            with self.db_session_maker.begin() as session:
                return session.query(PurchaseModel).where(and_(PurchaseModel.category == category,
                                                                  PurchaseModel.wallet_id == wallet_id)).order_by(desc(PurchaseModel.id)).all()
        except DBAPIError as e:
            raise DatabaseError() from e

    def purchase_select_by_acc(self, wallet_id: str):
        try:
            with self.db_session_maker.begin() as session:
                return session.query(PurchaseModel).where(PurchaseModel.wallet_id == wallet_id).order_by(desc(PurchaseModel.id)).all()
        except DBAPIError as e:
            raise DatabaseError() from e

    def purchase_delete_by_id(self, id: int):
        try:
            with self.db_session_maker.begin() as session:
                return session.execute(delete(PurchaseModel).where(PurchaseModel.id == id))
        except DBAPIError as e:
            raise DatabaseError() from e

    def purchase_delete_last_by_wallet_id(self, wallet_id: str):
        try:
            with self.db_session_maker.begin() as session:
                purchase = session.query(PurchaseModel).where(PurchaseModel.wallet_id == wallet_id).order_by(PurchaseModel.id.desc()).first()
                return session.execute(delete(PurchaseModel).where(PurchaseModel.id == purchase.id))
        except DBAPIError as e:
            raise DatabaseError() from e
