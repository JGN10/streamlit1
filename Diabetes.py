import streamlit as st
import pickle
import pandas as pd
import setting


if "shared" not in st.session_state:
   st.session_state["shared"] = True
   st.session_state.g_lineas = False
   st.session_state.g_puntos = False
   st.session_state.g_numero_lineas = 0
   st.session_state.s_numero_lineas = 0
   st.set_page_config(layout="wide")
   st.session_state.nuevo_csv = setting.fichero_datos_usuario_csv
   st.session_state.mongodb = setting.mongodb
   st.session_state.postgredb = setting.postgredb
   st.session_state.sqlite = setting.DATABASE_SQLITE
   st.session_state.codigo_usuario = 0
   st.session_state.predicc_guardada = 0
   st.session_state.porcentaje = 0.82
   st.session_state.modelo = "GradientBoostingClassifier"
   st.session_state.fichero = "modelo_GBC.pkl"

st.session_state.g_pruebas = 0
st.session_state.g_analisis = 0
st.session_state.g_prediccion = 0
st.session_state.g_diabetes = 1

#st.title("_Prediccion de la posible aparicion de la diabetes_")
st.title("_Ayuda a la predicción de la Diabetes_")
st.warning("Atención, esta app es con fines educativos, no es una prueba médica ante cualquier resultado alarmante consulte a su médico")
st.title("_¿Qué es la Diabetes?_")
#st.write("La diabetes es una enfermedad en la que los niveles de glucosa (azúcar) de la sangre están muy altos. La glucosa proviene de los alimentos que consume. La insulina es una hormona que ayuda a que la glucosa entre a las células para suministrarles energía")
st.write("La diabetes es una enfermedad en la que los niveles de glucosa (azúcar) de la sangre"\
         + " están muy altos de manera persistente o crónica.")
st.write("La causa de esto niveles tan altos puede ser debido ya sea a un defecto en la producción"\
         +" de insulina, a una resistencia a la acción de ella para utilizar la glucosa, a un"\
         +" aumento en la producción de glucosa o a una combinación de todas ellas")         
st.write("Las consecuencias de sufrir esta enfermedad son varias, pudiendo afectar a la visión,"\
         +" riñones y complicaciones coronarias.")

st.title("_¿Qué función tiene esta aplicación?_")
st.write("Esta aplicación ayuda a la predicción para diagnosticar si una persona va a padecer diabetes."\
         + " Se basa en un modelo predictivo en el que a partir de los valores de ciertos"\
         + " parámetros de cada persona, se puede predecir con una alta probabilidad de acierto,"\
         + " si dicha persona padecerá o no diabetes")

st.title("_¿Qué es un modelo predictivo?_")
st.write("El modelo predictivo, es una aplicación informática que a partir de un fichero con datos reales y"\
         + " aplicando un algoritmo sobre dichos datos, se consigue predecir un resultado con una alta"\
         + " probabilidad de acierto, introduciendo nuevos valores, diferentes a los del fichero utilizado")

st.title("_¿Qué fichero se ha utilizado?_")
st.write("El fichero original que se ha utilizado para entrenar el modelo predictivo, tiene un volumen de 750 registros"\
         + ", en los que se reflejan diferentes valores que pueden afectar en el diagnostico de la diabetes")

st.title("_¿Cuales son los valores que afectan al diagnostico?,_")

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Embarazo", "Glucosa", "Presión arterial",\
                                                         "Grosor de la piel", "Insulina", "BMI",\
                                                         "Función de pedigrí de diabetes", "Edad"])
tab1.write("Si has estado embarazada o cuantas veces lo has estado en tu vida.")
#tab2.write("El azúcar en la sangre, también llamada _glucosa_ es el azúcar principal que se encuentra en su sangre. Esta proviene de los alimentos que usted consume y es su principal fuente de energía. Su sangre lleva la glucosa a todas las células de su cuerpo para ser usada como energía.")
tab2.write("Concentración de glucosa en plasma, durante una prueba de tolerancia oral a la glucosa.")
tab3.write("La presión arterial es la fuerza de su sangre al empujar contra las paredes de sus arterias.")
#tab4.write("La dermis mide unos cuatro milímetros de espesor y está dividida en tres zonas: la dermis papilar, la dermis reticular y la dermis profunda. Se trata de un complejo sistema de vasos sanguíneos, linfáticos, nervios y fibras entrelazadas, además de una gran variedad de tipos de células")
tab4.write("Espesor del pliegue de la piel del tríceps (mm).")
#tab5.write("Hormona elaborada por las células de los islotes del páncreas. La insulina controla la cantidad de azúcar en la sangre al almacenarla en las células, donde el cuerpo la puede usar como fuente de energía.")
tab5.write("Resultado de la prueba de insulina en sangre.")
#tab6.write("El body mass index BMI o índice de masa corporal en nutrición, es una metodología que se utiliza para estimar la cantidad de masa que tiene una persona en su cuerpo. Además, este método permite determinar si el peso de una persona está en el rango de lo normal, sufre de sobrepeso o está delgado.")
tab6.write("Indice de masa corporal o BMI en inglés. Resultado de dividir en peso en KGs"\
         + " por el cuadrado de la estatura en metros")
tab7.write("Función que califica la probabilidad de diabetes según los antecedentes familiares.")
tab8.write("Edad de la persona.")

st.title("_Las diferentes ventanas de la aplicación_")

tab1, tab2, tab3,tab4 = st.tabs(["Diabetes", "Análisis", "Predicción", "Mantenimiento"])
#tab1.write("Trata del apartado de informacion")
tab1.write("Ventana de inicio de la aplicación, donde se explica el funcionamiento de la misma")
tab2.write("Ventana donde se puede visualizar datos del fichero utilizado. Se muestran diferentes gráficos "\
         + "que han ayudado a seleccionar el modelo a utilizar y una breve conclusión")
tab3.write("Ventana en la que se introducen los valores particulares y en la que se pude realizar "\
         + "la predicción. También se puede guardar dicha predicción para ir enriqueciendo el fichero utilizado")
tab4.write("Ventana de mantenimiendo en la que se puede visualizar los registros pendientes de añadir al fichero."\
         + " Se podrán añadir los registros al fichero de datos y volver a entrenar el modelo.")
tab4.write("A esta ventana únicamente tendrán acceso los usuarios dados de alta en la aplicación"\
         + " y con rol de administrador.")



