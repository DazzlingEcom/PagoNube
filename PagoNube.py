import streamlit as st
import pandas as pd
import chardet

# Título de la aplicación
st.title("Procesador de CSV - Agrupación por Número de Venta y Valor Neto")

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
        df = pd.read_csv(uploaded_file, sep='\t', encoding=encoding)
        st.write("Archivo leído correctamente.")
        st.write(f"Encoding detectado: {encoding}")

        # Mostrar vista previa del archivo original
        st.write("Vista previa del archivo original:")
        st.dataframe(df.head())

        # Verificar columnas
        required_columns = ["Cliente", "Número de venta", "Valor neto"]
        st.write("Columnas detectadas:", list(df.columns))
        if not all(col in df.columns for col in required_columns):
            st.error(f"Faltan las siguientes columnas requeridas: {', '.join(required_columns)}")
            st.stop()

        # Limpiar y convertir columnas clave
        df["Número de venta"] = pd.to_numeric(df["Número de venta"], errors="coerce")
        df["Valor neto"] = pd.to_numeric(df["Valor neto"], errors="coerce")

        # Filtrar filas válidas
        valid_sales = df.dropna(subset=["Número de venta", "Valor neto"])

        # Agrupar por "Número de venta" y sumar "Valor neto"
        grouped_data = valid_sales.groupby("Número de venta")["Valor neto"].sum().reset_index()
        grouped_data.columns = ["Número de venta", "Suma Valor Neto"]

        # Mostrar resultados agrupados
        st.subheader("Resultados agrupados por Número de Venta:")
        if grouped_data.empty:
            st.warning("No se encontraron datos válidos después del procesamiento.")
        else:
            st.dataframe(grouped_data)

            # Descargar datos agrupados
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
