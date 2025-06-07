from flask import Flask, render_template, request
import pandas as pd
import os
from datetime import datetime
from services.dummyApi import dummyAPIendPoint

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    voltages = ['220kV', '400kV', '765kV']
    result_rows = []
    selected_voltage = None
    start_datetime = None
    end_datetime = None
    error_message = None
    #dataVal = None  # ✅ define before use

    if request.method == 'POST':
        selected_voltage = request.form.get('voltage')
        start_datetime = request.form.get('start_datetime')
        end_datetime = request.form.get('end_datetime')

        try:
            # ✅ convert to datetime early
            start_dt = datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M")
            end_dt = datetime.strptime(end_datetime, "%Y-%m-%dT%H:%M")

            # ✅ now call the dummy API using datetime objects
            api_values = dummyAPIendPoint('abcd', start_dt, end_dt)

            # ✅ load the Excel file
            excel_file_name = f"{start_dt.date()}.xlsx"
            excel_file_path = os.path.join("D:/SPCE/BTECH PROJECT/new website draft", excel_file_name)

            if not os.path.exists(excel_file_path):
                error_message = f"⚠️ No Excel file found for {start_dt.date()}."
            else:
                df = pd.read_excel(excel_file_path)
                if 'Event Time' in df.columns:
                    df['Event Time'] = pd.to_datetime(df['Event Time'], errors='coerce')
                    df = df[(df['Event Time'] >= start_dt) & (df['Event Time'] <= end_dt)]
                result_rows = df.to_dict(orient='records')

        except Exception as e:
            error_message = f"⚠️ Error: {e}"

    # ✅ always pass context to the template
    return render_template('index5.html',
                           voltages=voltages,
                           selected_voltage=selected_voltage,
                           start_datetime=start_datetime,
                           end_datetime=end_datetime,
                           result=result_rows,
                           error=error_message)
                           #api_values=dataVal)

if __name__ == '__main__':
    app.run(debug=True)
