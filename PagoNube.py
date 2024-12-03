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
        df = pd.read_csv(uploaded_file, sep=';', encoding=encoding, header=None)
        st.write("Archivo leído correctamente.")
        st.write(f"Encoding detectado: {encoding}")

        # Mostrar vista previa
        st.write("Vista previa del archivo:")
        st.dataframe(df.head())

        # Asignar nombres provisionales a las columnas
        df.columns = [f"col_{i}" for i in range(df.shape[1])]

        # Validar que al menos haya suficientes columnas para identificar la cuarta columna (Número de venta)
        if df.shape[1] < 4:
            st.error("El archivo no contiene suficientes columnas para procesar.")
            st.stop()

        # Seleccionar la cuarta columna como "Número de venta"
        df["Número de venta"] = df["col_3"].astype(str).fillna("")
        if df["Número de venta"].str.isnumeric().all():
            df["Número de venta"] = df["Número de venta"].astype(int).astype(str)

        # Validar que al menos haya suficientes columnas para identificar "Valor neto"
        if df.shape[1] < 13:  # Por ejemplo, si "Valor neto" está en la última columna
            st.error("El archivo no contiene suficientes columnas para identificar 'Valor neto'.")
            st.stop()

        # Seleccionar la columna "Valor neto" (última columna)
        df["Valor neto"] = pd.to_numeric(df.iloc[:, -1], errors="coerce")
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
