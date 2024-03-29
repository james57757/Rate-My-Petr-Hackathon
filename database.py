import os
import psycopg2
from dotenv import load_dotenv
import time
import math

load_dotenv()

class database:
    
    def __init__(self):
        self.conn = psycopg2.connect(
        host="dpg-cmrarri1hbls73fodgmg-a.oregon-postgres.render.com",
        #postgres://root:Q5gq7quc1Kq6MiYPk2Z2I6uSaXtbE4dQ@dpg-cmrarri1hbls73fodgmg-a.oregon-postgres.render.com/petr
        database="petr",
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD'),
        port="5432")
        self.cur = self.conn.cursor()
        
    

    def insertRating(self, class_id, enjoyment_rating, difficulty_rating, comment, grade, instructor_id):
        self.cur.execute('INSERT INTO ratings(class_id, enjoyment_rating, difficulty_rating, comment, \
                         grade, instructor_id) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id', (class_id, enjoyment_rating, difficulty_rating, comment,
                                                           grade, instructor_id))
        inserted_id = self.cur.fetchone()[0]
        self.conn.commit()
        return inserted_id
    
    def updateRating(self, class_id, enjoyment_rating, difficulty_rating, comment, grade, instructor_id):
        self.cur.execute('UPDATE ratings \
                        SET enjoyment_rating = %s, \
                            difficulty_rating = %s, \
                            comment = %s, \
                            grade = %s, \
                            instructor_id = %s \
                        WHERE class_id = %s', (enjoyment_rating, difficulty_rating, comment, grade, instructor_id, class_id))
        self.conn.commit()
    
    def deleteRating(self, rating_id):
        self.cur.execute('DELETE FROM ratings \
                     WHERE id = %s', (rating_id,))
        self.conn.commit()
    
    def getClassRatings(self, class_id):
        self.cur.execute('SELECT * FROM ratings WHERE class_id = %s', (class_id,))
        rating_records = self.cur.fetchall()

        return [{"id": record[0], "class_id": record[1], "enjoyment_rating": record[2], "difficulty_rating": record[3],
                 "comment": record[4], "grade": record[5], "added_timestamp": record[6], "instructor_id": record[7]} for record in rating_records]
    
    def getInstructorRatings(self, instructor_id):
        self.cur.execute('SELECT * FROM ratings WHERE instructor_id = %s', (instructor_id,))
        rating_records = self.cur.fetchall()
        return [{"id": record[0], "class_id": record[1], "enjoyment_rating": record[2], "difficulty_rating": record[3],
                 "comment": record[4], "grade": record[5], "added_timestamp": record[6], "instructor_id": record[7]} for record in rating_records]

    def getDepartmentRatings(self, departmentName):
        self.cur.execute(f"SELECT class_id, avg(difficulty_rating), avg(enjoyment_rating), count(id) FROM ratings WHERE class_id like '{departmentName}%' GROUP BY class_id")
        rating_records = self.cur.fetchall()
        return {record[0] : {"difficulty_rating": round(float(record[1]), 2), "enjoyment_rating": round(float(record[2]), 2), "count": record[3]} for record in rating_records}
    
    def getClassCodeRatings(self, classCode):
        self.cur.execute(f"SELECT class_id, avg(difficulty_rating), avg(enjoyment_rating), count(id) FROM ratings WHERE class_id like '%{classCode}' GROUP BY class_id")
        rating_records = self.cur.fetchall()
        return {record[0] : {"difficulty_rating": round(float(record[1]), 2), "enjoyment_rating": round(float(record[2]), 2), "count": record[3]} for record in rating_records}

    def close(self):
        self.cur.close()
        self.conn.close()
 

