import os
import sys
from model.ngram_LM import ngram_LM
from model.load_index import load_index

def menu():
    print("=== PROGRAM ANALISIS N-GRAM ===")
    print("1. Prediksi kata berikutnya (menggunakan N-gram STEM)")
    print("2. Print hasil prediksi")
    print("3. Keluar")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    sys.stdout.write('\033c')
    sys.stdout.flush()

def main_program():
    _, total_unigram, total_bigram, total_trigram, total_vocabulary = load_index()

    while True:
        menu()
        try:
            pilihan = int(input("Masukkan nomor menu (1-3): "))
        except:
            clear()
            print("Input tidak valid. Silakan masukkan angka 1-3.\n")
            continue

        if pilihan == 1:
            clear()
            print(">> Prediksi kata berikutnya (input 1-2 kata) <<")
            query = input("Masukkan kueri: ").strip()
            hasil = ngram_LM(query, total_unigram, total_bigram, total_trigram, int(total_vocabulary), top_k=5)
            print(f"\nTop-5 prediksi next-word untuk '{query}':")
            for idx, (kata, prob) in enumerate(hasil, start=1):
                print(f"  {idx}. {kata}  (prob: {prob:.4f})")
            print()

        elif pilihan == 2:
            clear()
            print(">> Prediksi kata berikutnya (input 1-2 kata) <<")
            query = input("Masukkan kueri: ").strip()
            hasil = ngram_LM(query, total_unigram, total_bigram, total_trigram, int(total_vocabulary), top_k=5)
            print(f"\nhasil dari N-Gram LM dari '{query}':")
            print(type(hasil))
            print(hasil)
            prediction = {'predictions': {}}
            for idx, (kata, prob) in enumerate(hasil):
                prediction['predictions'].update({f"{kata}":prob})
            print(prediction)

        elif pilihan == 3:
            clear()
            print("Keluar. Terima kasih!")
            break

        else:
            clear()
            print("Menu tidak tersedia. Masukkan angka 1-6 saja.\n")

if __name__ == "__main__":
    main_program()