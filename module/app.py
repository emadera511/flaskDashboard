from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
from faker import Faker
import io
import base64

app = Flask(__name__, template_folder='../app', static_folder='../app')

def generate_fake_data():
    fake = Faker()
    data = {
        'Name': [fake.name() for _ in range(100)],
        'Age': [fake.random_int(min=18, max=80) for _ in range(100)],
        'Salary': [fake.random_int(min=30000, max=120000) for _ in range(100)],
        'City': [fake.city() for _ in range(100)],
        'Date': [fake.date_this_decade() for _ in range(100)]
    }
    return pd.DataFrame(data)

df = generate_fake_data()

@app.route('/')
def index():
    columns = df.columns
    return render_template('index.html', columns=columns)

@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    chart_type = request.form.get('chart_type')
    x_axis = request.form.get('x_axis')
    y_axis = request.form.get('y_axis')
    
    fig, ax = plt.subplots()
    
    if chart_type == 'bar':
        df.plot.bar(x=x_axis, y=y_axis, ax=ax)
    elif chart_type == 'line':
        df.plot.line(x=x_axis, y=y_axis, ax=ax)
    elif chart_type == 'donut':
        df.groupby(x_axis)[y_axis].sum().plot.pie(ax=ax, autopct='%1.1f%%', startangle=90, wedgeprops={'width':0.3})
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)
    
    return render_template('chart.html', chart_url=chart_url)