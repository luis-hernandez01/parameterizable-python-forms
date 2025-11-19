import pandas as pd
import numpy as np
import math as mh


# ------------------------- utilities -------------------------

def merge(list1, list2):
    """Crear lista de tuplas (start,end) del mismo tamaño que la intersección mínima."""
    return list({list1[i]: list2[i] for i in range(min(len(list1), len(list2)))}.items())


def repartkm(data_trimestre, data_part, trimestre):
    """Reparte los tramos PR_INICIAL-PR_FINAL sobre las filas de data_part.

    data_trimestre: DataFrame con columnas PR_FINAL y PR_INICIAL (y opcionalmente otras)
    data_part: DataFrame con columnas init_km, end_km y columna para el trimestre
    trimester: nombre de columna donde se acumula
    """

    # Si está vacío no hacemos nada
    if data_trimestre is None or data_trimestre.shape[0] == 0:
        return data_part

    data = data_trimestre[["PR_FINAL", "PR_INICIAL"]]

    for value_end, value_init in data.itertuples(index=False):

        # Protección
        try:
            value_end = float(value_end)
            value_init = float(value_init)
        except Exception:
            continue

        if value_end == value_init:
            continue

        piso = mh.floor(value_init)
        arriba = mh.ceil(value_end)

        rangos_init = list(range(piso, arriba))
        rangos_endt = list(range(piso + 1, arriba + 1))
        ran = merge(rangos_init, rangos_endt)

        # Caso 1: contenido en único intervalo
        if len(ran) == 1:
            per = value_end - value_init
            end_val = ran[0][1]
            idx = data_part[data_part['end_km'] == end_val].index
            if idx.empty:
                # no existe ese end_km en data_part: skip
                continue
            data_part.loc[idx, trimestre] = data_part.loc[idx, trimestre] + per

        # Caso 2: abarca varios intervalos
        else:
            # Primer intervalo
            first_range = ran[0]
            per_first = (first_range[1] - value_init)
            idx = data_part[data_part['end_km'] == first_range[1]].index
            if not idx.empty:
                data_part.loc[idx, trimestre] = data_part.loc[idx, trimestre] + per_first

            # Último intervalo
            last_range = ran[-1]
            per_last = 1 - (last_range[1] - value_end)
            idx = data_part[data_part['end_km'] == last_range[1]].index
            if not idx.empty:
                data_part.loc[idx, trimestre] = data_part.loc[idx, trimestre] + per_last

            # Intermedios
            if len(ran) > 2:
                for _, end in ran[1:-1]:
                    idx = data_part[data_part['end_km'] == end].index
                    if idx.empty:
                        continue
                    data_part.loc[idx, trimestre] = data_part.loc[idx, trimestre] + 1

    return data_part


