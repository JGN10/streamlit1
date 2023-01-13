import pandas as pd
import streamlit as st
import plotly.figure_factory as ff
import plotly.express as px
import matplotlib.pyplot as plt 
import seaborn as sns
from pyspark.sql import SparkSession
import plotly
import extra_streamlit_components as stx


#@st.cache()
def leer_csv(fichero):
    return pd.read_csv(fichero)

df=leer_csv("diabetes.csv")


def f_lineas():
    st.subheader ("La información de las líneas que quiere mostrar son: ")
    col1, col2, col3  = st.columns(3)
    with col1:
        numero_lineas = st.number_input('Inserte el número de líneas', min_value=0, format='%i')
    df_aux = df.head(int(numero_lineas))
    st.dataframe(df_aux)

def f_describe():
    with st.expander("Sección información columnas", True):
        st.subheader ("La información estadística de las columnas del fichero: ")
        df_describe = df.describe()
        st.dataframe(df_describe)

def boton_refrescar(columnas):
    columnas_sel = []
    for col in columnas:
        columnas_sel.append(col)    
    print(columnas_sel)
    if c_embarazo:
        print("el embarazo 1 ",v_embarazo[0])
        print("el embarazo 2 ",v_embarazo[1])
    df_aux2=df[columnas_sel].head(int(numero_lineas_filtros))
    st.dataframe(df_aux2)


