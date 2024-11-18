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

# Colores disponibles
colores_disponibles = {
    "Rojo": "#FF0000",
    "Azul": "#0000FF",
    "Amarillo": "#FFFF00",
    "Verde": "#008000",
    "Rosa": "#FFC0CB",
    "Naranja": "#FFA500",
    "Negro": "#000000",
    "Blanco": "#FFFFFF",
}

# Inicializar eventos almacenados
if "eventos" not in st.session_state:
    st.session_state.eventos = {}

# Inicializar selección de color actual
if "color_seleccionado" not in st.session_state:
    st.session_state.color_seleccionado = "#FFFFFF"

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
        col.markdown(f"<div style='text-align: center; font-weight: bold;'>{dia}</div>", unsafe_allow_html=True)

    # Mostrar los días del mes
    for semana in dias_mes:
        cols = st.columns(7)
        for col, dia in zip(cols, semana):
            col.markdown("<div style='display: flex; flex-direction: column; align-items: center;'>", unsafe_allow_html=True)

            if dia == 0:  # Día vacío
                col.write("")
            else:
                fecha = date(anio, mes, dia)
                fecha_str = fecha.strftime("%Y-%m-%d")
                evento = st.session_state.eventos.get(fecha_str, {})
                color = evento.get("color", "#F0F0F0")  # Color predeterminado

                # El número como botón
                if col.button(f"{dia}", key=f"boton_{fecha_str}"):
                    st.session_state.selected_date = fecha

                # Etiqueta debajo del número
                descripcion_corta = " ".join(evento.get("descripcion", "").split()[:2])
                etiqueta_html = f"""
                <div style="
                    background-color: {color if descripcion_corta else 'transparent'};
                    color: white;  /* Texto de la etiqueta en blanco */
                    text-align: center;
                    padding: 5px;
                    border-radius: 5px;  /* Bordes redondeados */
                    font-size: 12px;
                    font-weight: bold;
                    width: 60px;
                    min-height: 15px;  /* Espacio reservado para la etiqueta */
                    margin-top: 5px;">
                    {descripcion_corta}
                </div>
                """
                col.markdown(etiqueta_html, unsafe_allow_html=True)

            col.markdown("</div>", unsafe_allow_html=True)

# Función para gestionar el evento seleccionado
def gestionar_evento():
    if "selected_date" in st.session_state:
        fecha = st.session_state.selected_date
        fecha_str = fecha.strftime("%Y-%m-%d")
        fecha_formato_texto = fecha.strftime(f"%d de {meses_esp[fecha.month]} de %Y")  # Mes en español

        st.subheader(f"Gestionar evento para el {fecha_formato_texto}")

        # Recuperar el evento actual si existe
        evento_actual = st.session_state.eventos.get(fecha_str, {})

        # Mostrar el formulario para añadir o editar evento
        descripcion = st.text_input("Descripción del evento", value=evento_actual.get("descripcion", ""))

        # Selector visual de colores
        st.write("Elige un color para este evento:")
        col_selector = st.columns(len(colores_disponibles))
        for idx, (nombre, hex_color) in enumerate(colores_disponibles.items()):
            button_html = f"""
            <button style="
                background-color: {hex_color};
                border: none;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                cursor: pointer;">
            </button>
            """
            col_selector[idx].markdown(button_html, unsafe_allow_html=True)
            # Mostrar rectángulo con el color debajo del botón
            col_selector[idx].markdown(
                f"<div style='background-color: {hex_color}; width: 60px; height: 20px; border-radius: 3px; margin-top: 5px;'></div>", 
                unsafe_allow_html=True
            )

            if col_selector[idx].button(f"{nombre}", key=f"color_{hex_color}"):
                st.session_state.color_seleccionado = hex_color

        color_final = st.session_state.color_seleccionado

        if st.button("Guardar evento"):
            if descripcion.strip():
                # Guardar el evento y color
                st.session_state.eventos[fecha_str] = {"descripcion": descripcion, "color": color_final}
                st.success(f"Evento guardado para el {fecha_formato_texto}")
            else:
                st.error("La descripción del evento no puede estar vacía.")

# Selección de mes y año
st.sidebar.header("Seleccionar mes y año")
mes = st.sidebar.selectbox("Mes", list(range(1, 13)), format_func=lambda x: meses_esp[x])
anio = st.sidebar.selectbox("Año", [2024, 2025])

# Mostrar el calendario interactivo
crear_calendario_interactivo(anio, mes)

# Gestionar el evento seleccionado
gestionar_evento()

# Mostrar todos los eventos registrados
if st.button("Ver todos los eventos"):
    st.subheader("Eventos registrados")
    for fecha, evento in sorted(st.session_state.eventos.items()):
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
        dia_semana = dias_semana[fecha_obj.weekday()]  # Obtener día de la semana
        fecha_formateada = fecha_obj.strftime(f"%d de {meses_esp[fecha_obj.month]} de %Y ({dia_semana})")
        st.write(f"**{fecha_formateada}**: {evento['descripcion']}")
