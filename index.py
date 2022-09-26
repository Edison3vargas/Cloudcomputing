from email.policy import default
from unicodedata import name
from flask import Flask, render_template,flash,redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
#Add database
app.config['SQLALCHEMY_DATABASE_URI']='mysql://admin:edison_123@database-ioteca.cpcwu7ahmch0.us-east-1.rds.amazonaws.com/bd_examen'
app.config['SQLALCHEMY_TRACK_MODEFICATIONS']=False
#Secret key
app.config['SECRET_KEY']='My secret is not secret'
#Initialezate the database
db=SQLAlchemy(app)

# ---------- Creando tablas en la base de datos bd_examen
#Create model ESCUELA
class Escuela(db.Model):
    __tablename__='escuela'

    codigo=db.Column(db.Integer, primary_key=True)
    duracion=db.Column(db.Integer, nullable=False)
    nombre=db.Column(db.String(120), nullable=False)
    create_date=db.Column(db.DateTime, default=datetime.utcnow)

    escuela = db.relationship('Estudiante', backref='escuela', lazy=True)


#Create model ESTUDIANTE
class Estudiante(db.Model):
    __tablename__='estudiante'

    dni=db.Column(db.String(8), primary_key=True)
    nombres=db.Column(db.String(120), nullable=False)
    apellidos=db.Column(db.String(200), nullable=False)
    FeNacimiento=db.Column(db.String(200), nullable=False)
    sexo=db.Column(db.String(10), nullable=False)    
    create_date=db.Column(db.DateTime, default=datetime.utcnow)

    cod_escuela=db.Column(db.Integer, db.ForeignKey('escuela.codigo'))

    matricula = db.relationship('Matricula', backref='estudiante', lazy=True)


#Create model CURSO
class Curso(db.Model):
    __tablename__='curso'

    codigo=db.Column(db.Integer, primary_key=True)
    creditos=db.Column(db.Integer, nullable=False)
    nombre=db.Column(db.String(120), nullable=False)
    create_date=db.Column(db.DateTime, default=datetime.utcnow)

    curso = db.relationship('Matricula', backref='curso', lazy=True)


#Create model MATRICULA
class Matricula(db.Model):
    __tablename__='matricula'

    id=db.Column(db.Integer, primary_key=True)
    create_date=db.Column(db.DateTime, default=datetime.utcnow)
    cod_curso=db.Column(db.Integer, db.ForeignKey('curso.codigo'))
    dni=db.Column(db.String(8), db.ForeignKey('estudiante.dni'))   
    

with app.app_context():
    db.create_all()
    
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++   
# -------------- Creando CLASES

#Create form class escuela
class EscuelaForm(FlaskForm):
    name=StringField("Nombre de la carrera", validators=[DataRequired()])
    duracion=StringField("Duracion de la carrera(Semestres)", validators=[DataRequired()])
    submit=SubmitField('Submit')

#Create form class curso
class CursoForm(FlaskForm):
    name=StringField("Nombre del curso", validators=[DataRequired()])
    creditos=StringField("Cantidad de creditoss", validators=[DataRequired()])
    submit=SubmitField('Submit')
    
#Create form class estudiante
class EstudianteForm(FlaskForm):
    dni=StringField("DNI", validators=[DataRequired()])
    nombres=StringField("Nombres", validators=[DataRequired()])
    apellidos=StringField("Apellidos", validators=[DataRequired()])
    FeNacimiento=StringField("Fecha de nacimiento", validators=[DataRequired()])
    sexo=StringField("Sexo", validators=[DataRequired()])
    cod_escuela=StringField("Codigo de EAP", validators=[DataRequired()])
    submit=SubmitField('Submit')
    
#Create form class MATRICULA
class MatriculaForm(FlaskForm):
    dni=StringField("DNI de estudiante", validators=[DataRequired()])
    cod_curso=StringField("Curso", validators=[DataRequired()])
    submit=SubmitField('Submit')   
    
###### +++++++++ AXTUALIZAR Y ELMINAR DATOS +++++++++++ ################