def process_all(data, emisiones):
    """Pipeline completo: toma df data (emisiones4) y emisiones (emisiones_trimestre)
    Devuelve (result, short_result) DataFrames.
    """

    # Trabajar sobre copias
    df = data.copy()
    emis = emisiones.copy()

    # Eliminar ID si existe
    if 'ID' in df.columns:
        df = df.drop(columns=['ID'])
    if 'ID' in emis.columns:
        emis = emis.drop(columns=['ID'])

    # Asegurar tipos
    df['PR_INICIAL'] = pd.to_numeric(df['PR_INICIAL'], errors='coerce')
    df['PR_FINAL'] = pd.to_numeric(df['PR_FINAL'], errors='coerce')

    # Crear pr_diff
    df['pr_diff'] = df['PR_FINAL'] - df['PR_INICIAL']

    trimestres = df['Trimestral'].unique()
    codigos = df['codigo_via'].unique()

    # values_trim: suma de pr_diff por trim_codigo
    values_trim = {}
    for codigo in codigos:
        for trim in trimestres:
            s = df[(df['Trimestral'] == trim) & (df['codigo_via'] == codigo)]['pr_diff'].sum()
            key = f"{trim}_{codigo}"
            values_trim[key] = float(np.round(s, 6))

    # df_por: proporción de km por codigo dentro de cada trimestre
    df_por = pd.DataFrame()
    for trim in trimestres:
        df_trim = df[df['Trimestral'] == trim]
        total = df_trim['pr_diff'].sum()
        cods = df_trim['codigo_via'].unique()
        filas = []
        for c in cods:
            v = df_trim[df_trim['codigo_via'] == c]['pr_diff'].sum()
            prop = (v / total) if total != 0 else 0
            filas.append({'Trimestral': trim, 'codigo': str(c), 'valores': prop})
        if filas:
            df_por = pd.concat([df_por, pd.DataFrame(filas)], ignore_index=True)

    # Construcción de rangos por codigo
    dframes = []

    for codigo in codigos:
        # max PR por vía (protección si no existen valores)
        subset = df[df['codigo_via'] == codigo]
        if subset.shape[0] == 0:
            continue

        max_pr = subset['PR_FINAL'].max()
        if pd.isna(max_pr):
            continue

        max_km_via = int(mh.ceil(max_pr)) + 1
        if max_km_via <= 1:
            continue

        rangofin = range(1, max_km_via)
        rangoini = range(0, len(rangofin))

        result = pd.DataFrame({'init_km': rangoini, 'end_km': rangofin})
        result['codigo_via'] = str(codigo)

        # agregar columnas por trimestre y repartir
        for trim in trimestres:
            result[trim] = 0.0
            data_trim = df[(df['Trimestral'] == trim) & (df['codigo_via'] == codigo)].copy()
            if data_trim.shape[0] == 0:
                continue
            data_trim.sort_values(by='PR_FINAL', inplace=True)
            result = repartkm(data_trim, result, trim)

        dframes.append(result)

    if len(dframes) == 0:
        # retornar dataframes vacíos si no hay datos
        empty_result = pd.DataFrame(columns=['init_km', 'end_km', 'codigo_via', 'emisiones_per_range'])
        return empty_result, empty_result

    result = pd.concat(dframes, ignore_index=True)

    # Procesar emisiones
    emis['Trimestral'] = emis['Trimestral'].astype(str)
    df_por['Trimestral'] = df_por['Trimestral'].astype(str)
    df_por['codigo'] = df_por['codigo'].astype(str)

    df_combinado = pd.merge(df_por, emis, on='Trimestral', how='left')
    if 'Emisiones' not in df_combinado.columns:
        df_combinado['Emisiones'] = 0

    df_combinado['Resultado'] = df_combinado['valores'] * df_combinado['Emisiones']

    # Calcular emisiones por km
    emisiones_km = {}
    for key, pdiff in values_trim.items():
        t, c = key.split("_")
        if pdiff != 0:
            vals = df_combinado[(df_combinado['Trimestral'] == t) & (df_combinado['codigo'] == c)]['Resultado'].values
            if vals.size > 0:
                emisiones_km[key] = float(vals[0]) / float(pdiff)
            else:
                emisiones_km[key] = 0.0
        else:
            emisiones_km[key] = 0.0

    # Añadir columnas de emisiones por cada combinación
    for key, value in emisiones_km.items():
        t, c = key.split("_")
        col = f"{key}_emisiones"
        # aplicar por fila: si codigo_via coincide, multiplicar la proporción de ese trimestre
        result[col] = result.apply(lambda row: row[t] * value if str(row['codigo_via']) == c else 0.0, axis=1)

    # Sumar todas las columnas de emisiones
    cols_em = [c for c in result.columns if c.endswith('_emisiones')]
    if len(cols_em) == 0:
        result['emisiones_per_range'] = 0.0
    else:
        result['emisiones_per_range'] = result[cols_em].sum(axis=1)

    short = result[['init_km', 'end_km', 'codigo_via', 'emisiones_per_range']].copy()

    return result, short