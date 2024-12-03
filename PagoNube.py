import streamlit as st
import pandas as pd
import chardet

# Título de la aplicación
st.title("Procesador Automático de CSV - Filtrar y Exportar por Valor Neto y Número de Venta")

# Subida del archivo CSV
uploaded_file = st.file_uploader("Sube un archivo CSV", type="csv")

if uploaded_file is not None:
    try:
        # Detectar encoding
        raw_data = uploaded_file.read()
        detected_encoding = chardet.detect(raw_data)
        encoding = detected_encoding['encoding']
        uploaded_file.seek(0)  # Resetear el puntero del archivo

        # Leer archivo CSV
        df = pd.read_csv(uploaded_file, sep=';', encoding=encoding)
        st.write("Archivo leído correctamente.")
        st.write(f"Encoding detectado: {encoding}")

        # Vista previa de las columnas detectadas
        st.write("Columnas detectadas:", list(df.columns))

        # Validar columnas necesarias
        required_columns = ["Número de venta", "Valor neto"]
        if not all(col in df.columns for col in required_columns):
            st.error(f"Faltan las siguientes columnas requeridas: {required_columns}")
            st.stop()

        # Asegurar que las columnas relevantes son de tipo string o numérico
        df["Número de venta"] = df["Número de venta"].astype(str).fillna("")
        df["Valor neto"] = pd.to_numeric(df["Valor neto"], errors="coerce")

        # Eliminar filas con valores no válidos en "Valor neto"
        df = df.dropna(subset=["Valor neto"])

        # Agrupar por "Número de venta" y sumar los valores netos
        grouped_data = df.groupby("Número de venta")["Valor neto"].sum().reset_index()

        # Mostrar los datos agrupados
        st.subheader("Datos agrupados por Número de venta:")
        st.dataframe(grouped_data)

        # Exportar los datos agrupados a CSV
        csv = grouped_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar CSV Agrupado",
            data=csv,
            file_name='ventas_agrupadas.csv',
            mime='text/csv'
        )

    except Exception as e:
        st.error(f"Error procesando el archivo: {e}")
else:
    st.info("Por favor, sube un archivo CSV para comenzar.")
