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

# Mostrar el calendario filtrado por mes
month = st.sidebar.selectbox("Selecciona un mes", options=pd.date_range(start=start_date, end=end_date, freq='MS').strftime('%B %Y'))

# Filtrar las fechas del mes seleccionado
month_start = datetime.strptime(month, "%B %Y")
month_end = month_start + pd.DateOffset(months=1) - timedelta(days=1)
month_view = calendar_df[(calendar_df["Fecha"] >= month_start) & (calendar_df["Fecha"] <= month_end)]

# Mostrar el mes
st.subheader(f"Calendario de {month}")

# Dividir el mes en semanas y mostrar los días
days_of_week = ["L", "M", "X", "J", "V", "S", "D"]
start_weekday = month_start.weekday()  # Día de la semana del primer día del mes
days_in_month = (month_end - month_start).days + 1

# Inicializar las columnas para el calendario
columns = st.columns(7)

# Mostrar los días de la semana
for i, day in enumerate(days_of_week):
    columns[i].write(day)

# Mostrar el calendario del mes
day_counter = 0
for i in range(start_weekday):
    columns[i].write("")  # Espacios vacíos antes del primer día del mes

for i in range(day_counter, days_in_month + day_counter):
    day_date = month_start + timedelta(days=i)
    day_event = month_view[month_view["Fecha"] == day_date]["Evento"].values
    event_text = day_event[0] if len(day_event) > 0 else ""
    columns[(i + start_weekday) % 7].write(f"{day_date.day}\n{event_text}")

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