@app.route('/')
def index():
    firts_name='Sistema De Matriculas'
    stuff='This is bold text'
    flash("Wellcome To Our Website")
    return render_template("index.html",firts_name=firts_name, stuff=stuff)

# --------------- ESCUELA ------------
# ----------> Add Escuela
@app.route('/escuela/add',methods=['GET','POST'])
def add_escuela():
    nombre=None
    form=EscuelaForm()
    #validate form
    if form.validate_on_submit():
        escuela=Escuela(nombre=form.name.data, duracion=form.duracion.data)
        db.session.add(escuela)
        db.session.commit()
        nombre=form.name.data
        form.name.data=''
        form.duracion.data=''
        flash("Registro AGREGADO correctamente")
    our_users=Escuela.query.order_by(Escuela.create_date)
    return render_template('add_escuela.html',
    form=form,
    nombre=nombre,
    our_users=our_users
    )

#Delete Escuela
@app.route('/escuela/delete/<codigo>')
def delete_escuela(codigo):  
    escuela=Escuela.query.get(codigo)
    db.session.delete(escuela)
    db.session.commit()
    flash("Registro ELIMINADO correctamente")

    return redirect('/escuela/add')

#Upadate Escuela
@app.route('/escuela/update/<codigo>',methods=['GET','POST'])
def update_escuela(codigo):
    escuela=Escuela.query.get(codigo)
    form=EscuelaForm()
    if form.validate_on_submit():
        escuela.nombre=form.name.data
        escuela.duracion=form.duracion.data

        db.session.commit()

    name=form.name.data
    form.name.data=''
    form.duracion.data=''
    flash("Datos ACTUALIZADOS correctamente")
    our_users=Escuela.query.order_by(Escuela.create_date)

    return render_template('update_escuela.html',escuela=escuela,form=form,name=name,our_users=our_users)

# ----------------------------------------------------------------------------------------------------------
# ---------------- CURSO ------------
#------------> Curso

# Add curso
@app.route('/curso/add',methods=['GET','POST'])
def add_curso():
    nombre=None
    form=CursoForm()
    #validate form
    if form.validate_on_submit():
        curso=Curso(nombre=form.name.data, creditos=form.creditos.data)
        db.session.add(curso)
        db.session.commit()
        nombre=form.name.data
        form.name.data=''
        form.creditos.data=''
        flash("Registro AGREGADO correctamente")
    our_users=Curso.query.order_by(Curso.create_date)
    return render_template('add_curso.html',
    form=form,
    nombre=nombre,
    our_users=our_users
    )

#Delete Curso
@app.route('/curso/delete/<codigo>')
def delete_curso(codigo):  
    curso=Curso.query.get(codigo)
    db.session.delete(curso)
    db.session.commit()
    flash("Registro ELIMINADO correctamente")

    return redirect('/curso/add')

#Upadate Curso
@app.route('/curso/update/<codigo>',methods=['GET','POST'])
def update_curso(codigo):
    curso=Curso.query.get(codigo)
    form=CursoForm()
    if form.validate_on_submit():
        curso.nombre=form.name.data
        curso.creditos=form.creditos.data

        db.session.commit()

    name=form.name.data
    form.name.data=''
    form.creditos.data=''
    flash("Datos ACTUALIZADOS correctamente")
    our_users=Curso.query.order_by(Curso.create_date)

    return render_template('update_curso.html',curso=curso,form=form,name=name,our_users=our_users)

