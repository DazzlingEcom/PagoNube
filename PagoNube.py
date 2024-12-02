import streamlit as st
import pandas as pd

# Título de la aplicación
st.title("Procesador de Archivos CSV")

# Subida del archivo CSV
uploaded_file = st.file_uploader("Sube un archivo CSV", type="csv")

if uploaded_file is not None:
    # Leer el archivo CSV en un DataFrame
    df = pd.read_csv(uploaded_file)

    # Mostrar el contenido del CSV
    st.subheader("Vista previa del archivo CSV:")
    st.dataframe(df)

    # Extracción de información específica
    st.subheader("Extracción de datos específicos")

    # Mostrar columnas disponibles
    st.write("Columnas disponibles:", list(df.columns))

    # Selección de columna para analizar
    column_to_analyze = st.selectbox("Selecciona una columna para analizar:", df.columns)

    # Mostrar estadísticas básicas de la columna seleccionada
    if column_to_analyze:
        st.write(f"Estadísticas de la columna '{column_to_analyze}':")
        st.write(df[column_to_analyze].describe())

    # Filtro personalizado
    st.subheader("Filtrar datos")
    if st.checkbox("¿Deseas aplicar un filtro a los datos?"):
        filter_column = st.selectbox("Selecciona la columna para filtrar:", df.columns)
        if df[filter_column].dtype == 'object':
            unique_values = df[filter_column].unique()
            selected_value = st.selectbox(f"Selecciona un valor en '{filter_column}':", unique_values)
            filtered_data = df[df[filter_column] == selected_value]
        else:
            min_value = st.number_input(f"Valor mínimo para '{filter_column}':", value=float(df[filter_column].min()))
            max_value = st.number_input(f"Valor máximo para '{filter_column}':", value=float(df[filter_column].max()))
            filtered_data = df[(df[filter_column] >= min_value) & (df[filter_column] <= max_value)]

        st.write("Datos filtrados:")
        st.dataframe(filtered_data)

    # Descargar datos filtrados
    if st.checkbox("¿Deseas descargar los datos filtrados?"):
        csv = filtered_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar CSV",
            data=csv,
            file_name='datos_filtrados.csv',
            mime='text/csv'
        )
