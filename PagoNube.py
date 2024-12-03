import streamlit as st
import pandas as pd
import chardet

# Título de la aplicación
st.title("Procesador Automático de CSV - Agrupar por Número de Venta y Valor Neto")

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

        # Mostrar vista previa
        st.write("Vista previa del archivo:")
        st.dataframe(df.head())

        # Verificar nombres de columnas y mapearlos correctamente
        required_columns = ["Número de venta", "Valor neto"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"Faltan las siguientes columnas requeridas: {missing_columns}")
            st.stop()

        # Asegurarse de que "Número de venta" sea tratada como texto para evitar problemas con ceros iniciales
        df["Número de venta"] = df["Número de venta"].astype(str)

        # Convertir "Valor neto" a numérico
        df["Valor neto"] = pd.to_numeric(df["Valor neto"], errors="coerce")

        # Filtrar filas válidas
        valid_df = df.dropna(subset=["Número de venta", "Valor neto"])

        # Agrupar por "Número de venta" y sumar los valores netos
        grouped_data = valid_df.groupby("Número de venta")["Valor neto"].sum().reset_index()

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
