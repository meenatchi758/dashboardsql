from flask import Flask, render_template
import pandas as pd
import json
import pymysql  # ✅ You’re using MySQL now

app = Flask(__name__)

def get_data():
    conn = pymysql.connect(
        host="localhost",
        user="root",         # 🔁 Replace with your MySQL username
        password="Meena@vts123",     # 🔁 Replace with your MySQL password
        database="dashboard_db"        # 🔁 Replace with your MySQL database name
    )
    df = pd.read_sql_query("SELECT * FROM sales", conn)
    df['date'] = pd.to_datetime(df['date']).dt.date
    conn.close()
    return df


@app.route('/')
def dashboard():
    df = get_data()

    pie_data = df.groupby('category')['revenue'].sum().reset_index()
    line_data = df.groupby('date')['revenue'].sum().reset_index()

    return render_template("dashboard.html",
        table=df.to_html(classes="table table-bordered", index=False),
        pie_labels=json.dumps(list(pie_data['category'])),
        pie_values=json.dumps(list(pie_data['revenue'])),
        line_labels=json.dumps([d.strftime("%Y-%m-%d") for d in line_data['date']]),
        line_values=json.dumps(list(line_data['revenue']))
    )

if __name__ == '__main__':
    app.run(debug=True)
