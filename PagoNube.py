import streamlit as st
import pandas as pd
import chardet

# Título de la aplicación
st.title("Procesador de CSV - Agrupación y Filtrado")

# Subida del archivo CSV
uploaded_file = st.file_uploader("Sube un archivo CSV", type="csv")

if uploaded_file is not None:
    try:
        # Detectar el encoding del archivo
        raw_data = uploaded_file.read()
        detected_encoding = chardet.detect(raw_data)
        encoding = detected_encoding['encoding']
        uploaded_file.seek(0)  # Resetear el puntero del archivo

        # Leer el archivo CSV con encoding detectado
        st.write(f"Encoding detectado: {encoding}")
        df = pd.read_csv(uploaded_file, sep=';', encoding=encoding, skip_blank_lines=True)
        st.write("Archivo leído correctamente.")
        st.write(f"Total de filas originales: {df.shape[0]}")

        # Manejo de columnas compactadas (todo en una sola columna)
        if len(df.columns) == 1:
            st.warning("Las columnas parecen comprimidas. Intentando dividirlas...")
            df = pd.read_csv(uploaded_file, sep=';', encoding=encoding, header=0)
            st.write("Nuevas columnas detectadas después de dividir:")
            st.write(df.columns.tolist())

        # Validar columnas y asignar nombres
        if "Cliente" in df.columns[0]:
            df = df.rename(columns=lambda x: x.strip())
            expected_columns = [
                "Cliente", "Medio de pago", "Descripción", "Número de venta",
                "Fecha de creación", "Disponible para transferir", "Monto de la venta",
                "Tasa Pago Nube", "Cantidad de cuotas", "Costo de Cuota Simple",
                "Costo de cuotas Pago Nube", "Impuestos - IVA", "Impuestos - Ganancias", "Valor neto"
            ]
            df.columns = expected_columns[:len(df.columns)]

        # Validar columnas requeridas
        required_columns = ["Número de venta", "Valor neto", "Fecha de creación"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"Faltan las siguientes columnas requeridas: {', '.join(missing_columns)}")
            st.stop()

        # Convertir las columnas clave a los tipos adecuados
        df["Número de venta"] = pd.to_numeric(df["Número de venta"], errors="coerce")
        df["Valor neto"] = pd.to_numeric(df["Valor neto"], errors="coerce")
        df["Fecha de creación"] = pd.to_datetime(df["Fecha de creación"], errors="coerce", format='%d-%m-%Y %H:%M:%S')

        # Filtrar filas válidas
        valid_df = df.dropna(subset=["Número de venta", "Valor neto", "Fecha de creación"])

        # Agrupar por fecha y sumar valor neto
        grouped_data = valid_df.groupby(valid_df["Fecha de creación"].dt.date)["Valor neto"].sum().reset_index()
        grouped_data.columns = ["Fecha", "Suma Valor Neto"]

        # Mostrar resultados agrupados por fecha
        st.subheader("Resultados agrupados por Fecha:")
        if grouped_data.empty:
            st.warning("No se encontraron datos válidos después del procesamiento.")
        else:
            st.dataframe(grouped_data)

            # Descargar datos agrupados
            grouped_csv = grouped_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Descargar CSV Agrupado por Fecha",
                data=grouped_csv,
                file_name='suma_por_fecha.csv',
                mime='text/csv'
            )

        # Crear archivo filtrado con "Número de venta", "Valor Neto" y "Fecha"
        filtered_data = valid_df[["Número de venta", "Valor neto", "Fecha de creación"]].copy()
        filtered_data.columns = ["Número de venta", "Valor Neto", "Fecha"]

        # Mostrar datos filtrados
        st.subheader("Datos filtrados con Número de Venta, Valor Neto y Fecha:")
        st.dataframe(filtered_data)

        # Descargar datos filtrados
        filtered_csv = filtered_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar CSV Filtrado",
            data=filtered_csv,
            file_name='datos_filtrados.csv',
            mime='text/csv'
        )

    except Exception as e:
        st.error(f"Error procesando el archivo: {e}")
else:
    st.info("Por favor, sube un archivo CSV para comenzar.")
