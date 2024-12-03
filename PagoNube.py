import streamlit as st
import pandas as pd
import chardet

# Título de la aplicación
st.title("Procesador de CSV - Diagnóstico y Agrupación por Número de Venta")

# Subida del archivo CSV
uploaded_file = st.file_uploader("Sube un archivo CSV", type="csv")

if uploaded_file is not None:
    try:
        # Detectar encoding del archivo
        raw_data = uploaded_file.read()
        detected_encoding = chardet.detect(raw_data)
        encoding = detected_encoding['encoding']
        uploaded_file.seek(0)  # Resetear puntero del archivo

        # Leer el archivo CSV con encoding detectado
        st.write(f"Encoding detectado: {encoding}")
        df = pd.read_csv(uploaded_file, sep=';', encoding=encoding, error_bad_lines=False)
        st.write("Archivo leído correctamente.")
        st.write(f"Total de filas originales: {df.shape[0]}")

        # Mostrar vista previa
        st.write("Vista previa del archivo original:")
        st.dataframe(df.head(10))

        # Diagnóstico inicial de columnas
        st.write("Columnas detectadas:")
        st.write(list(df.columns))

        # Intentar dividir las columnas si parecen comprimidas
        if len(df.columns) == 1:
            st.warning("Las columnas parecen comprimidas. Intentando dividirlas...")
            df = pd.read_csv(uploaded_file, sep=';', encoding=encoding, header=None)
            st.write("Nuevas columnas detectadas después de dividir:")
            st.write(list(df.columns))

        # Comprobar encabezados esperados y asignar si es necesario
        expected_columns = [
            "Cliente", "Medio de pago", "Descripción", "Número de venta", 
            "Fecha de creación", "Disponible para transferir", "Monto de la venta", 
            "Tasa Pago Nube", "Cantidad de cuotas", "Costo de Cuota Simple", 
            "Costo de cuotas Pago Nube", "Impuestos - IVA", "Impuestos - Ganancias", "Valor neto"
        ]
        if len(df.columns) == len(expected_columns):
            df.columns = expected_columns
        else:
            st.error("El archivo no tiene el formato esperado o las columnas no coinciden.")
            st.stop()

        # Validar columnas necesarias
        required_columns = ["Número de venta", "Valor neto"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"Faltan las columnas requeridas: {', '.join(missing_columns)}")
            st.stop()

        # Convertir columnas clave a numérico
        df["Número de venta"] = pd.to_numeric(df["Número de venta"], errors="coerce")
        df["Valor neto"] = pd.to_numeric(df["Valor neto"], errors="coerce")

        # Filtrar filas con datos válidos
        valid_sales = df.dropna(subset=["Número de venta", "Valor neto"])

        # Diagnóstico de filas válidas
        st.write(f"Total de filas válidas después del filtrado: {valid_sales.shape[0]}")

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
