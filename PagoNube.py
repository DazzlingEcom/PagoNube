import streamlit as st
import pandas as pd

# Título de la aplicación
st.title("Procesador Automático de CSV - Valor Neto")

# Subida del archivo CSV
uploaded_file = st.file_uploader("Sube un archivo CSV", type="csv")

if uploaded_file is not None:
    # Leer el archivo CSV sin encabezados
    df = pd.read_csv(uploaded_file, header=None, sep=';')

    # Agregar un encabezado provisional para identificar columnas
    df.columns = [f"col_{i}" for i in range(df.shape[1])]

    # Extraer el último número (valor neto) de cada fila
    df["valor_neto"] = pd.to_numeric(df.iloc[:, -1], errors="coerce")

    # Mostrar vista previa del archivo
    st.subheader("Vista previa del archivo original:")
    st.dataframe(df)

    # Filtrar datos automáticamente por un rango en "valor_neto"
    st.subheader("Filtro Automático en 'Valor Neto'")
    min_value = st.number_input("Valor mínimo:", value=float(df["valor_neto"].min()))
    max_value = st.number_input("Valor máximo:", value=float(df["valor_neto"].max()))
    filtered_data = df[(df["valor_neto"] >= min_value) & (df["valor_neto"] <= max_value)]

    # Mostrar datos filtrados
    st.write("Datos filtrados:")
    st.dataframe(filtered_data)

    # Descargar datos filtrados
    csv = filtered_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Descargar CSV Filtrado",
        data=csv,
        file_name='datos_filtrados.csv',
        mime='text/csv'
    )
else:
    st.info("Por favor, sube un archivo CSV para comenzar.")