# ----------------------------------------------------------------------------------------------------
# ---------------- ESTUDIANTE -------------------
# ------------> Add Estudiante
@app.route('/estudiante/add',methods=['GET','POST'])
def add_estudiante():
    nombres=None
    form=EstudianteForm()
    
    #validate form
    if form.validate_on_submit():
        estudiante=Estudiante(dni=form.dni.data, nombres=form.nombres.data, 
                             apellidos=form.apellidos.data,
                             FeNacimiento=form.FeNacimiento.data,
                             sexo=form.sexo.data,
                             cod_escuela=form.cod_escuela.data,)
        db.session.add(estudiante)
        db.session.commit()
        form.dni.data=''
        nombres=form.nombres.data
        form.apellidos.data=''
        form.FeNacimiento.data=''
        form.sexo.data=''
        form.cod_escuela.data=''
        flash("Registro AGREGADO correctamente")
    our_users=Estudiante.query.order_by(Estudiante.create_date)
    escuela=Estudiante.query.order_by(Estudiante.create_date)
    return render_template('add_estudiante.html',
    form=form,
    nombres=nombres,
    our_users=our_users,
    escuela=escuela
    )

#Delete Estudiante
@app.route('/estudiante/delete/<dni>')
def delete_estudiante(dni):  
    estudiante=Estudiante.query.get(dni)
    db.session.delete(estudiante)
    db.session.commit()

    return redirect('/estudiante/add')

#Upadate Estudiante
@app.route('/estudiante/update/<dni>',methods=['GET','POST'])
def update_estudiante(dni):
    estudiante=Estudiante.query.get(dni)
    form=EstudianteForm()
    if form.validate_on_submit(): 
        estudiante.dni=form.dni.data,
        estudiante.nombres=form.nombres.data,
        estudiante.apellidos=form.apellidos.data,
        estudiante.FeNacimiento=form.FeNacimiento.data, 
        estudiante.sexo=form.sexo.data,         
        estudiante.cod_escuela=form.cod_escuela.data

        db.session.commit()

    nombres=form.nombres.data
    form.nombres.data=''
    form.apellidos.data=''
    form.FeNacimiento.data=''
    form.sexo.data=''
    form.cod_escuela.data=''
    flash("Registro MODIFICADO correctamente")
    our_users=Estudiante.query.order_by(Estudiante.create_date)
    escuelas=Escuela.query.order_by(Escuela.create_date)
    return render_template('update_estudiante.html',
    form=form,
    nombres=nombres,
    escuelas=escuelas,
    our_users=our_users,
    estudiante=estudiante    
    )
# --------------------------------------------------------------------------------------------------

# --------------- Matricula---------------
# --------------> Add Matricula
@app.route('/matricula/add',methods=['GET','POST'])
def add_matricula():
    nombre=None
    form=MatriculaForm()
    #validate form
    if form.validate_on_submit():
        matricula=Matricula(
            dni=form.dni.data,
            cod_curso=form.cod_curso.data)

        db.session.add(matricula)
        db.session.commit()
    
    form.dni.data=''
    form.cod_curso.data=''
    flash("Registro AGREGADO correctamente")
    our_users=Matricula.query.order_by(Matricula.create_date)
    cursos=Curso.query.order_by(Curso.create_date)
    return render_template('add_matricula.html',
    form=form,
    cursos=cursos,
    our_users=our_users
    )

#Delete Estudiante
@app.route('/matricula/delete/<id>')
def delete_matricula(id):  
    matricula=Matricula.query.get(id)
    db.session.delete(matricula)
    db.session.commit()
    flash("Registro ELIMINADO correctamente")

    return redirect('/matricula/add')

#Upadate Matricula
@app.route('/matricula/update/<id>',methods=['GET','POST'])
def update_matricula(id):
    matricula=Matricula.query.get(id)
    form=MatriculaForm()
    if form.validate_on_submit(): 
        matricula.dni=form.dni.data,
        matricula.cod_curso=form.cod_curso.data

        db.session.commit()

    nombre=Estudiante.query.get(matricula.dni)
    dni=form.dni.data
    form.dni.data=''
    form.cod_curso.data=''
    flash("Registro AGREGADO correctamente")
    our_users=Matricula.query.order_by(Matricula.create_date)
    cursos=Curso.query.order_by(Curso.create_date)
    return render_template('update_matricula.html',
    form=form,
    cursos=cursos,
    matricula=matricula,
    nombre=nombre,
    dni=dni,
    our_users=our_users   
    )

if __name__=='__main__':
    app.run(debug=True,port=5000,host="0.0.0.0")