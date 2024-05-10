from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCharFormat, QBrush, QColor
from PyQt5.QtWidgets import QApplication, QCalendarWidget


class CalendarWidget(QCalendarWidget):
    def __init__(self, *args, **kwargs):
        super(CalendarWidget, self).__init__(*args, **kwargs)

        # Вертикальный заголовок. The header is hidden.
        self.setVerticalHeaderFormat(self.NoVerticalHeader)

        # Изменить цвета субботы и воскресенья
        fmtGreen = QTextCharFormat()
        fmtGreen.setForeground(QBrush(Qt.green))
        self.setWeekdayTextFormat(Qt.Saturday, fmtGreen)
        fmtOrange = QTextCharFormat()
        fmtOrange.setForeground(QBrush(QColor(252, 140, 28)))
        self.setWeekdayTextFormat(Qt.Sunday, fmtOrange)
        self.show()

    def sel_date(self):
        return self.selectedDate()



StyleSheet = '''
/* Верхняя область навигации                            */
#qt_calendar_navigationbar {
    background-color: rgb(0, 188, 212);
    min-height: 100px;
}

/*  Кнопка последнего месяца и кнопка следующего месяца 
    (имя объекта найдено из источника/objectName)       */
#qt_calendar_prevmonth, #qt_calendar_nextmonth {
    border: none;                     /* убрать границу */
    margin-top: 64px;
    color: white;
    min-width: 36px;
    max-width: 36px;
    min-height: 36px;
    max-height: 36px;
    border-radius: 18px;            /* выглядит как эллипс */
    font-weight: bold;              /* шрифт полужирный    */

    /* Удалить стандартное изображение клавиши со стрелкой. 
       Вы также можете настроить                           */
    qproperty-icon: none;    
    background-color: transparent; /* Цвет фона прозрачный */
}

#qt_calendar_prevmonth {
    qproperty-text: "<";         /* Изменить текст кнопки  */
}

#qt_calendar_nextmonth {
    qproperty-text: ">";
}

#qt_calendar_prevmonth:hover, #qt_calendar_nextmonth:hover {
    background-color: rgba(225, 225, 225, 100);
}

#qt_calendar_prevmonth:pressed, #qt_calendar_nextmonth:pressed {
    background-color: rgba(235, 235, 235, 100);
}

/*  год, месяц                                                */
#qt_calendar_yearbutton, #qt_calendar_monthbutton {
    color: white;
    margin: 18px;
    min-width: 60px;
    border-radius: 30px;
}
#qt_calendar_yearbutton:hover, #qt_calendar_monthbutton:hover {
    background-color: rgba(225, 225, 225, 100);
}
#qt_calendar_yearbutton:pressed, #qt_calendar_monthbutton:pressed {
    background-color: rgba(235, 235, 235, 100);
}

/* Поле ввода года                                                        */
#qt_calendar_yearedit {
    min-width: 50px;
    color: white;
    background: transparent;         /* Сделать фон окна ввода прозрачным */
}
#qt_calendar_yearedit::up-button {   /* Кнопка вверх                      */
    width: 20px;
    subcontrol-position: right;      
}
#qt_calendar_yearedit::down-button { /* Кнопка вниз     */
    width: 20px;
    subcontrol-position: left;       
}

/* меню выбора месяца                                          */
CalendarWidget QToolButton QMenu {
     background-color: white;
}
CalendarWidget QToolButton QMenu::item {
    padding: 10px;
}
CalendarWidget QToolButton QMenu::item:selected:enabled {
    background-color: rgb(230, 230, 230);
}
CalendarWidget QToolButton::menu-indicator {
/*  image: none;        Удалите маленькую стрелку под выбором месяца !!! */
    subcontrol-position: right center;                /* Право по центру */
}

/* ниже календарной формы */
#qt_calendar_calendarview {
    outline: 0px;                                 /* Удалить выделенную пунктирную рамку */
    selection-background-color: rgb(0, 188, 212); /* Выберите цвет фона */
}
'''


if __name__ == '__main__':
    app = QApplication([])
    window = CalendarWidget()
    app.exec()
