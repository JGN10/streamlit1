import streamlit as st
import pickle
import pandas as pd
import numpy as np
from sklearn import preprocessing
import connection
#import psycopg2
#import pymongo
import setting
from datetime import datetime
import sqlite3 as sql
import time
import sys
import logging

def main():
        st.warning("Recuerde que esta app es con fines educativos, no es una prueba médica ante cualquier resultado alarmante consulte a su médico")


st.title('')
#st.title("Predicion de la aparicion de diabetes")
st.title("Módulo para la predicción de la Diabetes")
st.write("Debe informar los parametros requeridos para la predicción con sus valores particulares.")
st.write("Una vez introducido sus datos, debe pulsar el botón de Predicción. Se visualizará la predicción.")

def escalar_maxmin(valor,max,min):
        return (valor - min)/(max-min)

def parametros():
        st.sidebar.title("Parámetros requeridos")
        Pregnancies = st.sidebar.slider('Embarazada',int(df_calculos["Pregnancies"]["min"]),
                                        int(df_calculos["Pregnancies"]["max"]), 
                                        int(round(df_calculos["Pregnancies"]["mean"],0)))  

        Glucose = st.sidebar.slider('Glucosa', int(df_calculos["Glucose"]["min"]),
                                    int(df_calculos["Glucose"]["max"]),
                                    int(round(df_calculos["Glucose"]["mean"],0)))

        SkinThickness = st.sidebar.slider('Grosor de la piel', int(df_calculos["SkinThickness"]["min"]), 
                                          int(df_calculos["SkinThickness"]["max"]),
                                          int(round(df_calculos["SkinThickness"]["mean"],0)))

        BMI = st.sidebar.slider('BMI', round(float(df_calculos["BMI"]["min"]),2),
                                round(float(df_calculos["BMI"]["max"]),2), round(float(df_calculos["BMI"]["mean"]),2))

        Age = st.sidebar.slider('Edad', int(df_calculos["Age"]["min"]),
                                int(df_calculos["Age"]["max"]), int(round(df_calculos["Age"]["mean"],0)))

        BloodPressure = st.sidebar.slider('BloodPressure', int(df_calculos["BloodPressure"]["min"]), 
                                          int(df_calculos["BloodPressure"]["max"]),
                                          int(round(df_calculos["BloodPressure"]["mean"],0)))

        Insulin = st.sidebar.slider('Insulin', int(df_calculos["Insulin"]["min"]), 
                                    int(df_calculos["Insulin"]["max"]),
                                    int(round(df_calculos["Insulin"]["mean"],0)))

        DiabetesPedigreeFunction = st.sidebar.slider('DiabetesPedigreeFunction', 
                                                      round(float(df_calculos["DiabetesPedigreeFunction"]["min"]),3),
                                                      round(float(df_calculos["DiabetesPedigreeFunction"]["max"]),3),
                                                     round(float(df_calculos["DiabetesPedigreeFunction"]["mean"]),3))


        data = {'Pregnancies': escalar_maxmin (Pregnancies, 
                                                df_calculos["Pregnancies"]["max"],
                                                df_calculos["Pregnancies"]["min"]),
                'Glucose':escalar_maxmin (Glucose, df_calculos["Glucose"]["max"], df_calculos["Glucose"]["min"]),
                'BloodPressure': escalar_maxmin (BloodPressure, df_calculos["BloodPressure"]["max"],
                                                 df_calculos["BloodPressure"]["min"]),
                'SkinThickness': escalar_maxmin (SkinThickness,
                                                 df_calculos["SkinThickness"]["max"],
                                                 df_calculos["SkinThickness"]["min"]),
                'Insulin': escalar_maxmin (Insulin, df_calculos["Insulin"]["max"], 
                                                 df_calculos["Insulin"]["min"]),
                'BMI': escalar_maxmin (BMI, df_calculos["BMI"]["max"], df_calculos["BMI"]["min"]),
                'DiabetesPedigreeFunction': escalar_maxmin (DiabetesPedigreeFunction,
                                                            df_calculos["DiabetesPedigreeFunction"]["max"],
                                                            df_calculos["DiabetesPedigreeFunction"]["min"]),
                "Age": escalar_maxmin (Age, df_calculos["Age"]["max"], df_calculos["Age"]["min"])
                }
        data1 = {'Embarazos': Pregnancies,
                'Glucosa':Glucose,
                "Presión arterial":BloodPressure,
                'Grosor de la piel':SkinThickness,
                "Insulina":Insulin,
                'BMI':str(BMI),
                "FPD":str(DiabetesPedigreeFunction),
                "Edad":Age
                }
        features1 = pd.DataFrame(data1, index= [0])
        features = pd.DataFrame(data, index= [0])
        return features, features1


