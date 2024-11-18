import streamlit as st
import pandas as pd
import calendar
from datetime import datetime, date

# Configuración inicial
st.title("Calendario de Exámenes 2024-2025")

# Fiestas importantes de España
fiestas = {
    "2024-10-12": "Día de la Hispanidad",
    "2024-12-25": "Navidad",
    "2025-03-29": "Domingo de Ramos",
    "2025-04-03": "Jueves Santo",
    "2025-04-04": "Viernes Santo",
    "2025-04-20": "Día de San Jorge (Aragón)",
    "2025-05-01": "Día del Trabajador",
}

# Función para generar un calendario
def crear_calendario(anio, mes, eventos):
    cal = calendar.Calendar(firstweekday=0)
    dias_mes = cal.monthdayscalendar(anio, mes)
    nombre_mes = calendar.month_name[mes]

    # Mostrar el nombre del mes
    st.subheader(f"{nombre_mes} {anio}")
    
    # Encabezados de los días de la semana
    cols = st.columns(7)
    dias_semana = ["L", "M", "X", "J", "V", "S", "D"]
    for col, dia in zip(cols, dias_semana):
        col.markdown(f"**{dia}**", unsafe_allow_html=True)

    # Mostrar los días del mes
    for semana in dias_mes:
        cols = st.columns(7)
        for col, dia in zip(cols, semana):
            if dia == 0:  # Día vacío
                col.write("")
            else:
                fecha = date(anio, mes, dia)
                eventos_dia = eventos.get(fecha.strftime("%Y-%m-%d"), "")
                if eventos_dia:
                    col.markdown(f"**{dia}** 🎉")
                    col.caption(eventos_dia)
                else:
                    col.write(dia)

# Crear un diccionario con eventos
eventos = {fecha: descripcion for fecha, descripcion in fiestas.items()}

# Agregar exámenes al diccionario de eventos
st.sidebar.header("Añadir examen")
examen_fecha = st.sidebar.date_input("Fecha del examen")
examen_nombre = st.sidebar.text_input("Nombre del examen")

if st.sidebar.button("Guardar examen"):
    eventos[examen_fecha.strftime("%Y-%m-%d")] = examen_nombre
    st.sidebar.success(f"Examen '{examen_nombre}' guardado para el {examen_fecha.strftime('%d/%m/%Y')}")

# Selección de mes y año
st.sidebar.header("Seleccionar mes y año")
mes = st.sidebar.selectbox("Mes", list(range(1, 13)), format_func=lambda x: calendar.month_name[x])
anio = st.sidebar.selectbox("Año", [2024, 2025])

# Mostrar el calendario
crear_calendario(anio, mes, eventos)
