from sqlalchemy import create_engine

class Database:
    def connection(self):
        # Corrige la cadena de conexión si tu base es 'pragma'
        engine = create_engine("mysql+mysqlconnector://root:1234@localhost/pragma")
        return engine

if __name__ == "__main__":
    db = Database()
    engine = db.connection()
    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT VERSION();")
            print("Conexión exitosa. Versión de MySQL:", result.fetchone())
    except Exception as e:
        print("Error de conexión:", e)