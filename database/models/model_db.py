from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime, date
from typing import Literal
from sqlalchemy import ForeignKey, Date, DateTime


class Base(DeclarativeBase):
    pass


class WalletModel(Base):
    __tablename__ = "wallet"
    id: Mapped[str] = mapped_column(primary_key=True)
    password: Mapped[str] = mapped_column(nullable=0)
    balance: Mapped[float] = mapped_column(default=0)

    def __repr__(self) -> str:
        return f'Wallet (id={self.id!r}, balance={self.balance!r})'


class PurchaseModel(Base):
    __tablename__ = "purchase"
    category_type = Literal["Еда", "Одежда", "Техника", "Другое"]
    id: Mapped[int] = mapped_column(primary_key=True)
    wallet_id: Mapped[str] = mapped_column(ForeignKey(WalletModel.id), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    category: Mapped[category_type] = mapped_column(nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return (f'Purchase (id={self.id!r}, name={self.name!r}, category={self.category!r} date={self.date!r}, '
                f'price={self.price!r})')


class OperationModel(Base):
    __tablename__ = "operation"
    type_operation = Literal["Пополнение", "Списание", "Возврат товара"]
    id: Mapped[int] = mapped_column(primary_key=True)
    id_wallet: Mapped[str] = mapped_column(ForeignKey(WalletModel.id), nullable=False)
    date_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    type: Mapped[type_operation] = mapped_column(nullable=False)
    summ: Mapped[float] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return (f'Operation (id={self.id!r}, id_wallet={self.id!r}, date_time={self.date_time!r},'
                f' type={self.type!r}, summ={self.summ!r})')
