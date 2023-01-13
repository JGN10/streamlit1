import streamlit as st
import pickle
import pandas as pd
import numpy as np
from sklearn import preprocessing
import connection
import psycopg2
import pymongo
import setting
from datetime import datetime
import sqlite3 as sql
import time
import sys

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
                'SkinThickness': escalar_maxmin (SkinThickness,
                                                 df_calculos["SkinThickness"]["max"],
                                                 df_calculos["SkinThickness"]["min"]),
                'BMI': escalar_maxmin (BMI, df_calculos["BMI"]["max"], df_calculos["BMI"]["min"]),
                "Age": escalar_maxmin (Age, df_calculos["Age"]["max"], df_calculos["Age"]["min"]),
                'BloodPressure': escalar_maxmin (BloodPressure, df_calculos["BloodPressure"]["max"],
                                                 df_calculos["BloodPressure"]["min"]),
                'Insulin': escalar_maxmin (Insulin, df_calculos["Insulin"]["max"], 
                                                 df_calculos["Insulin"]["min"]),
                'DiabetesPedigreeFunction': escalar_maxmin (DiabetesPedigreeFunction,
                                                            df_calculos["DiabetesPedigreeFunction"]["max"],
                                                            df_calculos["DiabetesPedigreeFunction"]["min"])
                }
        #print(BMI)
        data1 = {'Embarazos': Pregnancies,
                'Glucosa':Glucose,
                "Presión arterial":BloodPressure,
                'Grosor de la piel':SkinThickness,
                "Insulina":Insulin,
                'BMI':str(BMI),
                "FPD":str(DiabetesPedigreeFunction),
                "Edad":Age
                }
        #print(data1)
        #Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,DiabetesPedigreeFunction,Age,Outcome
        #print('embarazos ' , data1['Embarazos'])        
        features1 = pd.DataFrame(data1, index= [0])
        features = pd.DataFrame(data, index= [0])
        return features, features1


df_calculos=pd.read_csv("calculos.csv", index_col= [0])
df, df1= parametros()
print(df1)
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

                
                #+ "," + str(round(df1.iloc[0]["BMI"],1))\
                #+ "," + str(round(df1.iloc[0]["Función de pedigrí de diabetes"],3))\

def click_sqlite():
        try:
                if "usuario" in st.session_state:
                        usuario_logeado = st.session_state.usuario
                else:
                        usuario_logeado = 'Anónimo'
                print("en el click sqlite")
                conexion = sql.connect(st.session_state.sqlite)
                c = conexion.cursor()
                c.execute("insert into cargas (usuario,fecha) values (?,?) returning codigo", (usuario_logeado,datetime.now()))
                for fila in c.fetchall():
                        codigo_carga = fila[0]
                cadena = str(int(df1.iloc[0]["Embarazos"]))\
                        + "," + str(int(df1.iloc[0]["Glucosa"])) \
                        + "," + str(int(df1.iloc[0]["Presión arterial"]))\
                        + "," + str(int(df1.iloc[0]["Grosor de la piel"]))\
                        + "," + str(int(df1.iloc[0]["Insulina"])) + "," + str(df1.iloc[0]["BMI"])\
                        + "," + str(df1.iloc[0]["FPD"])\
                        + "," + str(int(df1.iloc[0]["Edad"])) + "," + str(int(st.session_state.prediccion)) 
                print("en el insert valor de cadena", cadena)
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
                
        except psycopg2.Error as e:
                print("Error insertar registros: %s" % str(e))
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
        modelo_seleccionado = st.selectbox("modelo",lista_modelo)
        print('fuera de la funcion ', modelo_seleccionado)

if st.button('Predicción'):
        try: 
                conexion = sql.connect('diabetes.db')
                c = conexion.cursor()
                print('modelo seleccionado ', modelo_seleccionado)
                cursor_fichero = c.execute('SELECT fichero, porcentaje  FROM entrena_modelo where modelo = ? order by codigo desc', (modelo_seleccionado,))    
                for row_p in cursor_fichero.fetchall():
                        print(row_p[0])
                        print(row_p)
                        fichero_pkl = str(row_p[0])
                        print('después de row_p')
                        porcentaje = row_p[1]
                        print('después de row_p porcentaje')
                        break
                with open(fichero_pkl, "rb") as li:
                        guarda_modelo = pickle.load(li)
                prediccion = guarda_modelo.predict(df)
                st.session_state.prediccion= int(prediccion)
                if prediccion == 0:
                        #st.success(f"El modelo {st.session_state.modelo} indica que NO padecerá diabetes")
                        st.success(f"El modelo {modelo_seleccionado} con una exactitud de {porcentaje} indica que NO padecerá diabetes")
                else:
                        st.error(f"El modelo {modelo_seleccionado} con una exactitud de {porcentaje} indica que SI padecerá diabetes") 
                st.write("Puede guardar esta predicción para ayudarnos a mejorar el modelo utilizado y obtener mejores resultados")
                st.write("Se disponen de varias tecnologias para almacenar su predicción. Pulse el botón que más le interese")
                #if st.session_state.nuevo_csv != "":
                #        st.write("Para guardar su predicción en un fichero plano, pulse el botón Fichero")
                #        st.button("Fichero", on_click=click_csv)
                #if st.session_state.sqlite != "":        
                #        st.write("Para guardar su predicción en una base de datos SQLite, pulse el botón Base SQLite")
                #        st.button("Base SQLite", on_click=click_sqlite)         
                col1, col2 = st.columns(2)
                with col1:
                        st.subheader("Fichero CSV")
                        st.write("Para guardar su predicción en un fichero plano, pulse el botón Fichero CSV")
                        st.button("Fichero CSV", on_click=click_csv)

                with col2:
                        st.subheader("Base de datos")
                        st.write("Para guardar su predicción en una base de datos SQLite, pulse el botón Base SQLite")
                        st.button("Base SQLite", on_click=click_sqlite)
                
                #if st.session_state.mongodb != "":
                #        st.write("Moooongo")
        except:
                print("Error inesperado:", sys.exc_info()[0])
        finally:
                conexion.close()

if st.session_state.predicc_guardada == 1:
        st.success("Predicción guardada correctamente")
        st.session_state.predicc_guardada = 0
elif st.session_state.predicc_guardada == 2:
        st.error("Predicción NO guardada")
        st.session_state.predicc_guardada = 0


if __name__ == '__main__':
    main() 


