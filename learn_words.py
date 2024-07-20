import json
import random
import tkinter as tk
from tkinter import ttk, messagebox

kelimeler_dosyasi = "kelimeler.json"
eksik_kelimeler_dosyasi = "eksik_kelimeler.json"
ezberlenen_kelimeler_dosyasi = "ezberlenen_kelimeler.json"
kelimeler_v3_dosyasi = "kelimeler_v3.json"



def load_data(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    return data

def save_data(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def add_word():
    ing_kelime = ing_kelime_entry.get()
    tr_kelime = tr_kelime_entry.get()
    
    if ing_kelime and tr_kelime:
        kelimeler = load_data(kelimeler_dosyasi)
        eksik_kelimeler = load_data(eksik_kelimeler_dosyasi)
        ezberlenen_kelimeler = load_data(ezberlenen_kelimeler_dosyasi)
        
        # Kontrol et
        if (ing_kelime in kelimeler) or (ing_kelime in eksik_kelimeler) or (ing_kelime in ezberlenen_kelimeler):
            messagebox.showwarning("Uyarı", "Kelime zaten mevcut!")
        else:
            kelimeler[ing_kelime] = {"tr": tr_kelime, "puan": 99}
            save_data(kelimeler_dosyasi, kelimeler)
            messagebox.showinfo("Bilgi", "Kelime başarıyla eklendi!")
            ing_kelime_entry.delete(0, tk.END)
            tr_kelime_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Uyarı", "Kelime kutuları boş olamaz!")



def test_word():
    kelimeler = load_data(kelimeler_dosyasi)
    if kelimeler:
        weighted_words = []
        for word, data in kelimeler.items():
            weight = 10 if data["puan"] == 99 else 1
            weighted_words.extend([word] * weight)

        global current_word, current_answer
        current_word = random.choice(weighted_words)
        current_answer = kelimeler[current_word]["tr"]
        
        question_label_learn.config(text=f"İngilizce kelime: {current_word}")
        answer_entry_learn.delete(0, tk.END)
    else:
        messagebox.showinfo("Bilgi", "Kelime bulunamadı!")

def check_answer():
    global current_word, current_answer
    user_answer = answer_entry_learn.get().strip()
    
    kelimeler = load_data(kelimeler_dosyasi)
    
    if user_answer:
        if current_word in kelimeler:
            if user_answer.lower() == current_answer.lower():
                if kelimeler[current_word]["puan"] == 99:
                    kelimeler[current_word]["puan"] = 1  # Doğru cevap verildiğinde puanı 1 yap
                else:
                    kelimeler[current_word]["puan"] += 1
                
                if kelimeler[current_word]["puan"] == 3:
                    messagebox.showinfo("Tebrikler", f"{current_word} kelimesi ezberlendi ve ezberlenen kelimeler dosyasına taşındı!")
                    move_to_learned(current_word)
                else:
                    messagebox.showinfo("Tebrikler", "Doğru cevap! Puan artırıldı.")
            else:
                if kelimeler[current_word]["puan"] == 99:
                    kelimeler[current_word]["puan"] = -1 
                else:
                    kelimeler[current_word]["puan"] -= 1

                if kelimeler[current_word]["puan"] <= -2:
                    kelimeler[current_word]["puan"] = -2
                    move_to_missing(current_word, kelimeler[current_word]["tr"])
                    messagebox.showinfo("Bilgi", f"Kelime unutuldu ve eksik kelimeler dosyasına gönderildi: {current_word}")
                else:
                    messagebox.showinfo("Yanlış", "Yanlış cevap! Puan düşürüldü.")
                
            # Kelimeyi kelimeler.json dosyasından sil
            if kelimeler[current_word]["puan"] == 3 or kelimeler[current_word]["puan"] == -2:
                del kelimeler[current_word]
                
            save_data(kelimeler_dosyasi, kelimeler)
        else:
            messagebox.showwarning("Uyarı", "Kelime mevcut değil!")
    
    test_word()


def move_to_learned(word):
    kelimeler = load_data(kelimeler_dosyasi)
    learned_words = load_data(ezberlenen_kelimeler_dosyasi)
    
    if word in kelimeler:
        word_data = kelimeler.pop(word)  # Kelimeyi 'kelimeler.json'dan çıkar
        word_data["puan"] = 1  # Başlangıç puanı 1
        learned_words[word] = word_data  # Kelimeyi 'ezberlenen_kelimeler.json' dosyasına ekle
        save_data(kelimeler_dosyasi, kelimeler)  # Güncellenmiş 'kelimeler.json' dosyasını kaydet
        save_data(ezberlenen_kelimeler_dosyasi, learned_words)  # Güncellenmiş 'ezberlenen_kelimeler.json' dosyasını kaydet


def move_to_forget(word):
    learned_words = load_data("ezberlenen_kelimeler.json")
    kelimeler = load_data(kelimeler_dosyasi)
    
    if word in learned_words:
        word_data = learned_words.pop(word)
        word_data["puan"] = 99  # Başlangıç puanı 99
        kelimeler[word] = word_data
        save_data(kelimeler_dosyasi, kelimeler)
        save_data("ezberlenen_kelimeler.json", learned_words)
        messagebox.showinfo("Bilgi", f"Kelime unutuldu ve tekrar kelimeler.json dosyasına eklendi.")

def test_learned_word():
    learned_words = load_data("ezberlenen_kelimeler.json")
    if learned_words:
        global current_word, current_answer
        weighted_words = [word for word in learned_words]
        
        if weighted_words:
            current_word = random.choice(weighted_words)
            current_answer = learned_words[current_word]["tr"]
            
            question_label_learned.config(text=f"İngilizce kelime: {current_word}")
            answer_entry_learned.delete(0, tk.END)
        else:
            messagebox.showinfo("Bilgi", "Ezberlenen kelime bulunamadı!")
    else:
        messagebox.showinfo("Bilgi", "Ezberlenen kelimeler dosyası boş!")

def check_learned_answer():
    global current_word, current_answer
    user_answer = answer_entry_learned.get().strip()
    
    learned_words = load_data("ezberlenen_kelimeler.json")
    
    if user_answer:
        if current_word in learned_words:
            if user_answer.lower() == current_answer.lower():
                learned_words[current_word]["puan"] += 1
                if learned_words[current_word]["puan"] <= 0:
                    move_to_forget(current_word)
                else:
                    save_data("ezberlenen_kelimeler.json", learned_words)
                    messagebox.showinfo("Tebrikler", "Doğru cevap! Puan artırıldı.")
            else:
                learned_words[current_word]["puan"] -= 1
                if learned_words[current_word]["puan"] <= 0:
                    move_to_forget(current_word)
                else:
                    save_data("ezberlenen_kelimeler.json", learned_words)
                    messagebox.showinfo("Yanlış", "Yanlış cevap! Puan düşürüldü.")
        else:
            messagebox.showwarning("Uyarı", "Kelime mevcut değil!")
    
    test_learned_word()



def move_to_learned(word):
    kelimeler = load_data(kelimeler_dosyasi)
    learned_words = load_data(ezberlenen_kelimeler_dosyasi)
    
    if word in kelimeler:
        word_data = kelimeler.pop(word)  # Kelimeyi 'kelimeler.json'dan çıkar
        word_data["puan"] = 1  # Başlangıç puanı 1
        learned_words[word] = word_data  # Kelimeyi 'ezberlenen_kelimeler.json' dosyasına ekle
        save_data(kelimeler_dosyasi, kelimeler)  # Güncellenmiş 'kelimeler.json' dosyasını kaydet
        save_data(ezberlenen_kelimeler_dosyasi, learned_words)  # Güncellenmiş 'ezberlenen_kelimeler.json' dosyasını kaydet


def move_to_missing(word, translation):
    missing_words = load_data(eksik_kelimeler_dosyasi)
    kelimeler = load_data(kelimeler_dosyasi)

    if word in missing_words:
        missing_words[word]["puan"] -= 1
        if missing_words[word]["puan"] <= -2:
            missing_words[word]["puan"] = 0
            kelimeler[word] = missing_words.pop(word)
            save_data(kelimeler_dosyasi, kelimeler)
            messagebox.showinfo("Bilgi", f"{word} kelimesi tekrar kelimeler.json dosyasına eklendi.")
    else:
        missing_words[word] = {"tr": translation, "puan": -1}

    save_data(eksik_kelimeler_dosyasi, missing_words)


def test_missing_word():
    missing_words = load_data(eksik_kelimeler_dosyasi)
    if missing_words:
        global current_word, current_answer
        # Eksik kelimeleri doğrudan alın
        weighted_words = [word for word in missing_words]
        
        if weighted_words:
            current_word = random.choice(weighted_words)
            current_answer = missing_words[current_word]["tr"]
            
            question_label_missing.config(text=f"İngilizce kelime: {current_word}")
            answer_entry_missing.delete(0, tk.END)
        else:
            messagebox.showinfo("Bilgi", "Eksik kelime bulunamadı!")
    else:
        messagebox.showinfo("Bilgi", "Eksik kelimeler dosyası boş!")

def check_missing_answer():
    global current_word, current_answer
    user_answer = answer_entry_missing.get().strip()
    
    missing_words = load_data(eksik_kelimeler_dosyasi)
    
    if user_answer:
        if current_word in missing_words:
            if user_answer.lower() == current_answer.lower():
                # Doğru cevap
                missing_words[current_word]["puan"] += 1
                if missing_words[current_word]["puan"] >= 0:
                    kelimeler = load_data(kelimeler_dosyasi)
                    kelimeler[current_word] = missing_words.pop(current_word)
                    save_data(kelimeler_dosyasi, kelimeler)
                    save_data(eksik_kelimeler_dosyasi, missing_words)
                    messagebox.showinfo("Tebrikler", "Kelime doğru! Kelime tekrar kelimeler.json dosyasına eklendi.")
                else:
                    save_data(eksik_kelimeler_dosyasi, missing_words)
                    messagebox.showinfo("Tebrikler", "Doğru cevap! Puan artırıldı.")
            else:
                # Yanlış cevap
                missing_words[current_word]["puan"] -= 1
                if missing_words[current_word]["puan"] <= -2:
                    missing_words[current_word]["puan"] = -2  # Puanı -2 olarak güncelle
                if missing_words[current_word]["puan"] == 0:
                    # Puan 0 olduğunda kelimeyi taşır
                    kelimeler = load_data(kelimeler_dosyasi)
                    kelimeler[current_word] = missing_words.pop(current_word)
                    save_data(kelimeler_dosyasi, kelimeler)
                    save_data(eksik_kelimeler_dosyasi, missing_words)
                    messagebox.showinfo("Bilgi", "Kelime tekrar kelimeler.json dosyasına eklendi.")
                else:
                    save_data(eksik_kelimeler_dosyasi, missing_words)
                    messagebox.showinfo("Yanlış", "Yanlış cevap! Puan düşürüldü.")
        else:
            messagebox.showwarning("Uyarı", "Kelime mevcut değil!")
    
    test_missing_word()

def load_v3_data():
    try:
        with open(kelimeler_v3_dosyasi, 'r') as file:
            kelimeler_v3 = json.load(file)
    except FileNotFoundError:
        kelimeler_v3 = {}
    return kelimeler_v3

def save_v3_data(kelimeler_v3):
    with open(kelimeler_v3_dosyasi, 'w') as file:
        json.dump(kelimeler_v3, file, indent=4)

def add_v3_word():
    v1_kelime = v1_kelime_entry.get()
    v2_kelime = v2_kelime_entry.get()
    v3_kelime = v3_kelime_entry.get()
    
    if v1_kelime and v2_kelime and v3_kelime:
        kelimeler_v3 = load_v3_data()
        
        # Kontrol et
        if v1_kelime in kelimeler_v3:
            messagebox.showwarning("Uyarı", "V1 kelime zaten mevcut!")
        else:
            kelimeler_v3[v1_kelime] = {"v2": v2_kelime, "v3": v3_kelime, "puan": 20}
            save_v3_data(kelimeler_v3)
            messagebox.showinfo("Bilgi", "V1, V2, V3 kelime başarıyla eklendi!")
            v1_kelime_entry.delete(0, tk.END)
            v2_kelime_entry.delete(0, tk.END)
            v3_kelime_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Uyarı", "Tüm kutuların doldurulması gerekiyor!")



weight_multiplier = 500  # Buraya ağırlık katsayısını ayarlayabilirsiniz

def test_v3_word():
    kelimeler_v3 = load_v3_data()
    if kelimeler_v3:
        weighted_words = []
        for word, data in kelimeler_v3.items():
            # Kelimenin puanını dikkate alarak ağırlıklandırma yap
            weight = data["puan"] * weight_multiplier  # Katsayı ile çarpma
            weighted_words.extend([word] * int(weight))  # int() ile tam sayıya çevir
        
        if weighted_words:
            global current_word_v3, current_answer_v3
            current_word_v3 = random.choice(weighted_words)  # Ağırlıklı olarak rastgele kelime seç
            current_answer_v3 = kelimeler_v3[current_word_v3]["v2"]
            
            question_label_v3.config(text=f"V1 kelime: {current_word_v3}")
            answer_entry_v2.delete(0, tk.END)
            answer_entry_v3.delete(0, tk.END)
        else:
            messagebox.showinfo("Bilgi", "V3 kelime bulunamadı!")

def check_v2_and_v3_answer():
    global current_word_v3, current_answer_v3
    v2_answer = answer_entry_v2.get().strip()
    v3_answer = answer_entry_v3.get().strip()
    
    kelimeler_v3 = load_v3_data()
    
    if v2_answer and v3_answer:
        correct_v2 = kelimeler_v3[current_word_v3]["v2"].lower()
        correct_v3 = kelimeler_v3[current_word_v3]["v3"].lower()
        
        v2_correct = v2_answer.lower() == correct_v2
        v3_correct = v3_answer.lower() == correct_v3
        
        if v2_correct and v3_correct:
            messagebox.showinfo("Tebrikler", "Her iki cevap da doğru!")
        elif v2_correct:
            messagebox.showinfo("Tebrikler", "V2 cevabı doğru, V3 cevabı yanlış.")
        elif v3_correct:
            messagebox.showinfo("Tebrikler", "V2 cevabı yanlış, V3 cevabı doğru.")
        else:
            messagebox.showinfo("Yanlış", f"Her iki cevap da yanlış. Doğru cevaplar: V2: {correct_v2}, V3: {correct_v3}.")
        
        test_v3_word()
    else:
        messagebox.showwarning("Uyarı", "Cevap kutuları boş olamaz!")

app = tk.Tk()
app.title("Kelime Öğrenme Uygulaması")

# Sekmeler oluşturuluyor
tab_control = ttk.Notebook(app)

# Görsel iyileştirmeler
font_style = ('Helvetica', 12)
button_bg_color = '#4CAF50'
button_fg_color = '#FFFFFF'
pad_x = 10
pad_y = 5

# Kelime Ekleme Sekmesi
add_word_tab = ttk.Frame(tab_control)
tab_control.add(add_word_tab, text="Kelime Ekle")

tk.Label(add_word_tab, text="İngilizce Kelime:", font=font_style).pack(pady=pad_y)
ing_kelime_entry = tk.Entry(add_word_tab, font=font_style)
ing_kelime_entry.pack(pady=pad_y, padx=pad_x)
tk.Label(add_word_tab, text="Türkçe Kelime:", font=font_style).pack(pady=pad_y)
tr_kelime_entry = tk.Entry(add_word_tab, font=font_style)
tr_kelime_entry.pack(pady=pad_y, padx=pad_x)
add_word_button = tk.Button(add_word_tab, text="Kelime Ekle", command=add_word, bg=button_bg_color, fg=button_fg_color)
add_word_button.pack(pady=pad_y)

# Kelime Öğrenme Sekmesi
learn_word_tab = ttk.Frame(tab_control)
tab_control.add(learn_word_tab, text="Kelime Öğren")

question_label_learn = tk.Label(learn_word_tab, text="İngilizce kelime:", font=font_style)
question_label_learn.pack(pady=pad_y)
answer_entry_learn = tk.Entry(learn_word_tab, font=font_style)
answer_entry_learn.pack(pady=pad_y, padx=pad_x)
check_answer_button = tk.Button(learn_word_tab, text="Cevabı Kontrol Et", command=check_answer, bg=button_bg_color, fg=button_fg_color)
check_answer_button.pack(pady=pad_y)
test_word_button = tk.Button(learn_word_tab, text="Kelimeyi Test Et", command=test_word, bg=button_bg_color, fg=button_fg_color)
test_word_button.pack(pady=pad_y)

# Eksik Kelimeler Sekmesi
missing_word_tab = ttk.Frame(tab_control)
tab_control.add(missing_word_tab, text="Eksik Kelimeler")

question_label_missing = tk.Label(missing_word_tab, text="İngilizce kelime:", font=font_style)
question_label_missing.pack(pady=pad_y)
answer_entry_missing = tk.Entry(missing_word_tab, font=font_style)
answer_entry_missing.pack(pady=pad_y, padx=pad_x)
check_missing_answer_button = tk.Button(missing_word_tab, text="Cevabı Kontrol Et", command=check_missing_answer, bg=button_bg_color, fg=button_fg_color)
check_missing_answer_button.pack(pady=pad_y)
test_missing_word_button = tk.Button(missing_word_tab, text="Eksik Kelimeyi Test Et", command=test_missing_word, bg=button_bg_color, fg=button_fg_color)
test_missing_word_button.pack(pady=pad_y)

# Ezberlenen Kelimeler Sekmesi
learned_word_tab = ttk.Frame(tab_control)
tab_control.add(learned_word_tab, text="Ezberlenen Kelimeler")

question_label_learned = tk.Label(learned_word_tab, text="İngilizce kelime:", font=font_style)
question_label_learned.pack(pady=pad_y)
answer_entry_learned = tk.Entry(learned_word_tab, font=font_style)
answer_entry_learned.pack(pady=pad_y, padx=pad_x)
check_learned_answer_button = tk.Button(learned_word_tab, text="Cevabı Kontrol Et", command=check_learned_answer, bg=button_bg_color, fg=button_fg_color)
check_learned_answer_button.pack(pady=pad_y)
test_learned_word_button = tk.Button(learned_word_tab, text="Ezberlenen Kelimeyi Test Et", command=test_learned_word, bg=button_bg_color, fg=button_fg_color)
test_learned_word_button.pack(pady=pad_y)

# V1, V2, V3 Kelimeler Sekmesi
v3_tab = ttk.Frame(tab_control)
tab_control.add(v3_tab, text="V1, V2, V3 Kelimeler")

tk.Label(v3_tab, text="V1 Kelime:", font=font_style).pack(pady=pad_y)
v1_kelime_entry = tk.Entry(v3_tab, font=font_style)
v1_kelime_entry.pack(pady=pad_y, padx=pad_x)
tk.Label(v3_tab, text="V2 Kelime:", font=font_style).pack(pady=pad_y)
v2_kelime_entry = tk.Entry(v3_tab, font=font_style)
v2_kelime_entry.pack(pady=pad_y, padx=pad_x)
tk.Label(v3_tab, text="V3 Kelime:", font=font_style).pack(pady=pad_y)
v3_kelime_entry = tk.Entry(v3_tab, font=font_style)
v3_kelime_entry.pack(pady=pad_y, padx=pad_x)
add_v3_word_button = tk.Button(v3_tab, text="V1, V2, V3 Kelime Ekle", command=add_v3_word, bg=button_bg_color, fg=button_fg_color)
add_v3_word_button.pack(pady=pad_y)

# V1, V2, V3 Kelimeleri Test Et
v3_test_tab = ttk.Frame(tab_control)
tab_control.add(v3_test_tab, text="V1, V2, V3 Test")

question_label_v3 = tk.Label(v3_test_tab, text="V1 kelime:", font=font_style)
question_label_v3.pack(pady=pad_y)
answer_entry_v2 = tk.Entry(v3_test_tab, font=font_style)
answer_entry_v2.pack(pady=pad_y, padx=pad_x)
answer_entry_v3 = tk.Entry(v3_test_tab, font=font_style)
answer_entry_v3.pack(pady=pad_y, padx=pad_x)
check_v3_answer_button = tk.Button(v3_test_tab, text="Cevapları Kontrol Et (V2 & V3)", command=check_v2_and_v3_answer, bg=button_bg_color, fg=button_fg_color)
check_v3_answer_button.pack(pady=pad_y)
test_v3_word_button = tk.Button(v3_test_tab, text="V1, V2, V3 Test Et", command=test_v3_word, bg=button_bg_color, fg=button_fg_color)
test_v3_word_button.pack(pady=pad_y)

tab_control.pack(expand=1, fill="both")


app.mainloop()