from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()

class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.string_field

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def today_tasks():
    today = datetime.today()
    rows = session.query(Table).filter(Table.deadline == today).all()
    if len(rows) == 0:
        print(f"Today {today.month} {today.strftime('%b')}:")
        print("Nothing to do!")
    else:
        print(f"Today: {today.day} {today.strftime('%b')}:")
        i = 0
        for row in rows:
            print(f"{i + 1}. ", row.task)
            i += 1

def week_tasks():
    today = datetime.today()
    i = 0
    while i < 7:
        day = today + timedelta(days=i)
        rows = session.query(Table).filter(Table.deadline == day.date()).all()
        if len(rows) == 0:
            print(f"{day_of_week[day.weekday()]} {day.day} {day.strftime('%b')}:")
            print("Nothing to do!")
            i += 1
            print("")
        else:
            print(f"{day_of_week[day.weekday()]} {day.day} {day.strftime('%b')}:")
            j = 0
            for row in rows:
                print(f"{j + 1}. ", row.task)
                j += 1
            i += 1
            print("")

def all_tasks():
    rows = session.query(Table).all()
    if len(rows) == 0:
        print("Today:\nNothing to do!")
    else:
        print("Today:")
        i = 0
        for row in rows:
            print(f"{i + 1}. ", row.task)
            i += 1

def missed_tasks():
    rows = session.query(Table).filter(Table.deadline < datetime.today()).order_by(Table.deadline).all()
    if len(rows) == 0:
        print("Missed tasks:\nNothing is missed!")
    else:
        print("Missed tasks:")
        i = 0
        for row in rows:
            print(f"{i + 1}. ", row.task)
            i += 1

def add_task():
    task = input("Enter task\n")
    time = input("Enter deadline\n")
    print("The task has been added!")
    new_row = Table(task=task, deadline=datetime.strptime(time, '%Y-%m-%d').date())
    session.add(new_row)
    session.commit()
    return

def delete_task():
    rows = session.query(Table).order_by(Table.deadline).all()
    if len(rows) == 0:
        print("Nothing to delete")
    else:
        print("Chose the number of the task you want to delete:")
        i = 0
        for row in rows:
            print(f"{i + 1}. ", row.task)
            i += 1
        order = int(input())
        session.delete(rows[order - 1])
        session.commit()
        print("The task has been deleted!")



day_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

while True:
    print("")
    print("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
    order = input()
    if order == "1":
        today_tasks()
    elif order == "2":
        week_tasks()
    elif order == "3":
        all_tasks()
    elif order == "4":
        missed_tasks()
    elif order == "5":
        add_task()
    elif order == "6":
        delete_task()
    elif order == "0":
        break
    else:
        continue
