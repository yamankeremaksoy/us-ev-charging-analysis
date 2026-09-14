import os
import pandas as pd
import numpy as np

def find_excel_files(base_path):
    excel_files = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if (file.endswith('.xlsx') or file.endswith('.xls')) and not file.startswith('~$'):
                excel_files.append(os.path.join(root, file))
    return excel_files

def load_and_clean_data(base_path):
    files = find_excel_files(base_path)
    print(f"-> Bulunan Excel dosya sayisi: {len(files)}")
    if not files: 
        return None
    all_dfs = []
    for file_path in files:
        try:
            df = pd.read_excel(file_path)
            df.columns = df.columns.astype(str).str.strip().str.lower()
            all_dfs.append(df)
        except Exception:
            pass
    return pd.concat(all_dfs, ignore_index=True) if all_dfs else None

def run_analysis():
    # Esnek Veri Yolu (Hem yerel bilgisayarda hem GitHub reposunda çalışır)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(script_dir, "national_state-2030ncn-results")
    if not os.path.exists(base_path):
        base_path = r"C:\Users\Yaman\Desktop\national_state-2030ncn-results"

    print("1/4 Veriler birlestiriliyor...")
    combined_df = load_and_clean_data(base_path)
    if combined_df is None: 
        print("HATA: Excel verisi okunamadi.")
        return

    state_col = None
    for col in combined_df.columns:
        if any(k in str(col) for k in ['state', 'geography', 'region', 'area']):
            state_col = col
            break
    if not state_col:
        text_cols = combined_df.select_dtypes(include=['object', 'string']).columns
        state_col = text_cols[0] if len(text_cols) > 0 else combined_df.columns[0]

    numeric_cols = combined_df.select_dtypes(include=[np.number]).columns.tolist()
    if state_col in numeric_cols:
        numeric_cols.remove(state_col)

    df_clean = combined_df.dropna(subset=[state_col]).copy()

    if len(numeric_cols) >= 2:
        val_cols = numeric_cols[:2]
        df_grouped = df_clean.groupby(state_col, as_index=False)[val_cols].sum()
        df_grouped = df_grouped.iloc[:, :3]
        df_grouped.columns = ['state', 'ev_count_2025', 'ev_count_2030']
    else:
        val_col = numeric_cols[0]
        df_grouped = df_clean.groupby(state_col, as_index=False)[val_col].sum()
        df_grouped = df_grouped.iloc[:, :2]
        df_grouped.columns = ['state', 'ev_count_2030']
        df_grouped['ev_count_2025'] = (df_grouped['ev_count_2030'] * 0.65).astype(int)

    print("2/4 Metrikler ve Dagitim Algoritmasi hesaplaniyor...")
    df_grouped['ev_growth_absolute'] = df_grouped['ev_count_2030'] - df_grouped['ev_count_2025']
    df_grouped['ev_growth_pct'] = ((df_grouped['ev_growth_absolute'] / df_grouped['ev_count_2025'].replace(0, 1)) * 100).round(2)
    df_grouped['peak_grid_load_kw'] = (df_grouped['ev_count_2030'] * 1.2 * 0.15).round(2)

    total_growth = df_grouped['ev_growth_absolute'].sum()
    if total_growth > 0:
        df_grouped['allocated_chargers'] = ((df_grouped['ev_growth_absolute'] / total_growth) * 1000).astype(int)
    else:
        df_grouped['allocated_chargers'] = 1000 // len(df_grouped)

    output_excel = os.path.join(script_dir, "EV_Charging_Optimal_Allocation.xlsx")
    df_grouped.to_excel(output_excel, index=False)
    print(f"\n3/4 Tum sonuclar Excel dosyasina kaydedildi:\n -> {output_excel}")

    print("\n" + "=" * 65)
    print("ANALIZ BASARILI! OZET TABLO (ILK 10 EYALET):")
    print("=" * 65)
    print(df_grouped[['state', 'ev_count_2025', 'ev_count_2030', 'ev_growth_pct', 'allocated_chargers']].head(10).to_string(index=False))
    print("=" * 65)

if __name__ == '__main__':
    run_analysis()