df_calculos=pd.read_csv("calculos.csv", index_col= [0])
df, df1= parametros()

st.subheader("Parámetros Proporcionados")
st.dataframe(df1)

def click_csv():
        cadena = str(int(df1.iloc[0]["Embarazos"]))\
                + "," + str(int(df1.iloc[0]["Glucosa"]))\
                + "," + str(int(df1.iloc[0]["Presión arterial"]))\
                + "," + str(int(df1.iloc[0]["Grosor de la piel"]))\
                + "," + str(int(df1.iloc[0]["Insulina"]))\
                + "," + str(df1.iloc[0]["BMI"])\
                + "," + str(df1.iloc[0]["FPD"])\
                + "," + str(int(df1.iloc[0]["Edad"]))\
                + "," + str(st.session_state.prediccion) + "\n"
        with open(st.session_state.nuevo_csv,"a") as file:
                file.write(cadena)
        file.close()
        st.session_state.predicc_guardada = 1

def click_sqlite():
        try:
                if "usuario" in st.session_state:
                        usuario_logeado = st.session_state.usuario
                else:
                        usuario_logeado = 'Anónimo'
                try:
                        conexion = sql.connect(st.session_state.sqlite)
                        c = conexion.cursor()
                except Exception as e:
                        # logging.WARNING("Error conectar base de datos %s" % str(e))
                        print("Error conectar base de datos %s" % str(e))
                try:
                        #c.execute("INSERT INTO cargas (usuario,fecha) VALUES (?,?) RETURNING codigo", (usuario_logeado,datetime.now()))
                        c.execute("INSERT INTO cargas (usuario,fecha) VALUES (?,?)", (usuario_logeado,datetime.now()))
                        cursor_cargas = c.execute('SELECT MAX(codigo) FROM cargas')    
                        for fila in cursor_cargas.fetchall():
                                #c.execute("INSERT INTO cargas (usuario,fecha) VALUES (?,?) RETURNING codigo", (usuario_logeado,datetime.now()))
                                codigo_carga = fila[0]
                except Exception as e:
                #        logging.WARNING("Error insertar base de datos %s" % str(e)) 
                       print("Error insertar base de datos %s" % str(e))
                cadena = str(int(df1.iloc[0]["Embarazos"]))\
                        + "," + str(int(df1.iloc[0]["Glucosa"])) \
                        + "," + str(int(df1.iloc[0]["Presión arterial"]))\
                        + "," + str(int(df1.iloc[0]["Grosor de la piel"]))\
                        + "," + str(int(df1.iloc[0]["Insulina"])) + "," + str(df1.iloc[0]["BMI"])\
                        + "," + str(df1.iloc[0]["FPD"])\
                        + "," + str(int(df1.iloc[0]["Edad"])) + "," + str(int(st.session_state.prediccion)) 
                c.execute("INSERT INTO predicciones (formato_csv,embarazos,glucosa,"\
                                "tension, grosor_piel, insulina, IMC, DPF,edad, resultado ,cargado)"\
                                "VALUES(?, ?, ?, ?,?, ?, ?, ?, ?,?,?);",\
                                (cadena, int(df1.iloc[0]["Embarazos"]),\
                                int(df1.iloc[0]["Glucosa"]),\
                                int(df1.iloc[0]["Presión arterial"]),\
                                int(df1.iloc[0]["Grosor de la piel"]),\
                                int(df1.iloc[0]["Insulina"]),\
                                df1.iloc[0]["BMI"],\
                                df1.iloc[0]["FPD"],\
                                int(df1.iloc[0]["Edad"]),\
                                str(int(st.session_state.prediccion)),\
                                str(int(codigo_carga))))

                #datetime.strptime(parametro.Fecha, '%d-%m-%Y %H:%M:%S')))
                conexion.commit()
                st.session_state.predicc_guardada = 1
                
        except Exception as err:
                print(f"Unexpected {err}, {type(err)}")
                st.session_state.predicc_guardada = 2
                conexion.rollback()
                
        finally:
                c.close()
                conexion.close()