def f_filtros():
    with st.expander("Sección filtrado de información", True):
        st.subheader ("La información filtrada del fichero: ")
        col1, col2, col3  = st.columns(3)
        with col1:
            numero_lineas_filtros = st.number_input('Inserte el número de líneas a mostrar', min_value=0, format='%i')
        columnas = st.multiselect(
            'Seleccione las columnas a visualizar',
            ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness','Insulin','BMI','DiabetesPedigreeFunction','Age','Outcome'],
            ['Pregnancies'])
        #with st.expander("Sección filtros", True):

        col1, col2,col3,col4 = st.columns([1,2,1,2])
        with col1:
            c_embarazo = st.checkbox("Embarazos")
        with col2:
            if c_embarazo:
                v_embarazo = st.slider('Embarazos',int(df['Pregnancies'].min()), int(df['Pregnancies'].max()), (0, 4))    
        #col_2_1, col_2_2,col_2_3 = st.columns([1,2,4])
        with col3:#col_2_1:
            c_glucosa = st.checkbox("Glucosa")
        with col4:#col_2_2:
            if c_glucosa:
                v_glucosa = st.slider('Glucosa',int(df['Glucose'].min()), int(df['Glucose'].max()), (100,130))    
        
        col_2_1, col_2_2,col_2_3,col_2_4 = st.columns([1,2,1,2])
        with col_2_1:
            c_presion = st.checkbox('P. Arterial')
        with col_2_2:
            if c_presion:
                v_presion = st.slider('P. Arterial',int(df['BloodPressure'].min()), int(df['BloodPressure'].max()), (60,80))    
        #col_4_1, col_4_2,col_4_3 = st.columns([1,2,4])
        with col_2_3:
            c_piel = st.checkbox('Piel Triceps')
        with col_2_4:
            if c_piel:
                v_piel = st.slider('Piel Triceps',int(df['SkinThickness'].min()), int(df['SkinThickness'].max()), (10,30))    

        col_3_1, col_3_2,col_3_3,col_3_4 = st.columns([1,2,1,2])
        with col_3_1:
            c_insulina = st.checkbox('Insulina')
        with col_3_2:
            if c_insulina:
                v_insulina = st.slider('Insulina',int(df['Insulin'].min()), int(df['Insulin'].max()), (40,120))    
        #col_6_1, col_6_2,col_6_3 = st.columns([1,2,4])
        with col_3_3:
            c_indice = st.checkbox('IMC')
        with col_3_4:
            if c_indice:
                v_indice = st.slider('IMC',float(df['BMI'].min()), float(df['BMI'].max()), (20.0,40.0))    

        col_4_1, col_4_2,col_4_3, col_4_4 = st.columns([1,2,1,2])
        with col_4_1:
            c_pedigri = st.checkbox('DPF')
        with col_4_2:
            if c_pedigri:
                v_pedigri = st.slider('DPF',float(df['DiabetesPedigreeFunction'].min()), float(df['DiabetesPedigreeFunction'].max()), (0.20,10.60))    
        #col_8_1, col_8_2,col_8_3 = st.columns([1,2,4])
        with col_4_3:
            c_edad = st.checkbox('Edad')
        with col_4_4:
            if c_edad:
                v_edad = st.slider('Edad',int(df['Age'].min()), int(df['Age'].max()), (20,40))    

        col_5_1, col_5_2,col_5_3,col_5_4 = st.columns([1,2,1,2])
        with col_5_1:
            c_resultado = st.checkbox('Predicción')
        with col_5_2:
            if c_resultado:
                v_resultado = st.slider('Predicción',int(df['Outcome'].min()), int(df['Outcome'].max()), (0,1)) 
        
        df_filtrado = df.copy()
        if c_embarazo:
            df_filtrado = df_filtrado[(df_filtrado['Pregnancies'] >= v_embarazo[0]) &\
                                    (df_filtrado['Pregnancies'] <= v_embarazo[1])] 
        if c_glucosa:
            df_filtrado = df_filtrado[(df_filtrado['Glucose'] >= v_glucosa[0]) &\
                                    (df_filtrado['Glucose'] <= v_glucosa[1])] 
        if c_presion:
            df_filtrado = df_filtrado[(df_filtrado['BloodPressure'] >= v_presion[0]) &\
                                    (df_filtrado['BloodPressure'] <= v_presion[1])] 
        if c_piel:
            df_filtrado = df_filtrado[(df_filtrado['SkinThickness'] >= v_piel[0]) &\
                                    (df_filtrado['SkinThickness'] <= v_piel[1])] 
        if c_insulina:
            df_filtrado = df_filtrado[(df_filtrado['Insulin'] >= v_insulina[0]) &\
                                    (df_filtrado['Insulin'] <= v_insulina[1])] 
        if c_indice:
            df_filtrado = df_filtrado[(df_filtrado['BMI'] >= v_indice[0]) &\
                                    (df_filtrado['BMI'] <= v_indice[1])]
        if c_pedigri:
            df_filtrado = df_filtrado[(df_filtrado['DiabetesPedigreeFunction'] >= v_pedigri[0]) &\
                                    (df_filtrado['DiabetesPedigreeFunction'] <= v_pedigri[1])]
        if c_edad:
            df_filtrado = df_filtrado[(df_filtrado['Age'] >= v_edad[0]) &\
                                    (df_filtrado['Age'] <= v_edad[1])]
        if c_resultado:
            df_filtrado = df_filtrado[(df_filtrado['Outcome'] >= v_resultado[0]) &\
                                    (df_filtrado['Outcome'] <= v_resultado[1])]
        
        columnas_sel = []
        for col in columnas:
            columnas_sel.append(col)    
        #print(columnas_sel)
        df_aux2=df_filtrado[columnas_sel].head(int(numero_lineas_filtros))
        st.dataframe(df_aux2)

        
        

def f_diabetes():
    with st.expander("Sección muestreo de positivos", True):
        fig = plt.figure(figsize=(10,2))
        sns.countplot(x=df["Outcome"])
        st.subheader("En el siguiente gráfico se muestran el número de positivos(1) y negativos(0) de diabetes en el fichero utilizado ")
        st.plotly_chart(fig)

