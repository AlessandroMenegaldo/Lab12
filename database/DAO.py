from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.retailer import Retailer


class DAO():
    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT  DISTINCT gr.Country 
                    from go_retailers gr  """

        cursor.execute(query)

        for row in cursor:
            result.append(row["Country"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT  DISTINCT YEAR(gds.`Date`) as years
                    from  go_daily_sales gds  """

        cursor.execute(query)

        for row in cursor:
            result.append(row["years"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getReatailers(country):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT *
                    FROM go_retailers gr 
                    WHERE gr.Country = %s """

        cursor.execute(query, (country,))

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result



    @staticmethod
    def getConnessioni(country, year, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT tab1.Retailer_code as ret1, tab2.Retailer_code as ret2, COUNT(*) as peso
                    FROM (SELECT gds.Retailer_code, gds.Product_number 
                            FROM go_daily_sales gds, go_retailers gr 
                            WHERE gds.Retailer_code = gr.Retailer_code AND YEAR(gds.`Date`)= %s and gr.Country = %s 
                            GROUP BY gds.Retailer_code, gds.Product_number ) as tab1, (SELECT gds.Retailer_code, gds.Product_number 
                            FROM go_daily_sales gds, go_retailers gr 
                            WHERE gds.Retailer_code = gr.Retailer_code AND YEAR(gds.`Date`)= %s and gr.Country = %s 
                            GROUP BY gds.Retailer_code, gds.Product_number ) as tab2
                    WHERE tab1.Retailer_code < tab2.Retailer_code and tab1.Product_number = tab2.Product_number
                    group BY tab1.Retailer_code, tab2.Retailer_code"""

        cursor.execute(query, (year,country,year,country,))

        for row in cursor:
            result.append(Connessione(idMap[row["ret1"]],idMap[row["ret2"]], row["peso"]))

        cursor.close()
        conn.close()
        return result


