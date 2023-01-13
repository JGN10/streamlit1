import sqlite3 as sql
import hashlib


conexion = sql.connect('diabetes.db')
c = conexion.cursor()

def borra_tablas():
    c.execute('DROP TABLE roles')
    c.execute('DROP TABLE usuarios')
    c.execute('DROP TABLE cargas')
    c.execute('DROP TABLE entrenamientos')
    c.execute('DROP TABLE predicciones')
    c.execute('DROP TABLE entrena_modelo')


def crea_tabla_modelos():
    c.execute('CREATE TABLE IF NOT EXISTS entrena_modelo (codigo INTEGER PRIMARY KEY AUTOINCREMENT,\
                modelo TEXT,fichero TEXT, porcentaje float, entrenado integer,\
                FOREIGN KEY (entrenado) REFERENCES entrenamientos(codigo))')


def crea_tablas():
    c.execute('CREATE TABLE IF NOT EXISTS roles (codigo INTEGER PRIMARY KEY AUTOINCREMENT,\
                rol TEXT, observaciones TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS usuarios (codigo INTEGER PRIMARY KEY AUTOINCREMENT,\
                usuario TEXT,password TEXT,role INTEGER, \
                FOREIGN KEY (role) REFERENCES roles(codigo))')
    c.execute('CREATE TABLE IF NOT EXISTS cargas (codigo INTEGER PRIMARY KEY AUTOINCREMENT,\
                usuario INTEGER,fecha TIMESTAMP, FOREIGN KEY (usuario) REFERENCEs usuarios(codigo))')
    c.execute('CREATE TABLE IF NOT EXISTS entrenamientos (codigo INTEGER PRIMARY KEY AUTOINCREMENT,\
                usuario INTEGER,fecha TIMESTAMP, FOREIGN KEY (usuario) REFERENCES usuarios(codigo))')
    c.execute('CREATE TABLE IF NOT EXISTS predicciones (codigo INTEGER PRIMARY KEY AUTOINCREMENT,\
                formato_csv TEXT,embarazos integer, glucosa integer, tension integer, grosor_piel integer,\
                insulina integer, IMC float, DPF float, edad integer, resultado integer, cargado integer,\
                entrenado integer,\
                FOREIGN KEY (cargado) REFERENCES cargas(codigo),\
                FOREIGN KEY (entrenado) REFERENCES entrenamientos(codigo))')

def encripta(texto):
	return hashlib.sha256(str.encode(texto)).hexdigest()

def inserta_usuarios(usuario,password,role):
	c.execute('INSERT INTO usuarios(usuario,password,role) VALUES (?,?,?)',(usuario,encripta(password),role))
	conexion.commit()

def inserta_roles(role):
	c.execute('INSERT INTO roles (rol) VALUES (?)',(role,))
	conexion.commit()




def pruebas():
    c.execute('CREATE TABLE IF NOT EXISTS t1 (codigo INTEGER PRIMARY KEY AUTOINCREMENT, usuario TEXT)')
    cursor = c.execute ('insert into t1 (usuario) values (?) returning codigo', ('usuario1',))

    print(cursor)
   
    #print("valor ", valor[0])
    print("next(cursor)", next(cursor))
    print("cursor.fechall() " , cursor.fetchall())
    cursor = c.execute ('insert into t1 (usuario) values (?) returning codigo', ('usuario1',))
    print(cursor)
   
    #print("valor ", valor[0])
    print("next(cursor)", next(cursor))
    print("cursor.fechall() " , cursor.fetchall())
    cursor = c.execute ('insert into t1 (usuario) values (?) returning codigo', ('usuario1',))
    print(cursor)
   
    #print("valor ", valor[0])
    print("next(cursor)", next(cursor))
    print("cursor.fechall() " , cursor.fetchall())
    cursor = c.execute ('insert into t1 (usuario) values (?) returning codigo, usuario', ('usuario1',))
    print( "fetch.all sin nada " )
    #fila = cursor.fetchall()
    #print(fila[0])
    #
    for row in cursor.fetchall():
        
        for i in range(0,len(row)):
            print("row dentro del dos if ", row[i])
        print("row dentro de un if", row[0])
   
    #print("valor ", valor[0])
    #print("next(cursor)", next(cursor))
    print("cursor.fechall() " , cursor.fetchall())

    cursor = c.execute ('select * from  t1')
    print(cursor)
   
    #print("valor ", valor[0])
    print("next(cursor)", next(cursor))
    print("cursor.fechall() " , cursor.fetchall())

    """
    cur = conn.execute('insert into reg (k) values (?), (?), (?) returning id',
                   ('k1', 'k2', 'k3'))
print(next(cur))  # First result row.

cur = conn.execute('select * from reg')
print(cur.fetchall())
    """

#pruebas()
#borra_tablas()
#crea_tablas()
#inserta_roles("Administración")
#inserta_roles("Consulta")
#inserta_usuarios("Anónimo","0000"," 2")
#inserta_usuarios("Adrián","1111"," 1")
#inserta_usuarios("Jero","2222","1")
#inserta_usuarios("Otro","3333","2")
#crea_tabla_modelos()
#conexion.close()