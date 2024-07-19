"""
Write tests for classes in 2_python_part_2/task_classes.py (Homework, Teacher, Student).
Check if all methods working correctly.
Also check corner-cases, for example if homework number of days is negative.
"""

import datetime

from task_classes import Homework, Teacher, Student


def test_homework_is_active():
    homework = Homework('text', 1)
    assert homework.is_active() is True, 'Homework is active'

    homework = Homework('text', -12)
    assert homework.is_active() is False, 'Homework is not active'


    homework = Homework('text', 100)
    assert homework.is_active() is True, 'Homework is active'


def test_student_do_homework():
    student = Student('John', 'Doe')
    homework = Homework('text', 1)
    assert student.do_homework(homework) == homework, 'Homework is active'

    homework = Homework('text', -1)
    assert student.do_homework(homework) is None, 'Homework is not active'

    homework = Homework('text', 100)
    assert student.do_homework(homework) == homework, 'Homework is active'


def test_teacher_create_homework():
    teacher = Teacher('John', 'Doe')
    homework = teacher.create_homework('text', 1)
    assert homework.text == 'text', 'Homework text is correct'
    assert homework.deadline == datetime.timedelta(days=1), 'Homework deadline is correct'

    homework = teacher.create_homework('text', -1)
    assert homework.text == 'text', 'Homework text is correct'
    assert homework.deadline == datetime.timedelta(days=-1), 'Homework deadline is correct'

    homework = teacher.create_homework('text', 100)
    assert homework.text == 'text', 'Homework text is correct'
    assert homework.deadline == datetime.timedelta(days=100), 'Homework deadline is correct'

    homework = teacher.create_homework('text', 100)
    assert homework.created + homework.deadline > datetime.datetime.now(), 'Homework deadline is correct'




if __name__ == '__main__':
    test_student_do_homework()
    test_teacher_create_homework()
    test_homework_is_active()
