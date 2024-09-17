#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    __table_args__ = (
        PrimaryKeyConstraint(
            'id',
            name='id_pk'),
        UniqueConstraint(
            'email',
            name='unique_email'),
        CheckConstraint(
            'grade BETWEEN 1 AND 12',
            name='grade_between_1_and_12')
    )

    Index('index_name', 'name')

    id = Column(Integer())
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default=datetime.now())

    def __repr__(self):
        return f"Student {self.id}: " \
            + f"{self.name}, " \
            + f"Grade {self.grade}"

if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    # use our engine to configure a 'Session' class
    Session = sessionmaker(bind=engine)
    # use 'Session' class to create 'session' object
    session = Session()

    albert_einstein = Student(
        name="Albert Einstein",
        email="albert.einstein@zurich.edu",
        grade=6,
        birthday=datetime(
            year=1879,
            month=3,
            day=14
        ),
    )

    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(
            year=1912,
            month=6,
            day=23
        ),
    )

    # session.add(albert_einstein)
    # session.commit()

    #print(f"New student ID is {albert_einstein.id}.")

    session.bulk_save_objects([albert_einstein, alan_turing]) #bulk_save_objects() (used to save multiple objects) does not associate the records with the session, so we don't update our records' IDs but session.add() does.
    session.commit()

    # print(f"New student ID is {albert_einstein.id}.")
    # print(f"New student ID is {alan_turing.id}.")

    students = session.query(Student)    
    print([student for student in students])

    #or use the .all()
    #students = session.query(Student).all()
    #print(students)

    #To retrieve certain columns only, we specify it as an argument in the query method. Query returns records as a tuple
    names = [name for name in session.query(Student.name)]

    print(names)

    #the order_by() method allows us to sort by any column
    students_by_name = [student for student in session.query(
            Student.name).order_by(
            Student.name)]

    print(students_by_name)

    #sort in descending order of student grades
    students_by_grade_desc = [student for student in session.query(
            Student.name, Student.grade).order_by(
            desc(Student.grade))]

    print(students_by_grade_desc)
    
    #to limit to the first record
    oldest_student = [student for student in session.query(
            Student.name, Student.birthday).order_by(
            desc(Student.grade)).limit(1)]

    print(oldest_student)

    #or use first() to provide a limit
    oldest_student_one = session.query(
            Student.name, Student.birthday).order_by(
            desc(Student.grade)).first()

    print(oldest_student_one)
    
    #func from sqlalchemy gives us access to common SQL operations through functions like sum() and count()
    student_count = session.query(func.count(Student.id)).first()

    print(student_count)

    #to filter records use:
    query = session.query(Student).filter(Student.name.like('%Alan%'),
        Student.grade == 11)

    for record in query:
        print(record.name)

    #To update data, we can use python to modify obj. directly and commiting changes through the session as shown
    for student in session.query(Student):
        student.grade += 1

    session.commit()

    print([(student.name,
        student.grade) for student in session.query(Student)])

    #Or we can use the update() method without creating obj. beforehand
    session.query(Student).update({
        Student.grade: Student.grade + 1
    })

    print([(
        student.name,
        student.grade
    ) for student in session.query(Student)])

    #delete record from db using the delete() method
    #to delete and obj. in memory, use delete() on obj in session.
    query = session.query(
        Student).filter(
            Student.name == "Albert Einstein")        

    # retrieve first matching record as object
    albert_einstein = query.first()

    # delete record
    session.delete(albert_einstein)
    session.commit()

    # try to retrieve deleted record
    albert_einstein = query.first()

    print(albert_einstein)

    #or call the delete() method from query instead if there is no single obj. for deletion
    #this deletes all records returned by query
    query = session.query(
        Student).filter(
            Student.name == "Albert Einstein")

    query.delete()

    albert_einstein = query.first()

    print(albert_einstein)