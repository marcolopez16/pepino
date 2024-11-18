import streamlit as st
import pandas as pd
import calendar
from datetime import datetime, date

# Configuración inicial
st.title("Calendario Interactivo de Exámenes 2024-2025")

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

# Inicializar eventos almacenados
if "eventos" not in st.session_state:
    st.session_state.eventos = {fecha: descripcion for fecha, descripcion in fiestas.items()}

# Función para mostrar el calendario
def crear_calendario_interactivo(anio, mes):
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
                fecha_str = fecha.strftime("%Y-%m-%d")
                eventos_dia = st.session_state.eventos.get(fecha_str, "")

                # Botón interactivo para cada día
                if col.button(f"{dia}"):
                    st.session_state.selected_date = fecha_str
                
                # Mostrar eventos debajo del día
                if eventos_dia:
                    col.caption(eventos_dia)

# Función para añadir eventos
def agregar_evento():
    if "selected_date" in st.session_state:
        fecha = st.session_state.selected_date
        st.subheader(f"Añadir evento para el {fecha}")
        evento = st.text_input("Descripción del evento", key="nuevo_evento")
        
        if st.button("Guardar evento"):
            if evento.strip():
                st.session_state.eventos[fecha] = evento
                st.success(f"Evento añadido para el {fecha}")
            else:
                st.error("El evento no puede estar vacío.")
            del st.session_state.selected_date

# Selección de mes y año
st.sidebar.header("Seleccionar mes y año")
mes = st.sidebar.selectbox("Mes", list(range(1, 13)), format_func=lambda x: calendar.month_name[x])
anio = st.sidebar.selectbox("Año", [2024, 2025])

# Mostrar el calendario interactivo
crear_calendario_interactivo(anio, mes)

# Mostrar el formulario para añadir eventos si se seleccionó un día
agregar_evento()

# Mostrar todos los eventos registrados
if st.button("Ver todos los eventos"):
    st.subheader("Eventos registrados")
    for fecha, evento in sorted(st.session_state.eventos.items()):
        st.write(f"**{fecha}**: {evento}")
