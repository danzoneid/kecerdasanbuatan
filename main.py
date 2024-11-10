import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Definisi Fungsi Keanggotaan
def triangular(x, a, b, c):
    """Fungsi keanggotaan segitiga."""
    if a == b and b == c:
        return 1.0 if x == a else 0.0
    if x <= a or x >= c:
        return 0.0
    elif a < x < b:
        return (x - a) / (b - a)
    elif b <= x < c:
        return (c - x) / (c - b)
    else:
        return 0.0

# Membership Functions untuk setiap variabel
def get_membership_degrees_request_count(x):
    return {
        "Rendah": triangular(x, 0, 0, 400),
        "Sedang": triangular(x, 300, 500, 700),
        "Tinggi": triangular(x, 600, 1000, 1000)
    }

def get_membership_degrees_system_security_level(x):
    return {
        "Rendah": triangular(x, 0, 0, 4),
        "Sedang": triangular(x, 3, 5, 7),
        "Tinggi": triangular(x, 6, 10, 10)
    }

def get_membership_degrees_anomalous_data_volume(x):
    return {
        "Rendah": triangular(x, 0, 0, 200),
        "Sedang": triangular(x, 150, 250, 350),
        "Tinggi": triangular(x, 300, 500, 500)
    }

def get_membership_degrees_cyber_attack_risk_level(x):
    return {
        "Rendah": triangular(x, 0, 0, 25),
        "Sedang": triangular(x, 20, 50, 80),
        "Tinggi": triangular(x, 75, 100, 100)
    }

# Definisi Aturan Fuzzy
rules = [
    {"antecedent": ("Rendah", "Rendah", "Rendah"), "consequent": "Sedang"},
    {"antecedent": ("Rendah", "Rendah", "Sedang"), "consequent": "Tinggi"},
    {"antecedent": ("Rendah", "Rendah", "Tinggi"), "consequent": "Tinggi"},
    {"antecedent": ("Rendah", "Sedang", "Rendah"), "consequent": "Sedang"},
    {"antecedent": ("Rendah", "Sedang", "Sedang"), "consequent": "Sedang"},
    {"antecedent": ("Rendah", "Sedang", "Tinggi"), "consequent": "Tinggi"},
    {"antecedent": ("Rendah", "Tinggi", "Rendah"), "consequent": "Sedang"},
    {"antecedent": ("Rendah", "Tinggi", "Sedang"), "consequent": "Sedang"},
    {"antecedent": ("Rendah", "Tinggi", "Tinggi"), "consequent": "Tinggi"},
    {"antecedent": ("Sedang", "Rendah", "Rendah"), "consequent": "Sedang"},
    {"antecedent": ("Sedang", "Rendah", "Sedang"), "consequent": "Tinggi"},
    {"antecedent": ("Sedang", "Rendah", "Tinggi"), "consequent": "Tinggi"},
    {"antecedent": ("Sedang", "Sedang", "Rendah"), "consequent": "Sedang"},
    {"antecedent": ("Sedang", "Sedang", "Sedang"), "consequent": "Tinggi"},
    {"antecedent": ("Sedang", "Sedang", "Tinggi"), "consequent": "Tinggi"},
    {"antecedent": ("Sedang", "Tinggi", "Rendah"), "consequent": "Sedang"},
    {"antecedent": ("Sedang", "Tinggi", "Sedang"), "consequent": "Tinggi"},
    {"antecedent": ("Sedang", "Tinggi", "Tinggi"), "consequent": "Tinggi"},
    {"antecedent": ("Tinggi", "Rendah", "Rendah"), "consequent": "Tinggi"},
    {"antecedent": ("Tinggi", "Rendah", "Sedang"), "consequent": "Tinggi"},
    {"antecedent": ("Tinggi", "Rendah", "Tinggi"), "consequent": "Tinggi"},
    {"antecedent": ("Tinggi", "Sedang", "Rendah"), "consequent": "Tinggi"},
    {"antecedent": ("Tinggi", "Sedang", "Sedang"), "consequent": "Tinggi"},
    {"antecedent": ("Tinggi", "Sedang", "Tinggi"), "consequent": "Tinggi"},
    {"antecedent": ("Tinggi", "Tinggi", "Rendah"), "consequent": "Tinggi"},
    {"antecedent": ("Tinggi", "Tinggi", "Sedang"), "consequent": "Tinggi"},
    {"antecedent": ("Tinggi", "Tinggi", "Tinggi"), "consequent": "Tinggi"},
]

