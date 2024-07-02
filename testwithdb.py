import pyodbc
from flask import Flask, render_template, request, redirect, session
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.validators import InputRequired, Length, Regexp, NumberRange
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField, SelectField, RadioField, HiddenField, StringField, IntegerField, FloatField, DateField, DecimalField, SelectMultipleField, TextAreaField, FileField, FormField
from datetime import datetime
import os
from werkzeug.utils import secure_filename


BASE_PATH = 'D:\\'
UPLOAD_FOLDER = os.path.join(BASE_PATH, 'images')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


nonconf_options = [
    "Touch/Pressure Marks",
    "Rotten",
    "Physical Damage",
    "Spoilage",
    "Bad Smell",
    "Skin Discolorations",
    "Raw",
    "Over Ripe",
    "Size Variations",
    "Pest Infestation",
    "Internal Discolorations",
    "Fungus Infestation",
    "Wilted/Soggy",
    "Shape Variations",
    "Sour Taste",
    "Less/No Flavor",
    "Physical Contaminant",
    "Bruise Marks",
    "Insect Bites",
    "Excessive Skin Marks",
    "Color Variations",
    "Texture Defects",
    "Melted",
    "Vacuum Loss",
    "Torn",
    "Packaging Defects",
    "Expired",
]
# def connect_to_mssql():
#     server = ''
#     database = ''
#     username = ''
#     password = ''

#     try:
#         conn = pyodbc.connect(
#             f"DRIVER={{SQL Server Native Client 11.0}};SERVER={server};DATABASE={database};UID={username};PWD={password}")
#         return conn
#     except pyodbc.Error as ex:
#         print("Database connection error:", ex)
#         return None
   
class testform(FlaskForm):
    id_field = HiddenField()
    reportno = StringField('Report no:', [ InputRequired(), Length(min=1, max=50, message="Invalid ")])
    product = StringField('ProductName:', [ InputRequired(), Regexp(r'^[A-Za-z\s\-\']+$', message="Invalid "),
        Length(min=1, max=50, message="Invalid ")
        ])
    Supplier = SelectField('Choose supplier', [ InputRequired()],
        choices=[ ('a', 'A'),('b', 'B'),('c', 'C'),('other', 'Other') ])
    DOR = DateField("Date of Receiving", validators=[InputRequired()], format='%Y-%m-%d')
    DOI = DateField("Date of Inspection", validators=[InputRequired()], format='%Y-%m-%d')
    TruckTemp = DecimalField(' Truck Temperature in degree Celsius', [ InputRequired(), NumberRange(min=-999, max=999, message="Invalid range")])
    ProdTemp = DecimalField('Product Temperature in degree Celsius', [ InputRequired(), NumberRange(min=-999, max=999, message="Invalid range")])
    
    NumOfBox = IntegerField('Number Of Boxes', [ InputRequired(), NumberRange(min=0, max=999, message="Invalid range")])
    Wastage = IntegerField('Wastage in Kgs', [ InputRequired(), NumberRange(min=0, max=999, message="Invalid range")])

    NonConf = SelectMultipleField('Nature of Non-conformance:', [InputRequired()], choices=nonconf_options)

    
    LOC = SelectField('Location', [ InputRequired()],choices=[ ('a', 'A'),('b', 'B'),('c', 'C'),('other', 'Other')])
    contawbno = IntegerField('CONT/AWB No:', [ InputRequired(),NumberRange(min=1, max=999, message="Invalid range")])
    InspectorName = StringField('Name of inspector', [ InputRequired(), Regexp(r'^[A-Za-z\s\-\']+$', message="Invalid "),
        Length(min=1, max=50, message="Invalid ")
        ])
    
    Remarks = TextAreaField("Remarks:", validators=[validators.Optional()])
    updated = HiddenField()
    submit = SubmitField('Next')



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SECRET_KEY'] = 'secret123344556'

