import streamlit as st
import pandas as pd

# Título de la aplicación
st.title("Procesador Automático de CSV - Filtrar y Ordenar por Valor Neto")

# Subida del archivo CSV
uploaded_file = st.file_uploader("Sube un archivo CSV", type="csv")

if uploaded_file is not None:
    # Leer el archivo CSV sin encabezados
    df = pd.read_csv(uploaded_file, header=None, sep=';')

    # Agregar un encabezado provisional para identificar columnas
    df.columns = [f"col_{i}" for i in range(df.shape[1])]

    # Excluir filas cuya columna 0 esté vacía
    df = df[df['col_0'].notna() & df['col_0'].str.strip().astype(bool)]

    # Extraer el último número (valor neto) de cada fila
    df["valor_neto"] = pd.to_numeric(df.iloc[:, -1], errors="coerce")

    # Convertir la columna de fecha a formato datetime (col_5 en este caso)
    if 'col_5' in df.columns:
        df["fecha"] = pd.to_datetime(df["col_5"], errors="coerce", format='%d-%m-%Y %H:%M:%S')

    # Mostrar vista previa del archivo original
    st.subheader("Vista previa del archivo procesado:")
    st.dataframe(df)

    # Agrupar por fecha y sumar los valores de "valor_neto"
    grouped_df = df.groupby(df["fecha"].dt.date)["valor_neto"].sum().reset_index()
    grouped_df.columns = ["fecha", "suma_valor_neto"]

    # Ordenar por la suma de valores netos
    sorted_grouped_df = grouped_df.sort_values(by="suma_valor_neto", ascending=False)

    # Mostrar datos ordenados
    st.subheader("Datos agrupados por fecha y ordenados por suma de 'valor_neto':")
    st.dataframe(sorted_grouped_df)

    # Descargar datos ordenados
    csv_sorted = sorted_grouped_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Descargar CSV Ordenado",
        data=csv_sorted,
        file_name='datos_ordenados.csv',
        mime='text/csv'
    )

    # Crear un DataFrame filtrado con "Número de venta" y "valor_neto"
    filtered_df = df[["col_0", "valor_neto"]].rename(columns={"col_0": "numero_venta", "valor_neto": "valor_neto"})
    filtered_df = filtered_df.dropna(subset=["valor_neto"])

    # Mostrar los datos filtrados
    st.subheader("Valores Netos con sus respectivos Números de Ventas:")
    st.dataframe(filtered_df)

    # Descargar datos filtrados
    csv_filtered = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Descargar CSV Filtrado",
        data=csv_filtered,
        file_name='datos_filtrados.csv',
        mime='text/csv'
    )
else:
    st.info("Por favor, sube un archivo CSV para comenzar.")
