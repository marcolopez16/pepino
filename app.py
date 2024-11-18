import streamlit as st
import pandas as pd
import calendar
from datetime import datetime, date

# Configuración inicial
st.title("Calendario Interactivo de Exámenes 2024-2025")

# Traducción de los días y meses al español
dias_semana = ["L", "M", "X", "J", "V", "S", "D"]
meses_esp = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

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
    nombre_mes = meses_esp[mes]

    # Mostrar el nombre del mes
    st.subheader(f"{nombre_mes} {anio}")

    # Encabezados de los días de la semana
    cols = st.columns(7)
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

                # Mostrar el botón con color dinámico
                if eventos_dia:
                    if col.button(f"{dia}", key=f"boton_{fecha_str}", help=eventos_dia):
                        st.session_state.selected_date = fecha
                        st.success(f"Seleccionaste el {fecha.strftime('%d/%m/%Y')}")
                else:
                    if col.button(f"{dia}", key=f"boton_{fecha_str}"):
                        st.session_state.selected_date = fecha

# Función para añadir eventos
def agregar_evento():
    if "selected_date" in st.session_state:
        fecha = st.session_state.selected_date
        fecha_formato_texto = fecha.strftime("%d de %B de %Y").capitalize()
        fecha_formato_corto = fecha.strftime("%d-%m-%Y")

        # Reemplazar los nombres de los meses con el diccionario español
        for numero_mes, nombre_mes in meses_esp.items():
            fecha_formato_texto = fecha_formato_texto.replace(fecha.strftime("%B"), nombre_mes)

        st.subheader(f"Añadir evento para el {fecha_formato_texto} ({fecha_formato_corto})")
        evento = st.text_input("Descripción del evento", key="nuevo_evento")

        if st.button("Guardar evento"):
            if evento.strip():
                st.session_state.eventos[fecha.strftime("%Y-%m-%d")] = evento
                st.success(f"Evento añadido para el {fecha_formato_texto}")
            else:
                st.error("El evento no puede estar vacío.")
            del st.session_state.selected_date

# Selección de mes y año
st.sidebar.header("Seleccionar mes y año")
mes = st.sidebar.selectbox("Mes", list(range(1, 13)), format_func=lambda x: meses_esp[x])
anio = st.sidebar.selectbox("Año", [2024, 2025])

# Mostrar el calendario interactivo
crear_calendario_interactivo(anio, mes)

# Mostrar el formulario para añadir eventos si se seleccionó un día
agregar_evento()

# Mostrar todos los eventos registrados
if st.button("Ver todos los eventos"):
    st.subheader("Eventos registrados")
    for fecha, evento in sorted(st.session_state.eventos.items()):
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
        dia_semana = dias_semana[fecha_obj.weekday()]  # Obtener día de la semana
        fecha_formateada = fecha_obj.strftime(f"%d de {meses_esp[fecha_obj.month]} de %Y ({dia_semana})")
        st.write(f"**{fecha_formateada}**: {evento}")
