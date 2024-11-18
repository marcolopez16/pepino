import streamlit as st
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
    "2024-10-12": {"descripcion": "Día de la Hispanidad", "color": "#FFCCCC"},
    "2024-12-25": {"descripcion": "Navidad", "color": "#FFD700"},
    "2025-03-29": {"descripcion": "Domingo de Ramos", "color": "#90EE90"},
    "2025-04-03": {"descripcion": "Jueves Santo", "color": "#87CEEB"},
    "2025-04-04": {"descripcion": "Viernes Santo", "color": "#87CEEB"},
    "2025-04-20": {"descripcion": "Día de San Jorge (Aragón)", "color": "#FF4500"},
    "2025-05-01": {"descripcion": "Día del Trabajador", "color": "#FFA07A"},
}

# Inicializar eventos almacenados
if "eventos" not in st.session_state:
    st.session_state.eventos = fiestas.copy()  # Cargar fiestas al inicio

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
                evento = st.session_state.eventos.get(fecha_str, {})
                color = evento.get("color", "#F0F0F0")  # Color predeterminado

                # Botón con color dinámico
                if col.button(f"{dia}", key=f"boton_{fecha_str}"):
                    st.session_state.selected_date = fecha

                col.markdown(
                    f"""
                    <style>
                    [key='boton_{fecha_str}'] {{
                        background-color: {color};
                        color: black;
                    }}
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

# Función para gestionar el formulario de eventos
def gestionar_evento():
    if "selected_date" in st.session_state:
        fecha = st.session_state.selected_date
        fecha_str = fecha.strftime("%Y-%m-%d")
        fecha_formato_texto = fecha.strftime("%d de %B de %Y").capitalize()

        st.subheader(f"Gestionar evento para el {fecha_formato_texto}")

        evento_actual = st.session_state.eventos.get(fecha_str, None)

        if evento_actual:
            # Mostrar el evento actual y el botón para editar
            st.write(f"**Evento actual**: {evento_actual['descripcion']}")
            st.write(f"**Color actual**: {evento_actual['color']}")
            if st.button("Editar evento"):
                st.session_state.edit_mode = True
        else:
            # Añadir un nuevo evento
            st.session_state.edit_mode = True

        # Mostrar el formulario si estamos en modo edición
        if "edit_mode" in st.session_state and st.session_state.edit_mode:
            descripcion = st.text_input("Descripción del evento", value=evento_actual["descripcion"] if evento_actual else "")
            color = st.color_picker("Elige un color para este evento", value=evento_actual["color"] if evento_actual else "#FFCCCC")

            if st.button("Guardar evento"):
                if descripcion.strip():
                    st.session_state.eventos[fecha_str] = {"descripcion": descripcion, "color": color}
                    st.success(f"Evento guardado para el {fecha_formato_texto}")
                    del st.session_state.edit_mode  # Salir del modo edición
                else:
                    st.error("El evento no puede estar vacío.")

# Selección de mes y año
st.sidebar.header("Seleccionar mes y año")
mes = st.sidebar.selectbox("Mes", list(range(1, 13)), format_func=lambda x: meses_esp[x])
anio = st.sidebar.selectbox("Año", [2024, 2025])

# Mostrar el calendario interactivo
crear_calendario_interactivo(anio, mes)

# Gestionar el formulario para el evento
gestionar_evento()

# Mostrar todos los eventos registrados
if st.button("Ver todos los eventos"):
    st.subheader("Eventos registrados")
    for fecha, evento in sorted(st.session_state.eventos.items()):
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
        dia_semana = dias_semana[fecha_obj.weekday()]  # Obtener día de la semana
        fecha_formateada = fecha_obj.strftime(f"%d de {meses_esp[fecha_obj.month]} de %Y ({dia_semana})")
        st.write(f"**{fecha_formateada}**: {evento['descripcion']}")
