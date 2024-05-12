from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QLineEdit, QPushButton,
                             QMessageBox, QWidget, QHBoxLayout, QLabel, QComboBox, QTableWidget, QTableWidgetItem,
                             QErrorMessage, QCalendarWidget)
from PyQt6.QtGui import QAction
from database.controllers.wallet_controller import WalletController
from database.controllers.operation_controller import OperationController
from database.controllers.purchase_controller import PurchasesController
from finances.accounting import Operation, Purchase
from datetime import datetime, date
from exceptions.community_exceptions import DateError, PriceLessZero, BalanceLessZero, SummLessZero
from exceptions.db_exceptions import EmptyFieldError, LongFieldError


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Учет собственных денежных средств")
        self.setGeometry(860, 200, 600, 200)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.accountUserNameEdit = QLineEdit()
        self.accountUserNameEdit.setPlaceholderText('Логин')
        self.accountPasswordEdit = QLineEdit()
        self.accountPasswordEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.accountPasswordEdit.setPlaceholderText('Пароль')
        self.enterButton = QPushButton("Войти")
        self.enterButton.setStyleSheet("background: rgb(128, 128, 128)")
        self.createAccountButton = QPushButton("Регистрация")
        self.createAccountButton.setStyleSheet("background: rgb(128, 128, 128)")
        self.enterButton.clicked.connect(self.enter_process)
        self.createAccountButton.clicked.connect(self.to_registry)

        full_box = QVBoxLayout()

        enter_layout = QVBoxLayout()
        input_name_password = QVBoxLayout()
        input_name_password.addWidget(self.accountUserNameEdit)
        input_name_password.addWidget(self.accountPasswordEdit)
        self.input_name_password = QWidget()
        self.input_name_password.setLayout(input_name_password)

        gbox = QHBoxLayout()
        gbox.addWidget(self.enterButton)
        gbox.addWidget(self.createAccountButton)
        self.gbox = QWidget()
        self.gbox.setLayout(gbox)
        enter_layout.addWidget(self.input_name_password)
        enter_layout.addWidget(self.gbox)
        self.enter_layout = QWidget()
        self.enter_layout.setLayout(enter_layout)

        self.accountUserNameCreate = QLineEdit()
        self.accountUserNameCreate.setPlaceholderText('Логин')
        self.accountUserPasswordCreate = QLineEdit()
        self.accountUserPasswordCreate.setEchoMode(QLineEdit.EchoMode.Password)
        self.accountUserPasswordCreate.setPlaceholderText('Пароль')

        registry_layout = QVBoxLayout()
        self.backButton = QPushButton("Назад")
        self.backButton.setStyleSheet("background: rgb(0, 128, 0); color: rgb(255, 255, 255)")
        self.backButton.setFixedSize(55, 20)
        self.backButton.clicked.connect(self.to_enter)
        self.registryButton = QPushButton("Зарегистрироваться")
        self.registryButton.setStyleSheet("background: rgb(128, 128, 128)")
        registry_layout.addWidget(self.backButton)
        registry_layout.addWidget(self.accountUserNameCreate)
        registry_layout.addWidget(self.accountUserPasswordCreate)
        registry_layout.addWidget(self.registryButton)

        self.registry_layout = QWidget()
        self.registry_layout.setLayout(registry_layout)
        self.registry_layout.hide()
        self.registryButton.clicked.connect(self.reg_process)

        main_layout = QVBoxLayout()
        self.profileLineEdit = QLineEdit()
        self.profileLineEdit.setReadOnly(True)
        switch_layout = QHBoxLayout()
        self.walletButton = QPushButton("Кошелек")
        self.walletButton.setStyleSheet("background: rgb(128, 128, 128)")
        self.purchasesButton = QPushButton("Мои покупки")
        self.purchasesButton.setStyleSheet("background: rgb(128, 128, 128)")
        self.walletButton.clicked.connect(self.main_to_wallet)
        self.purchasesButton.clicked.connect(self.main_to_purchases)
        switch_layout.addWidget(self.purchasesButton)
        switch_layout.addWidget(self.walletButton)
        self.switch_layout = QWidget()
        self.switch_layout.setLayout(switch_layout)

        main_layout.addWidget(self.profileLineEdit)
        main_layout.addWidget(self.switch_layout)

        wallet_layout = QVBoxLayout()
        balance_layout = QHBoxLayout()
        self.balance_label = QLabel("Баланс")
        self.balance_cur = QLineEdit()
        self.balance_cur.setReadOnly(True)
        self.add_moneyWarn = QLabel("Пополнение баланса доступно 1 числа каждого месяца!")
        self.add_moneyWarn.setStyleSheet('color: rgb(128, 0, 0)')
        self.add_money_Button = QPushButton("Пополнить баланс")
        self.add_money_Button.setStyleSheet('background: rgb(0, 128, 0)')
        self.operation_label = QLabel("История операций: ")
        self.add_money_Button.clicked.connect(self.add_money)

        filter_operations = QHBoxLayout()
        self.type_operation_combo = QComboBox()
        self.type_operation_combo.addItem("Все типы")
        self.type_operation_combo.addItem("Пополнение")
        self.type_operation_combo.addItem("Списание")
        self.day_filter_oper_combo = QComboBox()
        self.add_day_item(self.day_filter_oper_combo)
        self.month_filter_oper_combo = QComboBox()
        self.add_month_item(self.month_filter_oper_combo)
        self.year_filter_oper_combo = QComboBox()
        self.add_year_item(self.year_filter_oper_combo)
        filter_operations.addWidget(self.type_operation_combo)
        filter_operations.addWidget(self.day_filter_oper_combo)
        filter_operations.addWidget(self.month_filter_oper_combo)
        filter_operations.addWidget(self.year_filter_oper_combo)
        self.filter_operations = QWidget()
        self.filter_operations.setLayout(filter_operations)

        self.operations_table = QTableWidget()
        self.operations_table.setColumnCount(3)
        self.operations_table.setColumnWidth(0, 150)
        self.operations_table.setColumnWidth(1, 250)
        self.operations_table.setColumnWidth(2, 350)
        balance_layout.addWidget(self.balance_label)
        balance_layout.addWidget(self.balance_cur)
        self.balance_layout = QWidget()
        self.balance_layout.setLayout(balance_layout)
        wallet_layout.addWidget(self.balance_layout)
        wallet_layout.addWidget(self.add_moneyWarn)
        wallet_layout.addWidget(self.add_money_Button)
        wallet_layout.addWidget(self.operation_label)
        wallet_layout.addWidget(self.filter_operations)
        self.work_filter_oper_button = QPushButton("Применить фильтр")
        self.work_filter_oper_button.setStyleSheet('background: rgb(144, 238, 144)')
        self.work_filter_oper_button.clicked.connect(self.show_operation)
        wallet_layout.addWidget(self.work_filter_oper_button)
        wallet_layout.addWidget(self.operations_table)
        self.wallet_layout = QWidget()
        self.wallet_layout.setLayout(wallet_layout)
        self.wallet_layout.hide()

        re_balance_layout = QVBoxLayout()
        self.summ_Edit = QLineEdit()
        self.summ_Edit.setPlaceholderText('Cумма (руб.)')
        self.edit_summ_Button = QPushButton('Пополнить')
        self.edit_summ_Button.setStyleSheet("background: rgb(0, 128, 0)")
        self.edit_summ_Button.clicked.connect(self.update_summ)
        re_balance_layout.addWidget(self.summ_Edit)
        re_balance_layout.addWidget(self.edit_summ_Button)
        self.re_balance_layout = QWidget()
        self.re_balance_layout.setLayout(re_balance_layout)
        self.re_balance_layout.hide()

        purchases_layout = QVBoxLayout()
        self.add_purchasesButton = QPushButton("Добавить покупку")
        self.add_purchasesButton.setStyleSheet('background: rgb(0, 128, 0)')
        self.add_purchasesButton.clicked.connect(self.add_purchase)
        self.purchases_label = QLabel("Мои покупки: ")

        filter_purchases = QHBoxLayout()
        self.cat_filter_combo = QComboBox()
        self.cat_filter_combo.addItem("Все категории")
        self.cat_filter_combo.addItem("Еда")
        self.cat_filter_combo.addItem("Одежда")
        self.cat_filter_combo.addItem("Техника")
        self.cat_filter_combo.addItem("Другое")
        self.day_filter_combo = QComboBox()
        self.add_day_item(self.day_filter_combo)
        self.month_filter_combo = QComboBox()
        self.add_month_item(self.month_filter_combo)
        self.year_filter_combo = QComboBox()
        self.add_year_item(self.year_filter_combo)
        filter_purchases.addWidget(self.cat_filter_combo)
        filter_purchases.addWidget(self.day_filter_combo)
        filter_purchases.addWidget(self.month_filter_combo)
        filter_purchases.addWidget(self.year_filter_combo)

        self.filter_purchases = QWidget()
        self.filter_purchases.setLayout(filter_purchases)
        self.work_filter_button = QPushButton("Применить фильтр")
        self.work_filter_button.setStyleSheet('background: rgb(144, 238, 144)')
        self.work_filter_button.clicked.connect(self.show_purchases)
        purchases_layout.addWidget(self.add_purchasesButton)
        purchases_layout.addWidget(self.purchases_label)
        self.my_purchases_table = QTableWidget()
        self.my_purchases_table.setColumnCount(5)
        self.my_purchases_table.setColumnWidth(0, 150)
        self.my_purchases_table.setColumnWidth(1, 150)
        self.my_purchases_table.setColumnWidth(2, 150)
        self.my_purchases_table.setColumnWidth(3, 150)
        self.my_purchases_table.setColumnWidth(4, 150)

        purchases_layout.addWidget(self.filter_purchases)
        purchases_layout.addWidget(self.work_filter_button)
        purchases_layout.addWidget(self.my_purchases_table)
        self.purchases_layout = QWidget()
        self.purchases_layout.setLayout(purchases_layout)

        add_purchase_layout = QVBoxLayout()

        self.date_label = QLabel("Дата")
        self.date_of_purch = QLineEdit()
        self.date_of_purch.setText('0'*(2-len(str(date.today().day)))+str(date.today().day) + '.' +
                                   '0'*(2-len(str(date.today().month)))+str(date.today().month) + '.'
                                   + str(date.today().year))
        self.date_of_purch.setReadOnly(True)
        v_box_date = QVBoxLayout()
        self.calendar = QCalendarWidget()
        self.edit_date_Button = QPushButton("Изменить дату")
        self.edit_date_Button.setStyleSheet('background: rgb(128, 128, 128)')
        self.edit_date_Button.clicked.connect(self.edit_date)
        v_box_date.addWidget(self.calendar)
        v_box_date.addWidget(self.edit_date_Button)
        self.v_box_date = QWidget()
        self.v_box_date.setLayout(v_box_date)

        self.name_purchase_Edit = QLineEdit()
        self.name_purchase_Edit.setPlaceholderText("Название покупки")
        self.category_label = QLabel("Категория")
        self.category_combo = QComboBox()
        self.category_combo.addItem("Еда")
        self.category_combo.addItem("Одежда")
        self.category_combo.addItem("Техника")
        self.category_combo.addItem("Другое")
        self.price_purchase_Edit = QLineEdit()
        self.price_purchase_Edit.setPlaceholderText("Цена")
        self.add_purchase_in_added_Button = QPushButton("Добавить покупку")
        self.add_purchase_in_added_Button.setStyleSheet('background: rgb(0, 129, 0); color: rgb(255, 255, 255)')
        self.add_purchase_in_added_Button.clicked.connect(self.add_purchase_db)
        add_purchase_layout.addWidget(self.name_purchase_Edit)
        add_purchase_layout.addWidget(self.category_label)
        add_purchase_layout.addWidget(self.category_combo)
        add_purchase_layout.addWidget(self.date_label)
        add_purchase_layout.addWidget(self.v_box_date)
        add_purchase_layout.addWidget(self.date_of_purch)
        add_purchase_layout.addWidget(self.price_purchase_Edit)
        add_purchase_layout.addWidget(self.add_purchase_in_added_Button)

        self.add_purchase_layout = QWidget()
        self.add_purchase_layout.setLayout(add_purchase_layout)
        self.add_purchase_layout.hide()

        insufficient_funds_mlayout = QVBoxLayout()
        self.warningLabel = QLabel("На вашем счете недостаточно средств!")
        self.warningLabel.setStyleSheet("color: rgb(128, 0, 0)")
        self.cancel_purchase_but = QPushButton("Отменить покупку")
        self.cancel_purchase_but.clicked.connect(self.cancel_purchase)
        self.continue_purchase_but = QPushButton("Сохранить покупку в списке покупок без списание средств")
        self.continue_purchase_but.clicked.connect(self.continue_purchase)
        insufficient_funds_mlayout.addWidget(self.warningLabel)
        insufficient_funds_layout = QHBoxLayout()
        insufficient_funds_layout.addWidget(self.cancel_purchase_but)
        insufficient_funds_layout.addWidget(self.continue_purchase_but)
        self.insufficient_funds_layout = QWidget()
        self.insufficient_funds_layout.setLayout(insufficient_funds_layout)
        insufficient_funds_mlayout.addWidget(self.insufficient_funds_layout)
        self.insufficient_funds_mlayout = QWidget()
        self.insufficient_funds_mlayout.setLayout(insufficient_funds_mlayout)
        self.insufficient_funds_mlayout.hide()

        main_layout.addWidget(self.insufficient_funds_mlayout)
        main_layout.addWidget(self.purchases_layout)
        main_layout.addWidget(self.wallet_layout)
        self.main_layout = QWidget()
        self.main_layout.setLayout(main_layout)
        self.main_layout.hide()

        full_box.addWidget(self.enter_layout)
        full_box.addWidget(self.registry_layout)
        full_box.addWidget(self.main_layout)
        full_box.addWidget(self.wallet_layout)
        full_box.addWidget(self.add_purchase_layout)
        full_box.addWidget(self.re_balance_layout)
        self.full_box = QWidget()
        self.full_box.setLayout(full_box)
        central_widget = QWidget()
        central_widget.setLayout(full_box)
        self.setCentralWidget(central_widget)
        self.menu()
        self.show()

    def to_registry(self):
        self.enter_layout.hide()
        self.accountUserNameEdit.clear()
        self.accountPasswordEdit.clear()
        self.registry_layout.show()

    def to_enter(self):
        self.registry_layout.hide()
        self.accountUserNameCreate.clear()
        self.accountUserPasswordCreate.clear()
        self.enter_layout.show()

    def reg_process(self):
        try:
            user_name = self.accountUserNameCreate.text()
            password = self.accountUserPasswordCreate.text()
            wall_c = WalletController()
            similar_name = wall_c.wallet_select_account_by_name(user_name)
            if similar_name is None:
                wallet_contr = WalletController()
                wallet_contr.wallet_insert(user_name, password)
                self.registry_layout.hide()
                self.accountUserNameCreate.clear()
                self.accountUserPasswordCreate.clear()
                self.enter_layout.show()
            else:
                warn = ('Пользователь с данным логином логином уже существует. \n'
                        'Пожалуйста, повторите попытку.')
                QMessageBox.about(self, "Ошибка", warn)
        except EmptyFieldError:
            er = QErrorMessage(self)
            error_text = 'Поля "Логин" и "Пароль" не могут быть пустыми'
            er.showMessage(error_text)
        except LongFieldError:
            er = QErrorMessage(self)
            error_text = 'Параметры "Логин" и "Пароль" не могут превышать по длине 32 символа'
            er.showMessage(error_text)

    def enter_process(self):
        user_name = self.accountUserNameEdit.text()
        password = self.accountPasswordEdit.text()
        wallet_contr = WalletController()
        account = wallet_contr.wallet_select_account(user_name, password)
        if account is None:
            warn = ('Пользователя с данным логином и паролем не существует. \n'
                    'Пожалуйста, повторите попытку.')
            er = QErrorMessage(self)
            er.showMessage(warn)
        else:
            self.profileLineEdit.setText(user_name)
            self.accountUserNameEdit.clear()
            self.accountPasswordEdit.clear()
            self.enter_layout.hide()
            self.main_layout.show()
            self.show_purchases()
            self.setGeometry(860, 200, 820, 400)

    def get_balance(self):
        wallet_contr = WalletController()
        user_id = self.profileLineEdit.text()
        cur_bal = wallet_contr.wallet_select_balance(user_id)
        self.balance_cur.setText(f'{cur_bal} руб')

    def main_to_wallet(self):
        self.re_balance_layout.hide()
        self.add_purchase_layout.hide()
        self.purchases_layout.hide()
        self.wallet_layout.show()
        self.get_balance()
        self.show_operation()

    def main_to_purchases(self):
        self.add_purchase_layout.hide()
        self.re_balance_layout.hide()
        self.wallet_layout.hide()
        self.purchases_layout.show()

    def add_money(self):
        if str(datetime.now())[8:8+2] == '01':
            self.wallet_layout.hide()
            self.re_balance_layout.show()
            self.setGeometry(860, 200, 600, 200)
        else:
            text = "Пополнение баланса доступно только первого числа каждого месяца"
            er = QErrorMessage(self)
            er.showMessage(text)

    def update_summ(self):
        try:
            summ = float(self.summ_Edit.text())
            if summ<=0:
                raise SummLessZero
            wc = WalletController()
            bef_upd = wc.wallet_select_balance(self.profileLineEdit.text())
            wc.wallet_balance_update(self.profileLineEdit.text(), bef_upd+summ)
            operation = Operation(summ=summ, type="Пополнение")
            oc = OperationController()
            oc.operation_insert(self.profileLineEdit.text(), operation)
            self.update_summ_to_wallet()
        except ValueError:
            warn = 'В поле "Пополнить" можно вводить только вещественные числа большие нуля'
            error = QErrorMessage(self)
            error.showMessage(warn)
        except BalanceLessZero:
            warn = 'Баланс не может быть меньше нуля'
            error = QErrorMessage(self)
            error.showMessage(warn)
        except SummLessZero:
            warn = 'Сумма пополнения должна быть больлше нуля'
            error = QErrorMessage(self)
            error.showMessage(warn)

    def update_summ_to_wallet(self):
        self.summ_Edit.clear()
        self.re_balance_layout.hide()
        self.setGeometry(860, 200, 820, 400)
        self.wallet_layout.show()
        self.get_balance()
        self.show_operation()

    def add_purchase(self):
        self.purchases_layout.hide()
        self.add_purchase_layout.show()

    def add_purchase_db(self):
        try:
            purchase_name = self.name_purchase_Edit.text()
            purchase_category = str(self.category_combo.currentText())
            day_of_purchase = int(self.date_of_purch.text()[:2])
            month_of_purchase = int(self.date_of_purch.text()[3:5])
            year_of_purchase = int(self.date_of_purch.text()[6:])
            date_of_purchase = date(year_of_purchase, month_of_purchase, day_of_purchase)
            if date_of_purchase>date.today():
                raise DateError
            date_time_of_purchase = datetime(year_of_purchase, month_of_purchase, day_of_purchase,
                                             0, 0, 0)
            price_of_purchase = float(self.price_purchase_Edit.text())
            purchase = Purchase(purchase_name, date_of_purchase, purchase_category, price_of_purchase)
            pc = PurchasesController()
            pc.purchases_insert(self.profileLineEdit.text(), purchase)
            operation = Operation(summ=price_of_purchase, date_time=date_time_of_purchase, type="Списание")
            oc = OperationController()
            oc.operation_insert(self.profileLineEdit.text(), operation)
            wc = WalletController()
            bef_upd = wc.wallet_select_balance(self.profileLineEdit.text())
            wc.wallet_balance_update(self.profileLineEdit.text(), bef_upd-price_of_purchase)
            self.name_purchase_Edit.clear()
            self.price_purchase_Edit.clear()
            self.show_purchases()
            self.add_purchase_layout.hide()
            self.purchases_layout.show()
        except ValueError:
            warn = 'В поле "Цена" можно вводить только вещественные числа большие нуля'
            error = QErrorMessage(self)
            error.showMessage(warn)
        except PriceLessZero:
            warn = 'Цена покупки должна быть больше нуля'
            error = QErrorMessage(self)
            error.showMessage(warn)
        except EmptyFieldError:
            warn = 'Название покупки не может быть пустым полем'
            error = QErrorMessage(self)
            error.showMessage(warn)
        except LongFieldError:
            warn = 'Длина названия покупки не может превышать 32 символа'
            error = QErrorMessage(self)
            error.showMessage(warn)
        except BalanceLessZero:
            self.insufficient_funds()
        except DateError:
            warn = 'Дата покупки не может быть позже сегодняшней даты'
            error = QErrorMessage(self)
            error.showMessage(warn)

    def insufficient_funds(self):
        self.add_purchase_layout.hide()
        self.insufficient_funds_mlayout.show()

    def cancel_purchase(self):
        oc = OperationController()
        oc.operation_delete_last_by_wallet_id(self.profileLineEdit.text())
        pc = PurchasesController()
        pc.purchase_delete_last_by_wallet_id(self.profileLineEdit.text())
        self.name_purchase_Edit.clear()
        self.price_purchase_Edit.clear()
        self.insufficient_funds_mlayout.hide()
        self.purchases_layout.show()
        self.show_purchases()

    def continue_purchase(self):
        oc = OperationController()
        oc.operation_delete_last_by_wallet_id(self.profileLineEdit.text())
        self.name_purchase_Edit.clear()
        self.price_purchase_Edit.clear()
        self.insufficient_funds_mlayout.hide()
        self.purchases_layout.show()
        self.show_purchases()

    def show_purchases(self):
        pc = PurchasesController()
        if self.cat_filter_combo.currentText() == "Все категории":
            purchases_cat = pc.purchase_select_by_acc(self.profileLineEdit.text())
        else:
            purchases_cat = pc.purchase_select_by_category(self.profileLineEdit.text(),
                                                           self.cat_filter_combo.currentText())
        purchases_cat = [purch.id for purch in purchases_cat]
        if self.day_filter_combo.currentText() == "День без фильтра":
            purchases_day = pc.purchase_select_by_acc(self.profileLineEdit.text())
        else:
            purchases_day = [purchase for purchase in pc.purchase_select_by_acc(self.profileLineEdit.text())
                             if purchase.date.day == int(self.day_filter_combo.currentText())]
        purchases_day = [purch.id for purch in purchases_day]
        if self.month_filter_combo.currentText() == "Месяц без фильтра":
            purchases_month = pc.purchase_select_by_acc(self.profileLineEdit.text())
        else:
            purchases_month = [purchase for purchase in pc.purchase_select_by_acc(self.profileLineEdit.text())
                             if purchase.date.month == int(self.month_filter_combo.currentText())]
        purchases_month = [purch.id for purch in purchases_month]
        if self.year_filter_combo.currentText() == "Год без фильтра":
            purchases_year = pc.purchase_select_by_acc(self.profileLineEdit.text())
        else:
            purchases_year = [purchase for purchase in pc.purchase_select_by_acc(self.profileLineEdit.text())
                             if purchase.date.year == int(self.year_filter_combo.currentText())]
        purchases_year = [purch.id for purch in purchases_year]
        self.purchases_id = [purchase_id for purchase_id in purchases_cat if purchase_id in purchases_day and
                        purchase_id in purchases_month and purchase_id in purchases_year]
        purchases = [pc.purchase_select_by_id(purch_id) for purch_id in self.purchases_id]

        self.my_purchases_table.setHorizontalHeaderLabels(["Название", "Категория", "Дата", "Цена", " "])
        self.my_purchases_table.setRowCount(len(purchases))

        row = 0
        for purch in purchases:
            self.my_purchases_table.setItem(row, 0, QTableWidgetItem(purch.name))
            self.my_purchases_table.setItem(row, 1, QTableWidgetItem(purch.category))
            self.my_purchases_table.setItem(row, 2, QTableWidgetItem(str(purch.date)))
            self.my_purchases_table.setItem(row, 3, QTableWidgetItem(str(purch.price)+' руб.'))
            delete_button = QPushButton("Удалить товар")
            delete_button.setStyleSheet('color: rgb(255, 255, 255); background: rgb(128, 0, 0)')
            delete_button.clicked.connect(lambda ch, row=row: self.delete_purchase(row))
            self.my_purchases_table.setCellWidget(row, 4, delete_button)
            row += 1

    def delete_purchase(self, row):
        pc = PurchasesController()
        purch = pc.purchase_select_by_id(self.purchases_id[row])
        oc = OperationController()
        del_operation = Operation(summ=purch.price, type="Возврат товара")
        oc.operation_insert(self.profileLineEdit.text(), del_operation)
        wc = WalletController()
        bef_upd = wc.wallet_select_balance(self.profileLineEdit.text())
        wc.wallet_balance_update(self.profileLineEdit.text(), bef_upd+purch.price)
        pc.purchase_delete_by_id(self.purchases_id[row])
        self.my_purchases_table.removeRow(row)
        self.show_purchases()

    def show_operation(self):
        oc = OperationController()
        if self.type_operation_combo.currentText() == "Все типы":
            operations_type = oc.operation_select_by_acc(self.profileLineEdit.text())
        else:
            operations_type = oc.operation_select_by_type(self.profileLineEdit.text(),
                                                          self.type_operation_combo.currentText())
        operations_type = [operation.id for operation in operations_type]
        if self.day_filter_oper_combo.currentText() == "День без фильтра":
            operations_day = oc.operation_select_by_acc(self.profileLineEdit.text())
        else:
            operations_day = [operation for operation in oc.operation_select_by_acc(self.profileLineEdit.text())
                              if operation.date_time.day==int(self.day_filter_oper_combo.currentText())]
        operations_day = [operation.id for operation in operations_day]
        if self.month_filter_oper_combo.currentText() == "Месяц без фильтра":
            operations_month = oc.operation_select_by_acc(self.profileLineEdit.text())
        else:
            operations_month = [operation for operation in oc.operation_select_by_acc(self.profileLineEdit.text())
                              if operation.date_time.month == int(self.month_filter_oper_combo.currentText())]
        operations_month = [operation.id for operation in operations_month]
        if self.year_filter_oper_combo.currentText() == "Год без фильтра":
            operations_year = oc.operation_select_by_acc(self.profileLineEdit.text())
        else:
            operations_year = [operation for operation in oc.operation_select_by_acc(self.profileLineEdit.text())
                              if operation.date_time.year == int(self.year_filter_oper_combo.currentText())]
        operations_year = [operation.id for operation in operations_year]

        operations_id = [operation_id for operation_id in operations_type if operation_id in operations_day and
                         operation_id in operations_month and operation_id in operations_year]
        operations = [oc.operation_select_by_id(oper_id) for oper_id in operations_id]
        self.operations_table.setHorizontalHeaderLabels(["Сумма", "Тип", "Дата и время"])
        self.operations_table.setRowCount(len(operations))

        row = 0
        for operation in operations:
            self.operations_table.setItem(row, 0, QTableWidgetItem(str(operation.summ)+'руб.'))
            self.operations_table.setItem(row, 1, QTableWidgetItem(operation.type))
            self.operations_table.setItem(row, 2, QTableWidgetItem(str(operation.date_time)))

            row += 1

    def menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('Файл')
        swap_act = QAction('Сменить аккаунт', self)
        swap_act.triggered.connect(self.swap_profiles)
        exit_act = QAction('Выход', self)
        exit_act.triggered.connect(self.close)
        file_menu.addAction(swap_act)
        file_menu.addAction(exit_act)
        help_menu = menu_bar.addMenu('Справка')
        about_action = QAction('О программе', self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def swap_profiles(self):
        self.wallet_layout.hide()
        self.main_layout.hide()
        self.re_balance_layout.hide()
        self.add_purchase_layout.hide()
        self.registry_layout.hide()
        self.enter_layout.show()
        self.setGeometry(860, 200, 600, 200)

    def show_about_dialog(self):
        about_text = ("Учет личных финансов\n" 
                     "Приложение для контроля денежных расходов.")
        QMessageBox.about(self, "О программе", about_text)

    def add_day_item(self, filter: QComboBox):
        filter.addItem("День без фильтра")
        for i in range(1, 32):
            filter.addItem(str(i))

    def add_month_item(self, filter: QComboBox):
        filter.addItem("Месяц без фильтра")
        for i in range(1, 13):
            filter.addItem(str(i))

    def add_year_item(self, filter: QComboBox):
        filter.addItem("Год без фильтра")
        for i in range(datetime.now().year, 1999, -1):
            filter.addItem(str(i))

    def edit_date(self):
        day = self.calendar.selectedDate().day()
        month = self.calendar.selectedDate().month()
        year = self.calendar.selectedDate().year()
        self.date_of_purch.setText('0'*(2-len(str(day)))+str(day) + "." + '0'*(2-len(str(month))) +
                                   str(month)+'.'+str(year))
