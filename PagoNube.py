import streamlit as st
import pandas as pd
import chardet

# Título de la aplicación
st.title("Procesador de CSV - Agrupación por Número de Venta y Valor Neto")

# Subida del archivo CSV
uploaded_file = st.file_uploader("Sube un archivo CSV", type="csv")

if uploaded_file is not None:
    try:
        # Detectar encoding del archivo
        raw_data = uploaded_file.read()
        detected_encoding = chardet.detect(raw_data)
        encoding = detected_encoding['encoding']
        uploaded_file.seek(0)  # Resetear puntero del archivo

        # Leer archivo con separador ";"
        df = pd.read_csv(uploaded_file, sep=';', encoding=encoding)
        st.write("Archivo leído correctamente.")
        st.write(f"Encoding detectado: {encoding}")

        # Mostrar columnas detectadas y vista previa del archivo
        st.write("Columnas detectadas:")
        st.dataframe(df.head(10))  # Verifica visualmente los encabezados y valores iniciales

        # Renombrar columnas manualmente si no coinciden con las esperadas
        if "Número de venta" not in df.columns and df.shape[1] > 3:
            st.warning("Renombrando columnas automáticamente.")
            df.columns = ["Cliente", "Medio de pago", "Descripción", "Número de venta",
                          "Fecha de creación", "Disponible para transferir", "Monto de la venta",
                          "Tasa Pago Nube", "Cantidad de cuotas", "Costo de Cuota Simple",
                          "Costo de cuotas Pago Nube", "Impuestos - IVA", "Impuestos - Ganancias", "Valor neto"]

        # Validar si las columnas clave están presentes
        required_columns = ["Número de venta", "Valor neto"]
        st.write("Columnas después del renombramiento:", list(df.columns))
        if not all(col in df.columns for col in required_columns):
            st.error(f"Faltan las siguientes columnas requeridas: {', '.join(required_columns)}")
            st.stop()

        # Convertir "Número de venta" y "Valor neto" a numérico
        df["Número de venta"] = pd.to_numeric(df["Número de venta"], errors="coerce")
        df["Valor neto"] = pd.to_numeric(df["Valor neto"], errors="coerce")

        # Eliminar filas sin datos válidos en las columnas clave
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