def carga_lista_modelos():
        try:
                conexion = sql.connect('diabetes.db')
                c = conexion.cursor()
                cursor_max_entrenamiento = c.execute('SELECT max(entrenado) FROM entrena_modelo')    
                for row_p in cursor_max_entrenamiento.fetchall():
                    max_entrenamiento = row_p[0]
                cursor_modelos = c.execute('SELECT modelo FROM entrena_modelo where entrenado = ? order by porcentaje desc', (max_entrenamiento,))    
                modelos = []
                for row_p in cursor_modelos.fetchall():
                     modelos.append(row_p[0])
                return modelos
                
        except:
                print("Error inesperado:", sys.exc_info()[0])
        finally:
                conexion.close()


lista_modelo = carga_lista_modelos()
col1, col2,col3 = st.columns(3)
with col1:
        modelo_seleccionado = st.selectbox("Modelo a utilizar",lista_modelo)
        try:
                conexion = sql.connect('diabetes.db')
                c = conexion.cursor()
                cursor_entrena_modelo = c.execute('SELECT porcentaje FROM entrena_modelo where modelo = ? order by codigo desc', (modelo_seleccionado,))    
                for row_p in cursor_entrena_modelo.fetchall():
                        porcentaje= row_p[0]
                        break
                #st.write (f"El porcentaje del modelo seleccionado es: {porcentaje}")
        except Exception as e:
                        # logging.WARNING("Error conectar base de datos %s" % str(e))
                        print("Error conectar base de datos %s" % str(e))
        finally:
                c.close()
                conexion.close()
with col2:
        st.write (f" ")
        st.write (f"El porcentaje del modelo seleccionado es: {porcentaje}")


        
if st.button('Predicción'):
        try: 
                conexion = sql.connect('diabetes.db')
                c = conexion.cursor()
                cursor_fichero = c.execute('SELECT fichero, porcentaje  FROM entrena_modelo where modelo = ? order by codigo desc', (modelo_seleccionado,))    
                for row_p in cursor_fichero.fetchall():
                        fichero_pkl = str(row_p[0])
                        porcentaje = row_p[1]
                        break
                with open(fichero_pkl, "rb") as li:
                        guarda_modelo = pickle.load(li)
                prediccion = guarda_modelo.predict(df)
                st.session_state.prediccion= int(prediccion)
                if prediccion == 0:
                        st.success(f"El modelo {modelo_seleccionado} con una exactitud de {porcentaje} indica que NO padecerá diabetes")
                else:
                        st.error(f"El modelo {modelo_seleccionado} con una exactitud de {porcentaje} indica que SI padecerá diabetes") 
                st.write("Puede guardar esta predicción para ayudarnos a mejorar el modelo utilizado y obtener mejores resultados")
                st.write("Se disponen de varias tecnologias para almacenar su predicción. Pulse el botón que más le interese")
                col1, col2 = st.columns(2)
                with col1:
                        st.subheader("Fichero CSV")
                        st.write("Para guardar su predicción en un fichero plano, pulse el botón Fichero CSV")
                        st.button("Fichero CSV", on_click=click_csv)

                with col2:
                        st.subheader("Base de datos")
                        st.write("Para guardar su predicción en una base de datos SQLite, pulse el botón Base SQLite")
                        st.button("Base SQLite", on_click=click_sqlite)
                
        except:
                print("Error inesperado:", sys.exc_info()[0])
        finally:
                conexion.close()

if "predicc_guardada" in st.session_state:
        if st.session_state.predicc_guardada == 1:
                st.success("Predicción guardada correctamente")
                st.session_state.predicc_guardada = 0
        elif st.session_state.predicc_guardada == 2:
                st.error("Predicción NO guardada")
                st.session_state.predicc_guardada = 0
        else:
                pass
else:
        pass


if __name__ == '__main__':
    main() 