@app.route('/', methods=['GET', 'POST'])
def index():
    
    form1 = testform()
    if form1.validate_on_submit():
        reportno = request.form['reportno']
        product = request.form['product']
        Supplier = request.form['Supplier']
        DOR = datetime.strptime(request.form['DOR'], '%Y-%m-%d').date()  
        DOI = datetime.strptime(request.form['DOI'], '%Y-%m-%d').date()  
        TruckTemp = request.form.get('TruckTemp')  
        ProdTemp = request.form.get('ProdTemp')  
        
        NumOfBox = request.form['NumOfBox']
        Wastage = request.form['Wastage']
        selected_nonconf = []
        for option in form1.NonConf.data:
            selected_nonconf.append(option)  # This returns a list of selected values
        liststring = ",".join(str(x) for x in selected_nonconf)
        LOC = request.form['LOC']
        contawbno = request.form['contawbno']
        InspectorName = request.form['InspectorName']
        Remarks = request.form.get('Remarks')
        # return render_template('index.html.j2', form=form1, message='Data saved successfully!')
    
        # try:
        #     conn = connect_to_mssql()
        #     cursor = conn.cursor()
        #     # Insert data into the table
        #     cursor.execute("""
        #         INSERT INTO bkformtest5(reportno, product, Supplier, DOR, DOI, TruckTemp, ProdTemp, NumOfBox, Wastage, NonConf, LOC, contawbno,InspectorName, Remarks)
        #         VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        #     """, (reportno, product, Supplier, DOR, DOI, TruckTemp, ProdTemp, NumOfBox, Wastage, liststring, LOC, contawbno,InspectorName, Remarks))
        #     conn.commit()

        #     # return render_template('deviation_table.html.j2', form1=form1, selected_nonconf=selected_nonconf, reportno = reportno)
            

        # except Exception as ex:
        #     print("Error saving data:", ex)
        #     return 'Error: Data could not be saved.'
        # finally:
        #     if conn:
        #         conn.close()
        

        session['reportno'] = reportno
        return render_template('deviation_table.html.j2', form1=form1, selected_nonconf=selected_nonconf, reportno = reportno)
    

    return render_template('index.html.j2', form1=form1)


@app.route('/deviation_table', methods=['GET', 'POST'])
def deviation_table():


    if request.method == 'POST':
        # Upload file logic
        if 'uploaded-file' in request.files:
            uploaded_file = request.files['uploaded-file']
            if uploaded_file.filename != '':
                filename = secure_filename(uploaded_file.filename)
                uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    reportno = session.get('reportno')
    
    form_data = request.form

    form_dict = form_data.to_dict()
    
    import pandas as pd
    df = pd.DataFrame.from_dict(form_dict, orient= 'index')
    df.reset_index(inplace=True)
    df[["Type", "box_ind"]] = df["index"].str.split('_', expand=True)
    df['box_ind'] = df['box_ind']
    df = df[["box_ind","Type",0]]
    
    df = df.pivot(index='Type', values=0, columns='box_ind').reset_index()
    weight_row_index = df[df['Type'] == 'weight'].index[0]
    df = df.reindex([weight_row_index] + list(df.index.difference([weight_row_index])))
    df["ref_num"] = reportno 
    df=df.rename(columns ={'1': 'box 1', '2': 'box 2', '3': 'box 3'})
    
    df = df[['Type', 'box 1', 'box 2', 'box 3', 'ref_num']]
    

    

    # conn = connect_to_mssql()
    # table_name = 'dbktestdev8'
    
    # sanitized_columns = ", ".join([f"[{col}]" for col in df.columns])
    # sanitized_table_name = f"[{table_name}]"
 
        
    # query = f"INSERT INTO {sanitized_table_name} ({sanitized_columns}) VALUES ({','.join(['?'] * len(df.columns))})"
    # try:
    #         with conn.cursor() as cursor:
    #             cursor.executemany(query, df.values.tolist())
    #             conn.commit()
    # except Exception as e:
    #         print(f"Error during database insertion: {e}")  
    # finally:
    #         conn.close()

    
    return redirect('/')
  
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)






























# class devform(FlaskForm):
    
#     dttype = StringField('Type below, No of boxes xhexked upto 10', [ InputRequired(), Regexp(r'^[A-Za-z\s\-\']+$', message="Invalid "),
#         Length(min=1, max=50, message="Invalid ")
#         ])
#     dt1 = DecimalField('1',  [validators.Optional()], [NumberRange(min=-999, max=999, message="Invalid range")])
#     dt2 = DecimalField('2',  [validators.Optional()], [NumberRange(min=-999, max=999, message="Invalid range")])
#     dt3 = DecimalField('3',  [validators.Optional()], [NumberRange(min=-999, max=999, message="Invalid range")])
#     dt4 = DecimalField('4',  [validators.Optional()], [NumberRange(min=-999, max=999, message="Invalid range")])
#     dt5 = DecimalField('5',  [validators.Optional()], [NumberRange(min=-999, max=999, message="Invalid range")])
#     dt6 = DecimalField('6',  [validators.Optional()], [NumberRange(min=-999, max=999, message="Invalid range")])
#     dt7 = DecimalField('7',  [validators.Optional()], [NumberRange(min=-999, max=999, message="Invalid range")])
#     dt8 = DecimalField('8',  [validators.Optional()], [NumberRange(min=-999, max=999, message="Invalid range")])
#     dt9 = DecimalField('9',  [validators.Optional()], [NumberRange(min=-999, max=999, message="Invalid range")])
#     dt10 = DecimalField('10', [validators.Optional()], [NumberRange(min=-999, max=999, message="Invalid range")])

#     updated = HiddenField()
#     submit = SubmitField('Next')
    
# class MasterForm(FlaskForm):
#     row1 = FormField(devform)
#     row2 = FormField(devform)
    
#     submit = SubmitField("Submit")
