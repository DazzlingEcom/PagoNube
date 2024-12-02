import streamlit as st
import pandas as pd

# Título de la aplicación
st.title("Procesador Automático de CSV - Filtro por 'Valor Neto'")

# Subida del archivo CSV
uploaded_file = st.file_uploader("Sube un archivo CSV", type="csv")

if uploaded_file is not None:
    # Leer el archivo CSV en un DataFrame
    df = pd.read_csv(uploaded_file)

    # Mostrar el contenido del CSV
    st.subheader("Vista previa del archivo CSV:")
    st.dataframe(df)

    # Verificar si la columna 'valor neto' existe
    if 'valor neto' in df.columns:
        # Convertir 'valor neto' a un tipo numérico (si no lo está)
        df['valor neto'] = pd.to_numeric(df['valor neto'], errors='coerce')

        # Filtrar automáticamente los datos por un rango predeterminado
        st.subheader("Filtro Automático en 'Valor Neto'")
        min_value = st.number_input("Valor mínimo:", value=float(df['valor neto'].min()))
        max_value = st.number_input("Valor máximo:", value=float(df['valor neto'].max()))
        filtered_data = df[(df['valor neto'] >= min_value) & (df['valor neto'] <= max_value)]

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
        st.error("La columna 'valor neto' no se encontró en el archivo CSV. Por favor, sube un archivo válido.")
