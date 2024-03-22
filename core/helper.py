import sqlite3
from .doctor import *


def description_db(disease):
    conn=sqlite3.connect('description.db')
    cursor=conn.cursor()
    query = f"SELECT * FROM Description"
    cursor.execute(query)
    rows=cursor.fetchall()
    for row in rows:
        if row[0].strip()==disease:
            description=row
            break
    conn.close()
    description=list(description)
    return description[1]

def precaution_db(disease):
    conn=sqlite3.connect('precaution.db')
    cursor=conn.cursor()
    query = f"SELECT * FROM Disease"
    cursor.execute(query)
    rows=cursor.fetchall()
    for row in rows:
        if row[0].strip()==disease:
            precaution=row[1:]
            break
    precaution=list(precaution)
    conn.close()
    return precaution


def remedy_db(disease):
    conn=sqlite3.connect('remedy.db')
    cursor=conn.cursor()
    query = f"SELECT * FROM Remedy"
    cursor.execute(query)
    rows=cursor.fetchall()
    for row in rows:
        if row[0].strip()==disease:
            remedy=row[1:]
            break
    remedy=list(remedy)
    conn.close()
    return remedy

def test_db(disease):
    disease=disease[0].upper() + disease[1:]
    conn=sqlite3.connect('test.db')
    cursor=conn.cursor()
    query=f"SELECT * FROM Test"
    cursor.execute(query)
    rows=cursor.fetchall()
    test=[]
    for row in rows:
        if row[0].strip()==disease:
            test=row[1:]
            break
    conn.close()
    if test==None:
        return []
    if test:
        test=list(test)
    return test


def doctor_db(disease):
    conn=sqlite3.connect('Doctor.db')
    cursor=conn.cursor()
    query=f"SELECT * FROM Doctor"
    cursor.execute(query)
    rows=cursor.fetchall()
    for row in rows:
        if row[0].strip()==disease:
            doctor=row[1:]
            break
    doctor=list(doctor)
    doctor=doctor[0].split(',')
    doctor=doctor[0]
    conn.close()
    return doctor