# Fungsi untuk menghitung z berdasarkan Tsukamoto Method
def calculate_z_sedang(mu):
    """
    Menghitung z untuk 'Sedang' berdasarkan derajat keanggotaan mu.
    Fungsi keanggotaan 'Sedang' adalah segitiga [20, 50, 80].
    """
    if mu <= 0:
        return 0  # Tidak ada kontribusi
    elif 0 < mu < 1.0:
        # Hitung z pada sisi kenaikan dan penurunan
        z_rising = 20 + mu * (50 - 20)       # Sisi kenaikan dari 20 ke 50
        z_falling = 80 - mu * (80 - 50)      # Sisi penurunan dari 80 ke 50
        # Rata-rata kedua z untuk mendapatkan nilai tunggal
        z = (z_rising + z_falling) / 2
    elif mu == 1.0:
        z = 50  # Titik puncak
    else:
        z = 0
    return z

def calculate_z_tinggi(mu):
    """
    Menghitung z untuk 'Tinggi' berdasarkan derajat keanggotaan mu.
    Fungsi keanggotaan 'Tinggi' adalah segitiga [75, 100, 100].
    """
    if mu <= 0:
        return 0
    elif 0 < mu <= 1.0:
        z = 75 + mu * (100 - 75)
    else:
        z = 0
    return z

def calculate_z_rendah(mu):
    """
    Menghitung z untuk 'Rendah' berdasarkan derajat keanggotaan mu.
    Fungsi keanggotaan 'Rendah' adalah segitiga [0, 0, 25].
    """
    if mu <= 0:
        return 0
    elif 0 < mu <= 1.0:
        z = mu * 25
    else:
        z = 0
    return z

# Mapping dari konsekuen ke fungsi z
def get_z_value(consequent, mu):
    if consequent == "Rendah":
        return calculate_z_rendah(mu)
    elif consequent == "Sedang":
        return calculate_z_sedang(mu)
    elif consequent == "Tinggi":
        return calculate_z_tinggi(mu)
    else:
        return 0

# Fungsi untuk menjalankan Fuzzy Tsukamoto untuk satu data point
def fuzzy_tsukamoto(data_point, rules):
    # Fuzzifikasi
    degrees_request_count = get_membership_degrees_request_count(data_point["request_count"])
    degrees_system_security = get_membership_degrees_system_security_level(data_point["system_security_level"])
    degrees_anomalous_data = get_membership_degrees_anomalous_data_volume(data_point["anomalous_data_volume"])
    
    # Menyimpan nilai z dan alpha
    z_values = []
    alphas = []
    rule_steps = []
    
    # Evaluasi setiap aturan
    for idx, rule in enumerate(rules, start=1):
        antecedent = rule["antecedent"]
        consequent = rule["consequent"]
        
        # Mendapatkan derajat keanggotaan untuk antecedent
        mu_request = degrees_request_count.get(antecedent[0], 0)
        mu_security = degrees_system_security.get(antecedent[1], 0)
        mu_anomalous = degrees_anomalous_data.get(antecedent[2], 0)
        
        # Menghitung alpha (firing strength)
        alpha = min(mu_request, mu_security, mu_anomalous)
        
        if alpha > 0:
            # Menghitung z untuk konsekuen
            z = get_z_value(consequent, alpha)
            if z > 0:
                z_values.append(z)
                alphas.append(alpha)
                rule_steps.append({
                    'rule_number': idx,
                    'antecedent': antecedent,
                    'consequent': consequent,
                    'alpha': alpha,
                    'z': z
                })
    
    # Defuzzifikasi
    if len(z_values) == 0:
        # Tidak ada aturan yang terpenuhi, bisa diatur ke nilai default
        z_final = 0
    else:
        # Tsukamoto: z = sum(alpha * z) / sum(alpha)
        numerator = sum([a * z for a, z in zip(alphas, z_values)])
        denominator = sum(alphas)
        z_final = numerator / denominator if denominator != 0 else 0
    
    # Menyimpan langkah-langkah untuk ditampilkan
    steps = {
        'fuzzification': {
            'Jumlah Permintaan Akses': degrees_request_count,
            'Tingkat Keamanan Sistem': degrees_system_security,
            'Volume Data Anomali': degrees_anomalous_data
        },
        'rule_evaluation': rule_steps,
        'defuzzification': {
            'alphas': alphas,
            'z_values': z_values,
            'z_final': z_final
        }
    }
    
    return z_final, steps

# Fungsi untuk menghitung MAE dan Akurasi
def evaluate_performance(computed, actual):
    error = abs(computed - actual)
    accuracy = 1 - (error / 100)
    return error, accuracy

