import pandas as pd

def muat_data_lokal(path_file):
    try:
        bingkai_data = pd.read_excel(path_file)
        return bingkai_data
    except Exception as galat:
        print("Gagal memuat berkas lokal:", galat)
        return None

def cari_linear(data, kolom, kata_kunci):
    hasil = data[data[kolom].astype(str).str.contains(kata_kunci, case=False, na=False)]
    return hasil

def cari_biner(data, kolom, kata_kunci):
    data_urut = data.sort_values(by=kolom, key=lambda x: x.astype(str).str.lower()).reset_index(drop=True)
    left = 0
    right = len(data_urut) - 1
    kata_kunci = kata_kunci.lower()
    daftar_hasil = []
    while left <= right:
        tengah = (left + right) // 2
        nilai_tengah = str(data_urut.loc[tengah, kolom]).lower()
        if kata_kunci in nilai_tengah:
            indeks_left, indeks_right = tengah, tengah
            while indeks_left >= 0 and kata_kunci in str(data_urut.loc[indeks_left, kolom]).lower():
                daftar_hasil.append(data_urut.loc[indeks_left])
                indeks_left -= 1
            while indeks_right < len(data_urut) and kata_kunci in str(data_urut.loc[indeks_right, kolom]).lower():
                if indeks_right != tengah:
                    daftar_hasil.append(data_urut.loc[indeks_right])
                indeks_right += 1
            break
        elif kata_kunci < nilai_tengah:
            right = tengah - 1
        else:
            left = tengah + 1
    return pd.DataFrame(daftar_hasil)

def main():
    lokasi_berkas = r"D:\DATA ARIL\KULIAH\Struktur_Data\Struktur_Data_Dataset_Kelas_A_B_C(MyFile).xlsx"
    data = muat_data_lokal(lokasi_berkas)
    if data is None:
        return
    print("Kolom Tersedia:", data.columns.tolist())
    while True:
        print("\n== Menu Pencarian Paper ==")
        print("1. Pencarian Linear")
        print("2. Pencarian Biner")
        print("3. Keluar")
        opsi = input("Pilih (1/2/3): ")
        if opsi == '3':
            print("Terima kasih! Keluar dari program.")
            break
        elif opsi not in ['1', '2']:
            print("Opsi tak valid.")
            continue
        pemetaan_kolom = {
            '1': 'Judul Paper',
            '2': 'Nama Penulis',
            '3': 'Tahun Terbit'
        }
        print("\nCari berdasarkan:")
        print("1. Judul")
        print("2. Penulis")
        print("3. Tahun")
        pilihan_kolom = input("Pilih (1/2/3): ")
        if pilihan_kolom not in pemetaan_kolom:
            print("Kolom tak valid.")
            continue
        kolom_cari = pemetaan_kolom[pilihan_kolom]
        frasa_cari = input(f"Masukkan Kata kunci '{kolom_cari}' : ")
        if opsi == '1':
            hasil_cari = cari_linear(data, kolom_cari, frasa_cari)
        else:
            hasil_cari = cari_biner(data, kolom_cari, frasa_cari)
        print("\n=== Hasil Pencarian ===")
        if not hasil_cari.empty:
            for indeks, baris in hasil_cari.iterrows():
                print("================================================================================================================="
                "==================================================================================")
                print(f"Judul   : {baris.get('Judul Paper', 'N/A')}")
                print(f"Penulis : {baris.get('Nama Penulis', 'N/A')}")
                print(f"Tahun   : {int(baris['Tahun Terbit']) if pd.notnull(baris['Tahun Terbit']) else 'N/A'}")
                print(f"Abstrak : {baris.get('Abstrak (langusung copas dari paper)', 'N/A')}")
                print(f"Simpulan: {baris.get('Kesimpulan (Langusung copas dari paper)', 'N/A')}")
                print(f"Tautan  : {baris.get('Link Paper', 'N/A')}")
                print("================================================================================================================="
                "==================================================================================")
        else:
            print("paper tak ditemukan.")

if __name__ == "__main__":
    main()