def f_histo():
    with st.expander("Sección histogramas", True):
        col1, col2 = st.columns(2)
        with col1:
            opcion = st.selectbox("Seleccione la columna a mostrar", ("Embarazos","Glucosa","Presión Arterial","Grosor piel del triceps","Insulina", "IMC", "DPF", "Edad"))
        with col2:
            tipo = st.selectbox("Seleccione el tipo de gráfico", ("Estáticos","Dinámicos"))

        if opcion == "Embarazos":
            grafico = "Pregnancies"
        elif opcion == "Edad":
            grafico = "Age"
        elif opcion == "IMC":
            grafico = "BMI"
        elif opcion == "Glucosa":
            grafico = "Glucose"
        elif opcion == "Presión Arterial":
            grafico = "BloodPressure"
        elif opcion == "Grosor piel del triceps":
            grafico = "SkinThickness"
        elif opcion == "Insulina":
            grafico = "Insulin"
        elif opcion == "DPF":
            grafico = "DiabetesPedigreeFunction"
        
        c1,c2 = st.columns(2)
        with c1:
            fig_his=plt.figure(figsize=(5,5))
            sns.histplot(data = df,
                x = grafico,
                hue="Outcome",
                multiple="stack")
            cadena = "histograma de " + grafico
            #plt.title(cadena )
            cadena = "Histograma de " + grafico
            st.subheader(cadena)
            if tipo == "Estáticos":
                st.pyplot(fig_his)
            else:
                st.plotly_chart(fig_his, use_container_width=False)

        with c2:
            cadena = "Boxplot de " + grafico
            #plt.title(cadena )
            cadena = "Boxplot de " + grafico
            st.subheader(cadena)
            if tipo == "Estáticos":
                fig_box=plt.figure(figsize=(8,7.5))
                
                # grafico con seaborn:
                sns.boxplot(x="Outcome", y=grafico, data=df)
                st.pyplot(fig_box)
            else:
            # Plotly:
                fig =plt.figure(figsize=(1,1))
                fig = px.box(df, x="Outcome", y=grafico,width=100,height=475)
                st.plotly_chart(fig, use_container_width=True)
            
            #kind = "box")
            # st.plotly_chart(fig_box)

def f_puntos():
    with st.expander("Sección diagrama de puntos", True):
        
        c1,c2,c3 = st.columns(3)
        with c1:
            opciony = st.selectbox("Columna eje de ordenadas (y) ", ("Embarazos","Glucosa","Presión Arterial","Grosor piel del triceps","Insulina", "IMC", "DPF", "Edad"))
        with c2:
            opcionx = st.selectbox("Columna eje de abscisas (x)", ("Embarazos","Glucosa","Presión Arterial","Grosor piel del triceps","Insulina", "IMC", "DPF", "Edad"))
        with c3:
            tipo = st.selectbox("Seleccione tipo de gráfico", ("Estáticos","Dinámicos"))

        cadena = "Diagrama de puntos de los valores de " + opcionx + " y " + opciony
        st.subheader(cadena)
        if opcionx == "Embarazos":
            columnax = "Pregnancies"
        elif opcionx == "Edad":
            columnax = "Age"
        elif opcionx == "IMC":
            columnax = "BMI"
        elif opcionx == "Glucosa":
            columnax = "Glucose"
        elif opcionx == "Presión Arterial":
            columnax = "BloodPressure"
        elif opcionx == "Grosor piel del triceps":
            columnax = "SkinThickness"
        elif opcionx == "Insulina":
            columnax = "Insulin"
        elif opcionx == "DPF":
            columnax = "DiabetesPedigreeFunction"

        if opciony == "Embarazos":
            columnay = "Pregnancies"
        elif opciony == "Edad":
            columnay = "Age"
        elif opciony == "IMC":
            columnay = "BMI"
        elif opciony == "Glucosa":
            columnay = "Glucose"
        elif opciony == "Presión Arterial":
            columnay = "BloodPressure"
        elif opciony == "Grosor piel del triceps":
            columnay = "SkinThickness"
        elif opciony == "Insulina":
            columnay = "Insulin"
        elif opciony == "DPF":
            columnay = "DiabetesPedigreeFunction"

        


        # Plot!
        if tipo == "Estáticos":
            #fig=plt.figure(figsize=(8,7.5))
            fig = plt.figure(figsize=(10,10))
            sns.scatterplot(data=df, x=columnax, y=columnay, hue="Outcome")

            #fig, ax =plt.subplots()
            
            #ax.scatter(df[columnax], df[columnay], c=df['Outcome'],height = 400)
            #plt.ylabel(columnay)
            #plt.xlabel(columnax)
            #plt.legend(df['Outcome'])            
            st.pyplot(fig)
        else:
            #fig=plt.figure(figsize=(8,7.5))
            fig = px.scatter(df, x=columnax, y=columnay, color="Outcome") #, width=50, height= 150)
            st.plotly_chart(fig, use_container_width=True)