# Fungsi untuk plotting fungsi keanggotaan
def plot_membership(levels_func, var_name, input_value=None):
    x_min = 0
    x_max = 0
    if var_name == "Jumlah Permintaan Akses":
        x_min, x_max = 0, 1000
    elif var_name == "Tingkat Keamanan Sistem":
        x_min, x_max = 0, 10
    elif var_name == "Volume Data Anomali":
        x_min, x_max = 0, 500
    elif var_name == "Tingkat Resiko Serangan Siber":
        x_min, x_max = 0, 100
    x_values = np.linspace(x_min, x_max, 500)
    plt.figure(figsize=(8, 4))
    for level in ["Rendah", "Sedang", "Tinggi"]:
        y_values = [levels_func(x)[level] for x in x_values]
        plt.plot(x_values, y_values, label=f"{level}")
    if input_value is not None:
        degrees = levels_func(input_value)
        y_marker = max(degrees.values())
        plt.axvline(x=input_value, linestyle='--', color='k')
        plt.plot(input_value, y_marker, 'ro')
        plt.text(input_value, y_marker + 0.05, f'Input = {input_value}', ha='center')
    plt.title(f"Fungsi Keanggotaan - {var_name}")
    plt.xlabel(var_name)
    plt.ylabel("Derajat Keanggotaan")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)
    plt.clf()

# Dataset
dataset = [
    {"request_count": 200, "system_security_level": 3, "anomalous_data_volume": 50, "actual": 30},
    {"request_count": 400, "system_security_level": 2, "anomalous_data_volume": 150, "actual": 60},
    {"request_count": 150, "system_security_level": 8, "anomalous_data_volume": 30, "actual": 20},
    {"request_count": 900, "system_security_level": 1, "anomalous_data_volume": 400, "actual": 95},
    {"request_count": 250, "system_security_level": 5, "anomalous_data_volume": 80, "actual": 40},
    {"request_count": 700, "system_security_level": 3, "anomalous_data_volume": 300, "actual": 85},
    {"request_count": 100, "system_security_level": 9, "anomalous_data_volume": 20, "actual": 10},
    {"request_count": 500, "system_security_level": 7, "anomalous_data_volume": 100, "actual": 50},
    {"request_count": 800, "system_security_level": 4, "anomalous_data_volume": 350, "actual": 90},
    {"request_count": 300, "system_security_level": 6, "anomalous_data_volume": 60, "actual": 35},
]

# Streamlit App
st.title("Implementasi Fuzzy Tsukamoto untuk Prediksi Resiko Serangan Siber")

# Menu pilihan
menu = st.sidebar.selectbox("Pilih Menu", ["Tampilkan Hasil Dataset", "Input Manual"])

if menu == "Tampilkan Hasil Dataset":
    st.header("Hasil Prediksi dari Dataset")
    results = []
    for idx, data_point in enumerate(dataset, start=1):
        computed, _ = fuzzy_tsukamoto(data_point, rules)
        actual = data_point["actual"]
        error, accuracy = evaluate_performance(computed, actual)
        results.append({
            "Data Point": idx,
            "Computed CA Risk Level": round(computed, 2),
            "Actual CA Risk Level": actual,
            "Error": round(error, 2),
            "Akurasi (%)": round(accuracy * 100, 2)
        })
    # Tampilkan tabel hasil
    st.table(results)
    
    # Menghitung MAE dan Akurasi Rata-rata
    mae = sum([res["Error"] for res in results]) / len(results)
    average_accuracy = sum([res["Akurasi (%)"] for res in results]) / len(results)
    
    st.write("\n### Performance Metrics")
    st.write(f"- **Mean Absolute Error (MAE)**: {round(mae, 2)}")
    st.write(f"- **Akurasi Rata-rata**: {round(average_accuracy, 2)}%")
    
    # Pilih Data Point untuk melihat proses perhitungan
    st.write("\nPilih Data Point untuk melihat proses perhitungan:")
    selected_point = st.selectbox("Pilih Data Point", [f"Data Point {i}" for i in range(1, len(dataset)+1)])
    selected_index = int(selected_point.split()[2]) - 1
    data_point = dataset[selected_index]
    computed, steps = fuzzy_tsukamoto(data_point, rules)
    actual = data_point["actual"]
    st.write(f"\n### Proses perhitungan untuk {selected_point}:")
    st.write(f"Input:")
    st.write(f"- Jumlah Permintaan Akses: {data_point['request_count']}")
    st.write(f"- Tingkat Keamanan Sistem: {data_point['system_security_level']}")
    st.write(f"- Volume Data Anomali: {data_point['anomalous_data_volume']}")
    st.write(f"Prediksi: {computed:.2f}, Aktual: {actual}")
    
    # Tampilkan langkah-langkah perhitungan
    st.subheader("Proses dan Tahap Algoritma Fuzzy Tsukamoto")
    
    st.write("### Fuzzifikasi")
    st.write("Derajat Keanggotaan untuk setiap variabel input:")
    for var_name, memberships in steps['fuzzification'].items():
        st.write(f"**{var_name}:**")
        for level, degree in memberships.items():
            st.write(f"- {level}: {degree:.4f}")
    
    st.write("### Evaluasi Aturan")
    st.write("Aturan yang aktif dan perhitungan nilai α dan z:")
    if steps['rule_evaluation']:
        for rule_step in steps['rule_evaluation']:
            rule_number = rule_step['rule_number']
            antecedent = rule_step['antecedent']
            consequent = rule_step['consequent']
            alpha = rule_step['alpha']
            z = rule_step['z']
            st.write(f"**Aturan {rule_number}:** Jika {antecedent} maka {consequent}")
            st.write(f"- α (derajat kebenaran): {alpha:.4f}")
            st.write(f"- Nilai z: {z:.4f}")
    else:
        st.write("Tidak ada aturan yang aktif.")
    
    st.write("### Defuzzifikasi")
    total_alpha = sum(steps['defuzzification']['alphas'])
    if total_alpha == 0:
        st.write("Tidak ada aturan yang aktif.")
    else:
        st.write(f"Nilai z akhir (Tingkat Resiko Serangan Siber): {computed:.2f}")
    
    # Tampilkan grafik fungsi keanggotaan dengan posisi input
    st.header("Grafik Fungsi Keanggotaan dengan Posisi Input")
    st.subheader("Jumlah Permintaan Akses")
    plot_membership(get_membership_degrees_request_count, "Jumlah Permintaan Akses", data_point['request_count'])
    
    st.subheader("Tingkat Keamanan Sistem")
    plot_membership(get_membership_degrees_system_security_level, "Tingkat Keamanan Sistem", data_point['system_security_level'])
    
    st.subheader("Volume Data Anomali")
    plot_membership(get_membership_degrees_anomalous_data_volume, "Volume Data Anomali", data_point['anomalous_data_volume'])
    
    st.subheader("Tingkat Resiko Serangan Siber")
    plot_membership(get_membership_degrees_cyber_attack_risk_level, "Tingkat Resiko Serangan Siber", computed)
    
