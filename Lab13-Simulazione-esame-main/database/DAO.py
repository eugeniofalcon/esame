from database.DB_connect import DBConnect
from model.Neighbors import Neighbor
from model.Sighting import Sighting
from model.States import State

class DAO():

    @staticmethod
    def getStates():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM state"

        cursor.execute(query, ())

        for row in cursor:
            result.append(State(row["id"], row["Name"], row["Capital"], row["Lat"], row["Lng"], row["Area"], row["Population"], row["Neighbors"]))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getSighting():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM sighting order by `datetime` asc"

        cursor.execute(query, ())

        for row in cursor:
            result.append(Sighting(row["id"], row["datetime"], row["city"], row["state"], row["country"], row["shape"], row["duration"], row["duration_hm"], row["comments"], row["date_posted"], row["latitude"], row["longitude"]))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getNeighbors():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM neighbor"

        cursor.execute(query, ())

        for row in cursor:
            result.append(Neighbor(row["state1"], row["state2"]))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getShapes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT DISTINCT(shape) FROM sighting"

        cursor.execute(query, ())

        for row in cursor:
            result.append(row["shape"])

        cursor.close()
        conn.close()
        return result
    
    @staticmethod
    def getAges():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT DISTINCT YEAR(datetime) as year FROM sighting ORDER BY year"

        cursor.execute(query, ())

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result
    
    @staticmethod
    def getAllWeightedNeigh(year,shape):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT n.state1, n.state2 , count(*) as N
                    FROM sighting s , neighbor n 
                    where year(s.`datetime`) = %s
                    and s.shape = %s
                    and (s.state = n.state1 or s.state = n.state2 )
                    and n.state1 < n.state2
                    group by n.state1 , n.state2 """

        cursor.execute(query, (year,shape))

        for row in cursor:
            result.append((row['state1'],row['state2'], row["N"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSightingByState():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT DISTINCT state FROM sighting WHERE state IS NOT NULL"

        cursor.execute(query, ())

        for row in cursor:
            result.append(row["state"])

        cursor.close()
        conn.close()
        return result
