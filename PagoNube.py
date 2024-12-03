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

        # Leer archivo con separador ";" y encoding detectado
        df = pd.read_csv(uploaded_file, sep=';', encoding=encoding)
        st.write("Archivo leído correctamente.")
        st.write(f"Encoding detectado: {encoding}")

        # Mostrar las primeras filas para diagnóstico
        st.write("Vista previa del archivo original:")
        st.dataframe(df.head(10))

        # Diagnóstico de columnas
        st.write("Columnas detectadas:")
        st.write(list(df.columns))

        # Si el archivo no tiene las columnas esperadas
        expected_columns = ["Cliente", "Medio de pago", "Descripción", "Número de venta",
                            "Fecha de creación", "Disponible para transferir", "Monto de la venta",
                            "Tasa Pago Nube", "Cantidad de cuotas", "Costo de Cuota Simple",
                            "Costo de cuotas Pago Nube", "Impuestos - IVA", "Impuestos - Ganancias", "Valor neto"]

        if len(df.columns) == 1:  # El archivo puede tener encabezados en una única celda
            df = pd.read_csv(uploaded_file, sep=';', encoding=encoding, header=None)
            df.columns = expected_columns

        elif set(expected_columns).issubset(df.columns):
            df = df[expected_columns]  # Reordenar columnas si hay desalineación
        else:
            st.warning("Intentando renombrar columnas.")
            df.columns = expected_columns

        # Confirmar las columnas clave
        required_columns = ["Número de venta", "Valor neto"]
        if not all(col in df.columns for col in required_columns):
            st.error(f"Faltan columnas requeridas: {', '.join(required_columns)}")
            st.stop()

        # Convertir columnas a formato numérico
        df["Número de venta"] = pd.to_numeric(df["Número de venta"], errors="coerce")
        df["Valor neto"] = pd.to_numeric(df["Valor neto"], errors="coerce")

        # Eliminar filas con datos no válidos en las columnas clave
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