elif menu == "Input Manual":
    st.header("Input Data Manual")
    request_count = st.slider("Jumlah Permintaan Akses (0-1000):", 0, 1000, 500)
    security_level = st.slider("Tingkat Keamanan Sistem (0-10):", 0, 10, 5)
    anomalous_data = st.slider("Volume Data Anomali (0-500):", 0, 500, 250)
    
    data_point = {
        "request_count": request_count,
        "system_security_level": security_level,
        "anomalous_data_volume": anomalous_data,
        "actual": None
    }
    
    computed, steps = fuzzy_tsukamoto(data_point, rules)
    st.write(f"Tingkat Resiko Serangan Siber untuk input ini adalah: **{computed:.2f}**")
    
    # Tampilkan langkah-langkah perhitungan
    st.subheader("Proses dan Tahap Algoritma Fuzzy Tsukamoto")
    
    st.write("### Fuzzifikasi")
    st.write("Derajat Keanggotaan untuk setiap variabel input:")
    for var_name, memberships in steps['fuzzification'].items():
        st.write(f"**{var_name}:**")
        for level, degree in memberships.items():
            st.write(f"- {level}: {degree:.4f}")
    
    st.write("### Evaluasi Aturan")
    st.write("Aturan yang aktif dan perhitungan nilai α dan z:")
    if steps['rule_evaluation']:
        for rule_step in steps['rule_evaluation']:
            rule_number = rule_step['rule_number']
            antecedent = rule_step['antecedent']
            consequent = rule_step['consequent']
            alpha = rule_step['alpha']
            z = rule_step['z']
            st.write(f"**Aturan {rule_number}:** Jika {antecedent} maka {consequent}")
            st.write(f"- α (derajat kebenaran): {alpha:.4f}")
            st.write(f"- Nilai z: {z:.4f}")
    else:
        st.write("Tidak ada aturan yang aktif.")
    
    st.write("### Defuzzifikasi")
    total_alpha = sum(steps['defuzzification']['alphas'])
    if total_alpha == 0:
        st.write("Tidak ada aturan yang aktif.")
    else:
        st.write(f"Nilai z akhir (Tingkat Resiko Serangan Siber): {computed:.2f}")
    
    # Tampilkan grafik fungsi keanggotaan dengan posisi input
    st.header("Grafik Fungsi Keanggotaan dengan Posisi Input")
    st.subheader("Jumlah Permintaan Akses")
    plot_membership(get_membership_degrees_request_count, "Jumlah Permintaan Akses", request_count)
    
    st.subheader("Tingkat Keamanan Sistem")
    plot_membership(get_membership_degrees_system_security_level, "Tingkat Keamanan Sistem", security_level)
    
    st.subheader("Volume Data Anomali")
    plot_membership(get_membership_degrees_anomalous_data_volume, "Volume Data Anomali", anomalous_data)
    
    st.subheader("Tingkat Resiko Serangan Siber")
    plot_membership(get_membership_degrees_cyber_attack_risk_level, "Tingkat Resiko Serangan Siber", computed)
