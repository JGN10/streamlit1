import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import os
import shutil
import sqlite3 as sql
from datetime import date
from datetime import datetime

from sklearn.preprocessing import QuantileTransformer
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.preprocessing import MinMaxScaler
import pickle


from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
#from sklearn.ensemble import GradientBoostingRegressor
from sklearn import metrics




def entrena_sqlite(usuario):
    #abro cursor con los registros sin entrenar
    try:
        conexion = sql.connect('diabetes.db')
        c = conexion.cursor()
        nombre_actual = "diabetes.csv"
        with open(nombre_actual, 'r') as f1:
            for linea in f1:
                pass
            ultima_linea = linea
            final_linea = ultima_linea.find("\n")
        

        
        cursor_entrenamiento = c.execute ('insert into entrenamientos (usuario,fecha) values (?,?) returning codigo', (usuario,datetime.now()))
        for row in cursor_entrenamiento.fetchall():
            codigo_entrenamiento = row[0]
            print('el codigo de entrenamiento ', codigo_entrenamiento)
            with open(nombre_actual, 'a') as f:
                if final_linea == -1:
                    f.write("\n")
                cursor_predicciones = c.execute('SELECT a.codigo, a.formato_csv FROM predicciones as a WHERE a.entrenado is null')    
                print("antes del cursor de predicciones ")
                for row_p in cursor_predicciones.fetchall():
                    print("dentro del cursor de predicciones ")
                    codigo_prediccion = row_p[0]
                    formato_csv = row_p[1]
                    print("el codigo de prediccion ", codigo_prediccion)
                    print("el valor de formato_csv ", formato_csv)
                    c.execute('update predicciones set entrenado = ? where codigo = ?', (codigo_entrenamiento,codigo_prediccion))
                    f.write(formato_csv + "\n")
        conexion.commit()
        return (codigo_entrenamiento)
    except:
        print("en el error de entrena sqlite usuario")
        print("Error inesperado:", sys.exc_info()[0])
        conexion.rollback()
        return 0
        
    finally:
        conexion.close()
    



def entrena_csv(usuario, nuevo_csv):
    try:
        conexion = sql.connect('diabetes.db')
        c = conexion.cursor()
        usuario_logeado = usuario
        #Fecha actual
        fecha_actual = datetime.now()
        nombre_fichero_usuario = nuevo_csv + "_" + format(fecha_actual.year)\
                                    + format(fecha_actual.month) + format(fecha_actual.day)\
                                    + format(fecha_actual.hour) + format(fecha_actual.minute)\
                                    + format(fecha_actual.second) + usuario_logeado
        os.rename(nuevo_csv , nombre_fichero_usuario)
        nombre_actual = "diabetes.csv"
        nombre_nuevo = nombre_actual + "_" + format(fecha_actual.year) + format(fecha_actual.month)\
                        + format(fecha_actual.day) + format(fecha_actual.hour) + format(fecha_actual.minute)\
                        + format(fecha_actual.second)    
        shutil.copy(nombre_actual, nombre_nuevo)

        with open(nombre_actual, 'r') as f1:
            for linea in f1:
                pass
            ultima_linea = linea
            final_linea = ultima_linea.find("\n")
            

        with open(nombre_fichero_usuario) as archivo:
            with open(nombre_actual, 'a') as f:
                if final_linea == -1:
                    f.write("\n")
                for linea in archivo:
                    f.write(linea)

        cursor_entrenamiento = c.execute ('insert into entrenamientos (usuario,fecha) values (?,?) returning codigo', (usuario,datetime.now()))
        for row in cursor_entrenamiento.fetchall():
            codigo_entrenamiento = row[0]
        conexion.commit()
        return (codigo_entrenamiento)
    except:
        print("en el error de entrena csv usuario")
        print("Error inesperado:", sys.exc_info()[0])
        conexion.rollback()
        return 0
        
    finally:
        conexion.close()


