from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from flask_mysqldb import MySQL
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_session import Session
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)

#DB Configuration

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/amicaldopj'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'amicaldopj'
app.config['MYSQL_HOST'] = 'localhost'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecret'
app.config['TEMPLATES_AUTO_RELOAD'] = True


db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
mysql = MySQL(app)


# MySQL Database und Tables

ass = db.Table('ass',
               db.Column('d_id', db.Integer, db.ForeignKey('domain.id')),
               db.Column('t_id', db.Integer, db.ForeignKey('tag.id'))
               )


class Domain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    tags = db.relationship('Tag', secondary=ass, backref=db.backref('Domain', lazy='dynamic'))


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)

    def __repr__(self):
        return '<Tag %s>' % self.name


class AddInfo(FlaskForm):
    domain = StringField('', render_kw={"placeholder": "Domain"}, validators=[DataRequired()])
    tag = StringField('', render_kw={"class": "results", "type": "text", "data-role": "tagsinput"})


# Routes

@app.route('/')
def init():
    from app import db
    db.create_all()
    return 'Schreib mal /admin du Esel'


@app.route('/show', methods=['GET'])
def show_data():
    domains = Domain.query.all()
    tags = db.session.query(Domain, Tag).outerjoin(Tag, Domain.id == Tag.id).all() # Probably a Join query but I'm not sure ? And look index.html
    return render_template('index.html', Mydomains=domains, Mytags=tags)


@app.route('/show/<ids>', methods=['GET'])
def show_einzeln(ids):
    domains = Domain.query.filter_by(id=ids)
    ids = ids
    return render_template('one.html', ids=ids, domains=domains, title='Einzeln Domain')


@app.route('/anlegen', methods=['GET', 'POST'])
def add_domtag():
    form = AddInfo()
    if request.method == 'POST':
        req = request.form
        Domain = req['domain']
        Tag = req['tag']
        cur = mysql.connection.cursor()

        cur.execute('INSERT INTO Domain(name) VALUES (%s)', [Domain])
        for i in Tag.split(','):
            cur.executemany('INSERT INTO Tag(name) VALUES (%s)', (i,))


        Domain.tags.append(Tag) # Error | Here I should insert/update the association table "ass"
        db.session.commit()
        mysql.connection.commit()
        cur.close()
        return ('Succes')
    else:
        return render_template('formular.html', form=form, title='Add Data')


if __name__ == "__main__":
    app.run(debug=True)

'''
@app.route('/admin/add')

def add_users():

    from app import Tag, Domain
    db.create_all()

    d1 = Domain(id="1", name="Kev")
    t1 = Tag(t_id="1", name="Benz")
    d1.tags.append(t1)
    db.session.add([d1])
    db.session.commit()


'''
