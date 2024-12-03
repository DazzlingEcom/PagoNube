import streamlit as st
import pandas as pd
import chardet

# Título de la aplicación
st.title("Procesador de CSV - Agrupación por Número de Venta")

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

        # Mostrar vista previa del archivo
        st.write("Vista previa del archivo original:")
        st.dataframe(df.head())

        # Verificar nombres de columnas
        required_columns = ["Número de venta", "Valor neto"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"Faltan las siguientes columnas requeridas: {missing_columns}")
            st.stop()

        # Limpieza de la columna "Número de venta"
        st.write("Procesando columna 'Número de venta'...")
        df["Número de venta"] = df["Número de venta"].astype(str).str.strip()

        # Filtrar filas con valores no válidos o nulos en "Número de venta"
        df = df[df["Número de venta"].notna()]
        df = df[df["Número de venta"].str.isnumeric()]

        # Mostrar vista previa después del filtrado
        st.write("Vista previa después de filtrar números de venta válidos:")
        st.dataframe(df.head())

        # Convertir la columna "Valor neto" a numérico
        st.write("Convirtiendo 'Valor neto' a valores numéricos...")
        df["Valor neto"] = pd.to_numeric(df["Valor neto"], errors="coerce")

        # Filtrar filas válidas
        valid_df = df.dropna(subset=["Valor neto"])

        # Agrupar por "Número de venta" y sumar los valores netos
        grouped_data = valid_df.groupby("Número de venta")["Valor neto"].sum().reset_index()

        # Renombrar columnas para claridad
        grouped_data.columns = ["Número de venta", "Suma Valor Neto"]

        # Mostrar los datos agrupados
        st.subheader("Datos agrupados por Número de Venta:")
        if grouped_data.empty:
            st.warning("No se encontraron datos válidos después del procesamiento.")
        else:
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
