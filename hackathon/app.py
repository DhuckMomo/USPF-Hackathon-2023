from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, TimeField
from datetime import datetime
import os
import json
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'


def is_internet_available():
    try:
        requests.get("https://google.com", timeout=5)
        return True
    except requests.exceptions.ConnectionError:
        return False


class IncidentReportForm(FlaskForm):
    incident_type = SelectField('Incident Type', choices=[('fire', 'Fire'), ('accident', 'Accident'), ('medical', 'Medical Emergency')])
    date = DateField('Date')
    time = TimeField('Time')
    location = StringField('Location')
    description = TextAreaField('Description')


@app.route('/')
def index():
    form = IncidentReportForm()
    return render_template('incident_form.html', form=form)


@app.route('/submit_report', methods=['POST'])
def submit_report():
    form = IncidentReportForm()
    if form.validate_on_submit():
        try:
            date_time = datetime.combine(form.date.data, form.time.data)
        except ValueError as e:
            return jsonify({'success': False, 'errors': {'date_time': [str(e)]}})

        incident_data = {
            'incident_type': form.incident_type.data,
            'date_time': date_time,
            'location': form.location.data,
            'description': form.description.data
        }

        if is_internet_available():
            print("Internet connection is available")
            #  logic for submitting data to server here
            # ...
            pass
        else:
            print("No internet connection available")
            with open('incident_data.json', 'a') as f:
                f.write(json.dumps(incident_data) + '\n')

            # Show message about offline storage
            return jsonify({'success': True, 'message': 'Incident report saved offline.'})

    return jsonify({'success': False, 'errors': form.errors})



if __name__ == '__main__':
    app.run(debug=True)
