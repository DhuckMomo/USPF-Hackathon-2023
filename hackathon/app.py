from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, TimeField, RadioField
from datetime import datetime
import os
import json
import requests
from form import IncidentReportForm


#severity simple AI
def analyze_severity(severity):
    severity_messages = {
        'very_low': "The incident is considered very low severity. It may not require immediate attention.",
        'low': "The incident is considered low severity. It may not require immediate attention.",
        'medium': "The incident is of medium severity. Please address it promptly.",
        'high': "The incident is of high severity. Immediate attention and action are recommended.",
        'very_high': "The incident is considered very high severity. Immediate action is required.",
    }
    return severity_messages.get(severity, "Severity not specified.")

#Cebu Sentinel
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'


def is_internet_available():
    try:
        requests.get("https://google.com", timeout=5)
        return True
    except requests.exceptions.ConnectionError:
        return False



@app.route('/')
def index():
    form = IncidentReportForm()
    # Mock severity_insights for demonstration purposes
    severity_insights = "This is a sample severity insight."
    return render_template('incident_form.html', form=form, severity_insights=severity_insights)
    #return render_template('incident_form.html', form=form)




@app.route('/submit_report', methods=['POST'])
def submit_report():
    form = IncidentReportForm()
    severity_insights = analyze_severity(form.severity.data)
    if form.validate_on_submit():
        try:
            date_time = datetime.combine(form.date.data, form.time.data)
        except ValueError as e:
            return jsonify({'success': False, 'errors': {'date_time': [str(e)]}})

        incident_data = {
            'incident_type': form.incident_type.data,
            'date_time': date_time,
            'location': form.location.data,
            'barangay': form.barangay.data,
            'description': form.description.data
        }

        if is_internet_available():
            print("Internet connection is available")
            #  logic for submitting data to server here
            # ...

            
            return redirect(url_for('aftersubmit'))
        else:
            print("No internet connection available")
            with open('incident_data.json', 'a') as f:
                f.write(json.dumps(incident_data) + '\n')

            # Show message about offline storage and severity insights
            return jsonify({'success': True, 'message': 'Incident report saved offline.', 'severity_insights': severity_insights})

    return jsonify({'success': False, 'errors': form.errors})


@app.route('/report.html')
def report():
    return render_template('report.html')

@app.route('/homepage.html')
def homepage():
    return render_template('homepage.html')

@app.route('/incident_form.html')
def incident_form():
    form = IncidentReportForm()
    return render_template('incident_form.html', form=form)

@app.route('/aboutus.html')
def aboutus():
    return render_template('aboutus.html',)

@app.route('/aftersubmit.html')
def aftersubmit():
    return render_template('aftersubmit.html',)


if __name__ == '__main__':
    #cs23.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
