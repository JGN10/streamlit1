import sqlite3 as sql
import hashlib
import streamlit as st
import sys
import os
import entrena
import time


conexion = sql.connect('diabetes.db')
c = conexion.cursor()

def encripta(texto):
	return hashlib.sha256(str.encode(texto)).hexdigest()

def valida_encriptado(texto,texto_encriptado):
	if encripta(texto) == texto_encriptado:
		return texto_encriptado
	return False


def selecciona_usuario(usuario,password):
    try:
        c.execute('SELECT a.codigo, r.codigo, r.rol FROM usuarios as a join roles as r on a.role = r.codigo WHERE a.usuario =? AND a.password = ?',(usuario,password))
        for fila in c.fetchall():
            return fila[0],fila[1], fila[2]
        return False, False, False
    except:
        print("Error inesperado:", sys.exc_info()[0])
        return False, False, False
    finally:
        conexion.close()

    
def borra_todos_registros():
    c.execute('DELETE FROM usuarios')
    conexion.commit()



def csv_click():
    codigo_entrenamiento = entrena.entrena_csv(st.session_state.usuario, st.session_state.nuevo_csv)
    porcentaje, modelo,fichero = entrena.entrena_modelo(codigo_entrenamiento)
    st.session_state.porcentaje = porcentaje
    st.session_state.modelo = modelo
    st.session_state.fichero = fichero
    cadena = "Se han procesado correctamente los" \
            + " registros y se ha entrenado de nuevo el modelo"
    st.success(cadena)
    cadena = f"El modelo con mayor porcentaje de acierto ha sido {st.session_state.modelo}."\
            + f" con un porcentaje de {st.session_state.porcentaje}"
    st.success(cadena)

def sqlite_click():
    codigo_entrenamiento = entrena.entrena_sqlite(st.session_state.usuario)
    porcentaje, modelo,fichero = entrena.entrena_modelo(codigo_entrenamiento)
    st.session_state.porcentaje = porcentaje
    st.session_state.modelo = modelo
    st.session_state.fichero = fichero
    cadena = "Se han procesado correctamente los" \
            + " registros y se ha entrenado de nuevo el modelo"
    st.success(cadena)
    cadena = f"El modelo con mayor porcentaje de acierto ha sido {st.session_state.modelo}."\
            + f" con un porcentaje de {st.session_state.porcentaje}"
    st.success(cadena)

def ventana_administracion():
    if "usuario" in st.session_state:
        if st.session_state.codigo_rol == 1:
            cadena = "Ventana de mantenimiento. Usuario: " + st.session_state.usuario 
            st.title(cadena )
            st.subheader("Pulse el botón de los registros que quiera añadir al estudio del modelo")
            col1, col2 = st.columns(2)
            with col1: 
                st.subheader("Mantenimiento fichero")
                if st.session_state.nuevo_csv != "":
                    registros_csv = 0
                    try:
                        with open(st.session_state.nuevo_csv, 'r') as f1:
                            for linea in f1:
                                registros_csv += 1
                    except FileNotFoundError as e:
                        print(f"{e}")
                    if registros_csv > 0:
                        cadena = "El número de registros a tratar a través del fichero CSV es : " + str(registros_csv)
                        st.write(cadena)
                        st.button("Entrenar CSV", on_click=csv_click)
                    
                    else:
                        cadena = "No existen registros pendientes de tratar a través del fichero CSV "
                        st.write(cadena)
            with col2:
                st.subheader("Mantenimiento SQLite")
                if st.session_state.sqlite != "":        
                    try:
                        numero_registros_sqlite = 0
                        conexion = sql.connect('diabetes.db')
                        c = conexion.cursor()
                        cursor_predicciones = c.execute('SELECT count(*) FROM predicciones WHERE entrenado is null')    
                        for row in cursor_predicciones.fetchall():
                            numero_registros_sqlite = row[0]
                        if numero_registros_sqlite > 0:
                            cadena = "El número de registros a tratar a través de SQLite es : " + str(numero_registros_sqlite)
                            st.write(cadena)
                            st.button("Entrenar SQLite",on_click=sqlite_click)
                            
                        else:
                            cadena = "No existen registros pendientes de tratar a través de SQLite "
                            st.write(cadena)
                    except:
                        print("Error inesperado:", sys.exc_info()[0])
                    finally:
                        conexion.close()
                #if st.session_state.postgredb != "":        
                #             if st.session_state.mongodb != "":        
        else:
            cadena = "Ventana de administración. Usuario: " + st.session_state.usuario 
            st.title(cadena )
            st.subheader("No tiene permiso para realizar tareas de administración.")


def introduce_usuario():
    login_usuario = st.sidebar.text_input('Nombre de usuario')
    password_usuario = st.sidebar.text_input('Password de usuario',type='password')
    password_encriptado = encripta(password_usuario)
    st.session_state.login_usuario = login_usuario
    st.session_state.password_encriptado = password_encriptado
    if st.sidebar.button("login"):
        datos,codigo_rol, rol = selecciona_usuario(st.session_state.login_usuario,st.session_state.password_encriptado)
        if datos:
            st.session_state.usuario = st.session_state.login_usuario
            st.session_state.codigo_usuario = datos
            st.session_state.rol_usuario = rol
            st.session_state.codigo_rol = codigo_rol
            st.sidebar.subheader(f"Usuario: {st.session_state.usuario}") 
            st.sidebar.button("cambio usuario",on_click=click_cambio_usuario)   
            ventana_administracion()
            #login()
        else:
            print("en el else de datos ")
            st.sidebar.warning("Usuario o password incorrecto")
            st.title("Para acceder a esta ventana debe identificarse con usuario y password")
    else:
        st.title("Para acceder a esta ventana debe identificarse con usuario y password")

def click_cambio_usuario():
    del st.session_state.usuario
    del st.session_state.login_usuario
    del st.session_state.password_encriptado
    del st.session_state.codigo_usuario
    del st.session_state.rol_usuario
    del st.session_state.codigo_rol

def login():
    if ("usuario" not in st.session_state): # and ("usuario_validado" not in st.session_state): 
        introduce_usuario()
        
    else:
        st.sidebar.subheader(f"Usuario: {st.session_state.usuario}") 
        st.sidebar.button("cambio usuario",on_click=click_cambio_usuario)
        ventana_administracion()   


if __name__ == '__main__':
    login()