def f_mapa():
    with st.expander("Sección diagrama de puntos", True):
        c1,c2,c3 = st.columns(3)
        with c1:
            tipo = st.selectbox("Seleccione el tipo del gráfico", ("Estáticos","Dinámicos"))

        if tipo == "Estáticos":
            fig, ax = plt.subplots()
            cadena = "Diagrama de calor/correlación" 
            st.subheader(cadena)
            sns.heatmap(df.corr(), ax=ax, annot=True)
            st.write(fig)
        else:
            fig1 =px.imshow(df.corr(), text_auto=True)
            st.plotly_chart(fig1,use_container_width=True)

def f_conclusion():
    with st.expander("Sección análisis y conclusión", True):
        #st.subheader(f"El algoritmo utilizado ha sido {st.session_state.modelo}GradientBoostingClassifier, con una precisión de más de un 82%")
        st.subheader(f"El algoritmo utilizado ha sido {st.session_state.modelo}, con una precisión de más de un {round((st.session_state.porcentaje*100),2)}%")



st.title("Análisis realizado a la información")

tab1, tab2, tab3, tab4, tab5, tab6,tab7 = st.tabs(["Análisis", "Información Fichero","Muestra de Resultados", "Histogramas","Diagramas de puntos","Mapa de calor", "Conclusión"])
with tab1:
    st.write("En las diferentes pestañas de esta ventana, se puede visualizar los datos del fichero utilizado. "\
        + "También se puede ver los diversos gráficos que han ayudado a tomar una decisión sobre el modelo "\
        + "a utilizar en la predicción")

with tab2:
    f_lineas()
    f_describe()
    f_filtros()
    st.write("En el fichero original se ha observado que:")
    st.write("- Todos los campos son numéricos.")
    st.write("- No hay ninguna columna con valores nulos.")
    st.write("- Existen valores 0 en ciertas columnas que médicamente no son posibles,"\
        + " por lo que se tendrán que modificar.")

with tab3:
    f_diabetes()
    st.write("Se muestran el volumen de los datos positivos y negativos del conjunto del fichero utilizado.")
    st.write("Existiendo muchas más personas que NO están diagnosticadas con diabetes de las que si lo están")
with tab4:
    f_histo()
    st.write("Con este tipo de gráficos, se han visto que hay ciertas columnas que tienen muchos valores atípicos"\
        + " por lo para dichas columnas se tendrá que utilizar la mediana y no la media para sustituir los valores 0")
    st.write("La mediana se ve mucho menos afectada por los valores atípicos, que la media")
    st.write("las columnas con valores 0 y que sus valores se sustituirán son:")
    st.write("- Columna glucosa, dispone de una distribución normal, por lo que se utilizará la media")
    st.write("- Columna presión arterial, dispone de una distribución normal, por lo que se utilizará la media")
    st.write("- Columna grosor de piel, dispone de valores atípicos, por lo que se utilizará la mediana")
    st.write("- Columna insulina, dispone de valores atípicos, por lo que se utilizará la mediana")
    st.write("- Columna índice de masa corporal, dispone de valores atípicos, por lo que se utilizará la mediana")

with tab5:
    f_puntos()
    st.write("No se ve ningun grupo de dos variables que se pueda utilizar para la predicción. El resultado debe "\
        + "estar definido por más variables.")
    
with tab6:
    f_mapa()
    st.write("Existen algunas columnas que tienen menos correlación con el resultado de la predicción, pero no es "\
        + "una correlación muy baja, para descartar dichas columnas del algoritmo a utilizar")
with tab7:
    f_conclusion()
    st.write("El mejor resultado se ha alcanzado utilizando todas las columnas, "\
        + "incluidas las de menor correlación.")
    st.write("Se han utilizado varios algoritmos de clasificación y el que mejor se ha comportado a lo largo "\
        + f"de las pruebas ha sido el {st.session_state.modelo}. Se han llegado a alcanzar siempre valores "\
        + "por encima del 80% de precisión")

