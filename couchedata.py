# sudo apt-get install python-psycopg2 libpq-dev
# en postgres
# createuser -dl loic
# en loic
# createdb prog
# export DATABASE_URL=postgres://$(whoami)@/prog

from sqlalchemy import create_engine
from sqlalchemy.exc import DBAPIError, ProgrammingError
from sqlalchemy.orm import scoped_session, sessionmaker
import psycopg2
import os
import time

# NSolveODE({I', R', S'}, 0, {I0, R0, S0}, duree)
#engine = create_engine(os.getenv('DATABASE_URL'))
engine = create_engine('postgresql://loic@/prog')

def aff_err_alchemy(e):
    print(str(e.orig)[:-1])
    print(e.orig.pgcode)
    print(type(e))
    print(e.statement)
    print(e.params)
    if e.orig.pgcode == '42P07':
        print('la table existe déjà')

def listdict(r):
    return [i.__dict__ for i in r]
    
def init():
    """
    initialise la base de données
    se lance une fois
    """
    db = scoped_session(sessionmaker(bind=engine))
    try:
        db.execute("create table fiche (id serial primary key, titre varchar, text varchar)")
    except ProgrammingError as e:
        print('prog err')
        aff_err_alchemy(e)
    except DBAPIError as e:
        # voir https://docs.sqlalchemy.org/en/13/core/exceptions.html
        print('alchemy err')
        aff_err_alchemy(e)
    except Exception as e:
        print('exception')
        print(type(e))
    finally:
        db.remove()

def reset_fiche():
    """
    réinitialise les données
    """
    db = scoped_session(sessionmaker(bind=engine))

    try:
        db.execute("drop table fiche")
    except DBAPIError as e:
        print('alchemy err')
        aff_err_alchemy(e)
        db.remove()
        db = scoped_session(sessionmaker(bind=engine))
    
    try:
        db.execute("create table fiche (id serial primary key, titre varchar, text varchar)")
    except DBAPIError as e:
        print('alchemy err')
        aff_err_alchemy(e)
    finally:
        db.commit()
        db.remove()

def test_insert(n = 1):
    """
    cree des données de tests
    """
    db = scoped_session(sessionmaker(bind=engine))
    for _ in range(n):
        db.execute("insert into fiche (titre, text) values (:titre, :text)", {'titre': 'boo', 'text': 'time : '+str(int(time.time()))})
    db.commit()

def aff_liste():
    """
    affichage de degug pour voir le contenu de la table
    """
    db = scoped_session(sessionmaker(bind=engine))
    r= db.execute("select * from fiche").fetchall()
    for i in r:
        print(i.id, i.titre, i.text)

def fiche_liste(id = None):
    """
    retourne les éléments de la table fiche
    """
    db = scoped_session(sessionmaker(bind=engine))
    if id is None:
        r= db.execute("select * from fiche").fetchall()
    else:
        r= db.execute("select * from fiche where id = :id", {'id' : id}).fetchall()
    return (r)

def fiche_insert(titre, text):
    db = scoped_session(sessionmaker(bind=engine))
    db.execute("insert into fiche (titre, text) values (:titre, :text)", {'titre': titre, 'text': text})
    db.commit()

def mesure_session(iterations):
    deb = time.time()
    for _ in range(iterations):
        db = scoped_session(sessionmaker(bind=engine))
    fin = time.time()
    print (f'scoped_session : {iterations} itérations en {str(fin-deb)}s')

def mesure_insert(iterations):
    db = scoped_session(sessionmaker(bind=engine))
    titre = 'AAAAAA'
    texte = 'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
    deb = time.time()
    for _ in range(iterations):
        db.execute("insert into fiche (titre, text) values (:titre, :text)", {'titre': titre, 'text': texte})
    fin = time.time()
    print (f'insert : {iterations} insertions en {str(fin-deb)}s')
    deb = time.time()
    db.commit()
    fin = time.time()
    print (f'commit : apres {iterations} insertion, dure {str(fin-deb)}s')

def test_perf():
    init()
    reset_fiche()
    mesure_insert(1)
    mesure_insert(1000)
    mesure_insert(10000)
    reset_fiche()
    test_insert()
    aff_liste()
    mesure_session(1)
    mesure_session(10)
    mesure_session(100)
    mesure_session(1000)
    mesure_session(10000)
    mesure_session(100000)    

if __name__ == '__main__':
    #init()
    reset_fiche()
    test_insert(10)
    aff_liste()
    print(list(fiche_liste()))
    print(dict(fiche_liste()[0]))