def entrena_modelo(entrenamiento):
    df=pd.read_csv("diabetes.csv")

    df['Glucose']=df['Glucose'].replace(0,None)#normal distribution
    df['BloodPressure']=df['BloodPressure'].replace(0,None)#normal distribution
    df['SkinThickness']=df['SkinThickness'].replace(0,None)#skewed distribution
    df['Insulin']=df['Insulin'].replace(0,None)#skewed distribution
    df['BMI']=df['BMI'].replace(0,None)#skewed distribution

    Media_glucosa = df['Glucose'].mean()
    df["Glucose"].fillna(df['Glucose'].mean(), inplace = True)
    
    media_blood = df['BloodPressure'].mean()
    df['BloodPressure'].fillna(df['BloodPressure'].mean(), inplace = True)

    media_skin = df['SkinThickness'].median()
    df['SkinThickness'].fillna(df['SkinThickness'].median(), inplace = True)

    media_insulina =df['Insulin'].median()
    df['Insulin'].fillna(df['Insulin'].median(), inplace = True)

    media_bmi = df['BMI'].median()
    df['BMI'].fillna(df['BMI'].median(), inplace = True)


    df_selected=df
    df_describe = df_selected.describe()
    df_describe['SkinThickness']['mean'] = media_skin
    df_describe['BMI']['mean'] = media_bmi
    df_describe['Insulin']['mean'] = media_insulina
    df_describe.to_csv('calculos.csv')  


    minmax = MinMaxScaler()

    df_selected['Pregnancies'] = minmax.fit_transform(df_selected[['Pregnancies']])
    df_selected['Glucose'] = minmax.fit_transform(df[['Glucose']])
    df_selected['SkinThickness'] = minmax.fit_transform(df[['SkinThickness']])
    df_selected['BMI'] = minmax.fit_transform(df[['BMI']])
    df_selected['Age'] = minmax.fit_transform(df[['Age']])
    df_selected['BloodPressure'] = minmax.fit_transform(df[['BloodPressure']])
    df_selected['Insulin'] = minmax.fit_transform(df[['Insulin']])
    df_selected['DiabetesPedigreeFunction'] = minmax.fit_transform(df[['DiabetesPedigreeFunction']])

    target_name='Outcome'
    y= df_selected[target_name]#given predictions - training data 
    X=df_selected.drop(target_name,axis=1)#dropping the Outcome column and keeping all other columns as X
    X_train, X_test, y_train, y_test= train_test_split(X,y,test_size=0.2,random_state=0)#splitting data in 80% train, 20%test

    try:
        conexion = sql.connect('diabetes.db')
        c = conexion.cursor()

        #Logistic Regression
        lr = LogisticRegression(random_state = 0)
        lr.fit(X_train, y_train) 
        y_pred = lr.predict(X_test)
        with open('modelo_LR.pkl', 'wb') as mod:
            pickle.dump(lr,mod)
        # calculo para la exactitud del modelo
        exactitud_lr = metrics.accuracy_score(y_test, y_pred)
        porcentaje = exactitud_lr
        modelo = "LogisticRegression"
        fichero = "modelo_LR.pkl"
        c.execute ('insert into entrena_modelo (modelo,fichero,porcentaje,entrenado) values (?,?,?,?)', (modelo,fichero,round((porcentaje*100)),entrenamiento))

        #Vecinos
        kne = KNeighborsClassifier(n_neighbors = 5, metric = 'minkowski', p=2) 
        kne.fit(X_train, y_train) 
        y_pred = kne.predict(X_test)
        with open('modelo_KNE.pkl', 'wb') as mod:
            pickle.dump(kne,mod)
        exactitud_kne = metrics.accuracy_score(y_test, y_pred)
        if porcentaje < exactitud_kne:
            porcentaje = exactitud_kne
            modelo = "KNeighborsClassifier"
            fichero = "modelo_KNE.pkl"
        c.execute ('insert into entrena_modelo (modelo,fichero,porcentaje,entrenado) values (?,?,?,?)', ("KNeighborsClassifier","modelo_KNE.pkl",round((exactitud_kne*100)),entrenamiento))

        #Modelo SVM
        sv = svm.SVC(kernel='linear') # Linear Kernel 
        sv.fit(X_train, y_train) 
        y_pred = sv.predict(X_test)
        with open('modelo_SVM.pkl', 'wb') as mod:
            pickle.dump(sv,mod)
        exactitud_sv = metrics.accuracy_score(y_test, y_pred)
        if porcentaje < exactitud_sv:
            porcentaje = exactitud_sv
            modelo = "SVM"
            fichero = "modelo_SVM.pkl"
        c.execute ('insert into entrena_modelo (modelo,fichero,porcentaje,entrenado) values (?,?,?,?)', ("SVM","modelo_SVM.pkl",round((exactitud_sv*100)),entrenamiento))
        
        # Naives Bayes
        gnb = GaussianNB()
        gnb.fit(X_train, y_train)
        y_pred = gnb.predict(X_test)
        with open('modelo_GNB.pkl', 'wb') as mod:
            pickle.dump(gnb,mod)
        exactitud_gnb = metrics.accuracy_score(y_test, y_pred)
        if porcentaje < exactitud_gnb:
            porcentaje = exactitud_gnb
            modelo = "GaussianNB"
            fichero = "modelo_GNB.pkl"
        c.execute ('insert into entrena_modelo (modelo,fichero,porcentaje,entrenado) values (?,?,?,?)', ("GaussianNB","modelo_GNB.pkl",round((exactitud_gnb*100)),entrenamiento))

        # Modelo Decision Tree
        dt = DecisionTreeClassifier()
        dt = dt.fit(X_train, y_train)
        y_pred = dt.predict(X_test)
        with open('modelo_DT.pkl', 'wb') as mod:
            pickle.dump(dt,mod)
        exactitud_dt = metrics.accuracy_score(y_test, y_pred)
        if porcentaje < exactitud_dt:
            porcentaje = exactitud_dt
            modelo = "DecisionTreeClassifier"
            fichero = "modelo_DT.pkl"
        c.execute ('insert into entrena_modelo (modelo,fichero,porcentaje,entrenado) values (?,?,?,?)', ("DecisionTreeClassifier","modelo_DT.pkl",round((exactitud_dt*100)),entrenamiento))
        

        # modelo Random Forest
        rf = RandomForestClassifier(n_estimators=100)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_test)
        with open('modelo_RF.pkl', 'wb') as mod:
            pickle.dump(rf,mod)
        exactitud_rf = metrics.accuracy_score(y_test, y_pred)
        if porcentaje < exactitud_rf:
            porcentaje = exactitud_rf
            modelo = "RandomForestClassifier"
            fichero = "modelo_RF.pkl"
        c.execute ('insert into entrena_modelo (modelo,fichero,porcentaje,entrenado) values (?,?,?,?)', ("RandomForestClassifier","modelo_RF.pkl",round((exactitud_rf*100)),entrenamiento))
            
        gb_clf = GradientBoostingClassifier(n_estimators=150, max_features=20, max_depth=20, random_state=0)
        gb_clf.fit(X_train, y_train)
        y_pred = rf.predict(X_test)
        with open('modelo_GBC.pkl', 'wb') as mod:
            pickle.dump(gb_clf,mod)
        exactitud_gbc = metrics.accuracy_score(y_test, y_pred)
        if porcentaje < exactitud_gbc:
            porcentaje = exactitud_gbc
            modelo = "GradientBoostingClassifier"
            fichero = "modelo_GBC.pkl"
        c.execute ('insert into entrena_modelo (modelo,fichero,porcentaje,entrenado) values (?,?,?,?)', ("GradientBoostingClassifier","modelo_GBC.pkl",round((exactitud_gbc*100)),entrenamiento))
        conexion.commit()
        return(porcentaje, modelo,fichero)
    except:
        print("en el error de entrena modelo")
        print("Error inesperado:", sys.exc_info()[0])
        conexion.rollback()
        return (0,0,0)
        
    finally:
        conexion.close()

