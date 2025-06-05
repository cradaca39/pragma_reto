import os
from flask import request, Blueprint, current_app
from werkzeug.utils import secure_filename
import pandas as pd
from sqlalchemy import create_engine
from database_connect import Database
from sqlalchemy import text

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'result')
ALLOWED_EXTENSIONS = {'csv'}

transactions = Blueprint("transactions", __name__)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@transactions.post('/transactions')
def create_transactions():
    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if 'file' not in request.files:
        return ('No file part', 400)
    file = request.files['file']
    if file.filename == '':
        return ('No selected file', 400)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)  # <-- Asegura que la carpeta existe
        file.save(save_path)
        try:
            insert_data(save_path)
            return 'File uploaded and data inserted successfully', 200
        except Exception as ex:
            return (f'Error inserting data: {ex}', 500)
    else:
        return ('File not allowed', 400)

def insert_data(filepath):
    df = pd.read_csv(filepath, delimiter=",", header=None)
    df.columns = ["time", "price", "user_id"]
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    db = Database()
    engine = db.connection()
    df.to_sql('transactions', con=engine, if_exists='append', index=False)
    print("insert transactions sucessful")
    update_stats(engine, df)  # <-- Actualiza las estadísticas aquí

def update_stats(engine, df):
    prices = df['price'].dropna().astype(float)
    if prices.empty:
        return

    count = len(prices)
    total = prices.sum()
    min_price = prices.min()
    max_price = prices.max()

    with engine.begin() as conn:
        result = conn.execute(text("SELECT total_count, total_sum, total_min, total_max FROM transactions_stats WHERE id=1"))
        row = result.fetchone()
        if row is None:
            conn.execute(
                text("INSERT INTO transactions_stats (id, total_count, total_sum, total_min, total_max) VALUES (1, :count, :total, :min, :max)"),
                {"count": count, "total": total, "min": min_price, "max": max_price}
            )
        else:
            prev_count, prev_sum, prev_min, prev_max = row
            new_count = prev_count + count
            new_sum = prev_sum + total
            new_min = min(prev_min, min_price) if prev_min is not None else min_price
            new_max = max(prev_max, max_price) if prev_max is not None else max_price
            conn.execute(
                text("""
                    UPDATE transactions_stats
                    SET total_count=:count, total_sum=:total, total_min=:min, total_max=:max
                """),
                {"count": new_count, "total": new_sum, "min": new_min, "max": new_max}
            )

@transactions.get('/transactions/stats')
def get_stats():
    db = Database()
    engine = db.connection()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT total_count, total_sum, total_min, total_max FROM transactions_stats WHERE id=1"))
        row = result.fetchone()
        if row:
            total_count, total_sum, total_min, total_max = row
            avg = total_sum / total_count if total_count else 0
            return {
                "total_count": total_count,
                "average_price": avg,
                "min_price": total_min,
                "max_price": total_max
            }, 200
        else:
            return {"error": "No stats found"}, 404