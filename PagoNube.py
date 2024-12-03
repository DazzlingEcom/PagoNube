import streamlit as st
import pandas as pd
import chardet

# Título de la aplicación
st.title("Procesador Automático de CSV - Filtrar y Ordenar por Valor Neto")

# Subida del archivo CSV
uploaded_file = st.file_uploader("Sube un archivo CSV", type="csv")

if uploaded_file is not None:
    try:
        # Detectar el encoding del archivo
        raw_data = uploaded_file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        st.write(f"Encoding detectado: {encoding}")

        # Volver a cargar el archivo con el encoding detectado
        uploaded_file.seek(0)  # Restablecer el puntero del archivo después de leer
        df = pd.read_csv(uploaded_file, encoding=encoding, sep=';')

        # Mostrar columnas detectadas
        st.write("Columnas detectadas antes de renombrar:", list(df.columns))

        # Establecer encabezados correctos manualmente
        df.columns = [
            "cliente", "medio_pago", "descripcion", "numero_venta",
            "fecha_creacion", "disponible_transferir", "monto_venta",
            "tasa_pago_nube", "cantidad_cuotas", "costo_cuota_simple",
            "costo_cuotas_pago_nube", "impuestos_iva", "impuestos_ganancias",
            "valor_neto"
        ]

        # Mostrar vista previa del archivo con encabezados correctos
        st.write("Vista previa del archivo después de renombrar:")
        st.dataframe(df.head())

        # Filtrar filas donde "numero_venta" no sea nulo ni vacío
        df = df[df["numero_venta"].notna() & df["numero_venta"].str.strip().astype(bool)]

        # Convertir "valor_neto" a numérico
        df["valor_neto"] = pd.to_numeric(df["valor_neto"], errors="coerce")

        # Convertir "fecha_creacion" a datetime
        df["fecha"] = pd.to_datetime(df["fecha_creacion"], errors="coerce", format='%d-%m-%Y %H:%M:%S')

        # Agrupar por "fecha" y "numero_venta", y sumar "valor_neto"
        grouped_df = df.groupby(["fecha", "numero_venta"])["valor_neto"].sum().reset_index()
        grouped_df.columns = ["fecha", "numero_venta", "suma_valor_neto"]

        # Mostrar los datos agrupados
        st.subheader("Datos agrupados por fecha y número de venta:")
        st.dataframe(grouped_df)

        # Exportar el CSV con la información agrupada
        csv = grouped_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar CSV Agrupado",
            data=csv,
            file_name='datos_agrupados.csv',
            mime='text/csv'
        )
    except Exception as e:
        st.error(f"Error procesando el archivo: {e}")
else:
    st.info("Por favor, sube un archivo CSV para comenzar.")
