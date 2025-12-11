import numpy as np 
import sympy 
from sympy import symbols, sympify, lambdify 
import sys 

# ========= FUNGSI PENGUJI ==============:
def IsLinier(F, num_test=5):
    """IsLinier menguji kelinieran dari transformasi fungsi F dengan 
    menggunakan 5 kali looping untuk pengujiannya dengan nilai matriks
    yang berbeda"""

    for i in range(num_test):
        try:
            # Uji Syarat Aditivitas:
            u = np.random.randn(2, 2)
            v = np.random.randn(2, 2)
            
            F_u_plus_v = F(u + v)
            F_u_plus_F_v = F(u) + F(v)

            if not np.allclose(F_u_plus_v, F_u_plus_F_v):
                print(f"Uji Aditivitas [GAGAL] pada: ")
                print(f"u = {u}\n")
                print(f"v = {v}\n")
                print(f"F(u + v) = {F_u_plus_v}\n")
                print(f"F(u) + F(v) = {F_u_plus_F_v}\n")
                return False

            # Uji Syarat Homogenitas:
            k = np.random.randn()
            F_k_u = F(k * u)
            k_F_u = k * F(u)

            if not np.allclose(F_k_u, k_F_u):
                print(f"Uji Homogenitas [GAGAL] pada: ")
                print(f"u = {u}")
                print(f"k = {k}")
                print(f"F(ku) = {F_k_u}\n")
                print(f"k * F(u) = {k_F_u}\n")
                return False
            
        except Exception as e:
            return False
    print("UJI ADITIVITAS & HOMOGENITAS [LOLOS]")
    print(f"Uji Aditivitas [LOLOS] pada: ")
    print(f"u = {u}")
    print(f"v = {v}\n")
    print(f"F(u + v) = {F_u_plus_v}")
    print(f"F(u) + F(v) = {F_u_plus_F_v}\n")
    print(f"Uji Homogenitas [LOLOS] pada: ")
    print(f"u = {u}")            
    print(f"k = {k}\n")            
    print(f"F(ku) = {F_k_u}")
    print(f"k * F(u) = {k_F_u}\n")
    print("Fungsi tranformasi merupakan fungsi linier\n")
    return True

# ============= FUNGSI PROSEDURAL =============:
def InputFromUser(fungsi1, fungsi2):
    """Fungsi InputFromUser akan menerima input fungsi dari user sebelum 
     dimasukkan ke dalam fungsi penguji. Dalam fungsi ini, tipe data dari 
     input akan diubah menjadi ke tipe data yang sesuai dengan menggunakan 
     library Sympy sebelum di eksekusi oleh fungsi penguji. """
    try:
        # 1. Tentukan simbol variabel yang diinginkan (x, y)
        x, y = symbols('x y')

        # 2. Ubah string input menjadi ekspresi matematika yang dapat
        #    dieksekusi oleh program:
        eksp_fungsi1 = sympify(fungsi1)
        eksp_fungsi2 = sympify(fungsi2)

        # 3. Fungsi Numerik:
        f1 = lambdify((x, y), eksp_fungsi1, 'numpy')
        f2 = lambdify((x, y), eksp_fungsi2, 'numpy')

        # Fungsi pembungkus output untuk dimasukkan ke fungsi penguji:
        def FungsiBungkus(v):
            # v adalah suatu matriks 2x1
            x = v[0]
            y = v[1]

            # Hitung output
            out1 = f1(x, y)
            out2 = f2(x, y)

            # Kembalikan output menjadi satu list
            return np.array([out1, out2], dtype=float)
        
        # Penamaan yang lebih rapi supaya outputnya lebih jelas
        FungsiBungkus.__name__ = f"F(x, y) = ({fungsi1}, {fungsi2})"

        return FungsiBungkus

    except Exception as e:
        print(f"\n[ERROR PARSING] Input Anda tidak valid: '{e.expr}'")
        print("Pastikan Anda hanya menggunakan x, y, angka, dan operator matematika")
        print("Contoh: '2*x + y', 'x**2', 'sin(x)', 'exp(y)'")
        return None
    except Exception as e:
        print(f"\n[ERROR] Terjadi kesalahan tak terduga: {e}")
        return None

# Fungsi prosedural untuk menjalankan program:
def main():
    """Fungsi prosedural untuk menjalankan program"""
    print("==============================================")
    print("   Selamat Datang di Penguji Transformasi    ")
    print("==============================================")
    print("Program ini akan menguji apakah T(x, y) adalah transformasi linier.")
    print("Anda perlu mendefinisikan T(x, y) = (Komponen 1, Komponen 2).\n")
    
    print("Gunakan 'x', 'y', angka, dan operasi seperti:")
    print(" + (tambah), - (kurang), * (kali), / (bagi), ** (pangkat)")
    
    while True:
        fungsi1 = input("Masukkan formula Komponen 1 (output x): ")
        fungsi2 = input("Masukkan formula Komponen 2 (output y): ")

        if not fungsi1 or not fungsi2:
            print("[ERROR] Kedua komponen tidak boleh kosong.")
            continue
        
        print("\n... Membuat fungsi dari input string ...\n")

        F_untuk_uji = InputFromUser(fungsi1, fungsi2)

        if F_untuk_uji:
            Hasil_uji = IsLinier(F_untuk_uji)

            if Hasil_uji:
                print(f"Hasil: F(x, y) = ({fungsi1}, {fungsi2}) linier")
            else:
                print(f"Hasil: F(x, y) = ({fungsi1}, {fungsi2}) tidak linier")
        
        ulang = input("Uji Transformasi lain? (Y/T): ").strip().lower()
        if ulang != 'y':
            print("Terima kasih...")
            break

# Tombol Start Program di semua kondisi:
if __name__ == "__main__":
    main()