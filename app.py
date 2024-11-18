import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Configuración inicial
st.title("Calendario de Exámenes 2024-2025")
st.sidebar.header("Opciones")

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

# Crear un DataFrame de fechas
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)
dates = pd.date_range(start=start_date, end=end_date)

calendar_df = pd.DataFrame({
    "Fecha": dates,
    "Evento": [""] * len(dates)
})

# Marcar las fiestas en el DataFrame
for fecha, fiesta in fiestas.items():
    fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
    calendar_df.loc[calendar_df["Fecha"] == fecha_obj, "Evento"] = fiesta

# Mostrar el calendario filtrado por semana
st.sidebar.subheader("Selecciona una semana")
start_week = st.sidebar.date_input("Inicio de la semana", value=datetime(2024, 1, 1))
end_week = start_week + timedelta(days=6)

# Convertir las fechas a formato datetime para evitar conflictos de tipos
start_week = pd.to_datetime(start_week)
end_week = pd.to_datetime(end_week)

week_view = calendar_df[
    (calendar_df["Fecha"] >= start_week) & (calendar_df["Fecha"] <= end_week)
]

# Tabla de la semana
st.subheader(f"Semana del {start_week.strftime('%d/%m/%Y')} al {end_week.strftime('%d/%m/%Y')}")
st.dataframe(week_view, use_container_width=True)

# Agregar exámenes
st.sidebar.subheader("Añadir examen")
examen_fecha = st.sidebar.date_input("Fecha del examen")
examen_nombre = st.sidebar.text_input("Nombre del examen")

if st.sidebar.button("Guardar examen"):
    examen_fecha = pd.to_datetime(examen_fecha)  # Asegurar compatibilidad de formato
    if examen_fecha in calendar_df["Fecha"].values:
        calendar_df.loc[calendar_df["Fecha"] == examen_fecha, "Evento"] = examen_nombre
        st.sidebar.success(f"Examen '{examen_nombre}' guardado el {examen_fecha.strftime('%d/%m/%Y')}")
    else:
        st.sidebar.error("Fecha fuera del rango del calendario.")

# Botón para ver todos los eventos
if st.button("Ver todos los eventos"):
    st.subheader("Todos los eventos registrados")
    eventos = calendar_df[calendar_df["Evento"] != ""]
    st.dataframe(eventos, use_container_width=True)
