from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, TimeField, RadioField
from datetime import datetime
import os
import json
import requests


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
cs23 = Flask(__name__)
cs23.config['SECRET_KEY'] = 'your_secret_key'


def is_internet_available():
    try:
        requests.get("https://google.com", timeout=5)
        return True
    except requests.exceptions.ConnectionError:
        return False


class IncidentReportForm(FlaskForm):

    BARANGAY_CHOICES = [
        (None, 'Select Barangay'),
        ('adlaon', 'ADLAON'),
        ('agsungot', 'AGSUNGOT'),
        ('apas', 'APAS'),
        ('babag', 'BABAG'),
        ('bacayan', 'BACAYAN'),
        ('banilad', 'BANILAD'),
        ('basak_pardo', 'BASAK PARDO'),
        ('basak_san_nicolas', 'BASAK SAN NICOLAS'),
        ('binaliw', 'BINALIW'),
        ('bonbon', 'BONBON'),
        ('budla-an', 'BUDLA-AN (POB.)'),
        ('buhisan', 'BUHISAN'),
        ('bulacao', 'BULACAO'),
        ('buot-taup_pardo', 'BUOT-TAUP PARDO'),
        ('busay', 'BUSAY (POB.)'),
        ('calamba', 'CALAMBA'),
        ('cambinocot', 'CAMBINOCOT'),
        ('camputhaw', 'CAMPUTHAW'),
        ('capital_site', 'CAPITAL SITE'),
        ('carreta', 'CARRETA'),
        ('central', 'CENTRAL'),
        ('cogon_pardo', 'COGON PARDO'),
        ('cogon', 'COGON'),
        ('ramos', 'RAMOS'),
        ('day-as', 'DAY-AS'),
        ('duljo', 'DULJO'),
        ('ermita', 'ERMITA'),
        ('guadalupe', 'GUADALUPE'),
        ('guba', 'GUBA'),
        ('hippodromo', 'HIPPODROMO'),
        ('inayawan', 'INAYAWAN'),
        ('kalubihan', 'KALUBIHAN'),
        ('kalunasan', 'KALUNASAN'),
        ('kamagayan', 'KAMAGAYAN'),
        ('kasambagan', 'KASAMBAGAN'),
        ('kinasang-an_pardo', 'KINASANG-AN PARDO'),
        ('labangon', 'LABANGON'),
        ('lahug', 'LAHUG'),
        ('lorega', 'LOREGA (LOREGA SAN MIGUEL)'),
        ('lusaran', 'LUSARAN'),
        ('luz', 'LUZ'),
        ('mabini', 'MABINI'),
        ('mabolo', 'MABOLO'),
        ('malubog', 'MALUBOG'),
        ('mambaling', 'MAMBALING'),
        ('pahina_central', 'PAHINA CENTRAL'),
        ('pahina_san_nicolas', 'PAHINA SAN NICOLAS'),
        ('pamutan', 'PAMUTAN'),
        ('pardo', 'PARDO'),
        ('pari-an', 'PARI-AN'),
        ('paril', 'PARIL'),
        ('pasil', 'PASIL'),
        ('pit-os', 'PIT-OS'),
        ('pulangbato', 'PULANGBATO'),
        ('pung-ol-sibugay', 'PUNG-OL-SIBUGAY'),
        ('punta_princesa', 'PUNTA PRINCESA'),
        ('quiot_pardo', 'QUIOT PARDO'),
        ('sambag_i', 'SAMBAG I'),
        ('sambag_ii', 'SAMBAG II'),
        ('san_antonio', 'SAN ANTONIO'),
        ('san_jose', 'SAN JOSE'),
        ('san_nicolas_central', 'SAN NICOLAS CENTRAL'),
        ('san_roque', 'SAN ROQUE'),
        ('santa_cruz', 'SANTA CRUZ'),
        ('sapangdaku', 'SAPANGDAKU'),
        ('sawang_calero', 'SAWANG CALERO'),
        ('sinsin', 'SINSIN'),
        ('sirao', 'SIRAO'),
        ('suba', 'SUBA POB. (SUBA SAN NICOLAS)'),
        ('sudlon_i', 'SUDLON I'),
        ('sudlon_ii', 'SUDLON II'),
        ('t._padilla', 'T. PADILLA'),
        ('tabunan', 'TABUNAN'),
        ('tagbao', 'TAGBAO'),
        ('talamban', 'TALAMBAN'),
        ('taptap', 'TAPTAP'),
        ('tejero', 'TEJERO (VILLA GONZALO)'),
        ('tinago', 'TINAGO'),
        ('tisa', 'TISA'),
        ('to-ong_pardo', 'TO-ONG PARDO'),
        ('zapatera', 'ZAPATERA'),
    ]
    SEVERITY_CHOICES = [
        ('very_low', 'Very Low'),
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('very_high', 'Very High'),
    ]
    severity = RadioField('Severity', choices=SEVERITY_CHOICES)
    incident_type = SelectField('Incident Type', choices=[('fire', 'Fire'), ('accident', 'Accident'), ('medical', 'Medical Emergency')])
    date = DateField('Date')
    time = TimeField('Time')
    location = StringField('Location')
    barangay = SelectField('Barangay', choices=BARANGAY_CHOICES, default=None)
    description = TextAreaField('Description')


@cs23.route('/')
def index():
    form = IncidentReportForm()
    return render_template('incident_form.html', form=form)


@cs23.route('/submit_report', methods=['POST'])
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
            return jsonify({'success': True, 'message': 'Incident report submitted successfully.', 'severity_insights': severity_insights})
        else:
            print("No internet connection available")
            with open('incident_data.json', 'a') as f:
                f.write(json.dumps(incident_data) + '\n')

            # Show message about offline storage and severity insights
            return jsonify({'success': True, 'message': 'Incident report saved offline.', 'severity_insights': severity_insights})

    return jsonify({'success': False, 'errors': form.errors})


@cs23.route('/report.html')
def report():
    return render_template('report.html')

@cs23.route('/homepage.html')
def homepage():
    return render_template('homepage.html')

@cs23.route('/incident_form.html')
def incident_form():
    return render_template('incident_form.html')


if __name__ == '__main__':
    #cs23.run(debug=True)
    cs23.run(host='0.0.0.0', port=5000, debug=True)
