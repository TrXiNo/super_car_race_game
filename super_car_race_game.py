import tkinter as tk
import random
import winsound
import threading
import os

class ArabaYarisiGelisimis:
    def __init__(self, root):
        self.root = root
        self.root.title("🏎️ Süper Araba Yarışı v3.0")
        self.root.resizable(False, False)

        # Oyun Alanı Boyutları
        self.genislik = 400
        self.yukseklik = 600
        
        # Oyun Değişkenleri ve Sabitleri
        self.seritler = [90, 200, 310]  # Şeritlerin merkez X piksel koordinatları
        self.oyuncu_serit_idx = 1       # Oyuncu yarışa orta şeritte başlar
        self.skor = 0
        self.baslangic_hizi = 8
        self.hiz = self.baslangic_hizi
        
        # Durum Kontrolleri
        self.oyun_aktif = False
        self.duraklatildi = False
        self.ses_acik = True
        self.tanri_modu = False
        
        # Nesne Listeleri
        self.engeller = []
        self.serit_cizgileri = []
        self.oyuncu_parcalari = []
        
        # Skor Dosyası Tanımı
        self.skor_dosyasi = "skorlar.txt"
        self.en_yuksek_skor = 0
        self.en_son_skor = 0
        self.skorlari_yukle()
        
        # İlk olarak Ana Menüyü Yükle
        self.ana_menu_olustur()

    def skorlari_yukle(self):
        """Kalıcı skor hafızasından en yüksek ve en son skoru çeker."""
        if os.path.exists(self.skor_dosyasi):
            try:
                with open(self.skor_dosyasi, "r", encoding="utf-8") as f:
                    satirlar = f.read().splitlines()
                    if len(satirlar) >= 2:
                        self.en_yuksek_skor = int(satirlar[0])
                        self.en_son_skor = int(satirlar[1])
            except Exception:
                pass

    def skoru_kaydet(self):
        """Mevcut skoru kaydeder ve en yüksek skoru günceller."""
        self.en_son_skor = self.skor
        if self.skor > self.en_yuksek_skor:
            self.en_yuksek_skor = self.skor
        try:
            with open(self.skor_dosyasi, "w", encoding="utf-8") as f:
                f.write(f"{self.en_yuksek_skor}\n{self.en_son_skor}")
        except Exception:
            pass

    def ses_cal(self, frekans, sure):
        """Oyunun akışını (FPS) dondurmaması için sesleri arka planda (Thread) çalıştırır."""
        if self.ses_acik:
            threading.Thread(target=winsound.Beep, args=(frekans, sure), daemon=True).start()

    def ana_menu_olustur(self):
        """Oyun ilk açıldığında veya yeniden başlandığında ekrana gelen şık giriş menüsü."""
        self.menu_frame = tk.Frame(self.root, bg="#222222", width=self.genislik, height=self.yukseklik + 50)
        self.menu_frame.pack_propagate(False)
        self.menu_frame.pack()

        baslik = tk.Label(self.menu_frame, text="🏎️ SPEED RACER", font=("Arial", 28, "bold"), bg="#222222", fg="#ffcc00")
        baslik.pack(pady=40)

        # İstatistik Paneli
        istatistik_text = f"📊 EN YÜKSEK SKOR: {self.en_yuksek_skor}\n🏁 EN SON SKOR: {self.en_son_skor}"
        lbl_istatistik = tk.Label(self.menu_frame, text=istatistik_text, font=("Arial", 12, "bold"), bg="#111111", fg="#00ffff", width=30, height=3, relief="groove", bd=2)
        lbl_istatistik.pack(pady=10)

        # Menü Butonları
        btn_oyna = tk.Button(self.menu_frame, text="OYNA", font=("Arial", 14, "bold"), bg="#00cc44", fg="white", width=18, command=self.oyunu_baslat)
        btn_oyna.pack(pady=12)

        self.btn_ses = tk.Button(self.menu_frame, text="🔊 SES EFFECTS: AÇIK" if self.ses_acik else "🔇 SES EFFECTS: KAPALI", font=("Arial", 12, "bold"), bg="#333333" if self.ses_acik else "#cc0000", fg="white", width=18, command=self.ses_durumu_degistir)
        self.btn_ses.pack(pady=12)

        btn_ayarlar = tk.Button(self.menu_frame, text="⚙️ AYARLAR / REHBER", font=("Arial", 12, "bold"), bg="#333333", fg="white", width=18, command=self.yardim_penceresi)
        btn_ayarlar.pack(pady=12)

    def ses_durumu_degistir(self):
        """Sesleri kapatıp açan menü fonksiyonu."""
        self.ses_acik = not self.ses_acik
        metin = "🔊 SES EFFECTS: AÇIK" if self.ses_acik else "🔇 SES EFFECTS: KAPALI"
        renk = "#333333" if self.ses_acik else "#cc0000"
        self.btn_ses.config(text=metin, bg=renk)
        self.ses_cal(440, 100)

    def yardim_penceresi(self):
        """Ayarlar ve Rehber butonuna tıklandığında açılan bilgilendirme penceresi."""
        self.ses_cal(500, 100)
        pencere = tk.Toplevel(self.root)
        pencere.title("Ayarlar & Rehber")
        pencere.geometry("340x240")
        pencere.resizable(False, False)
        
        tk.Label(pencere, text="🎮 OYUN KONTROLLERİ", font=("Arial", 12, "bold")).pack(pady=10)
        
        # DÜZELTİLEN SATIR: Çift tırnak stringi içerisindeki çakışma giderildi
        rehber_metin = "• A / D veya Sol/Sağ Yön Tuşları: Şerit Değiştirme\n• W / S: Hızlanma ve Yavaşlama\n• [ \" ] Tuşu (Klavye üst sıra): Hile Konsolu"
        tk.Label(pencere, text=rehber_metin, justify="left", font=("Arial", 10)).pack(pady=5)
        
        tk.Label(pencere, text="💡 İpucu: Oyun esnasında konsola 'help' yazarak\ntüm gizli hile kodlarını listeleyebilirsiniz.", fg="darkblue", font=("Arial", 9, "italic")).pack(pady=10)

    def oyunu_baslat(self):
        """Giriş ekranını kapatıp oyun arabirimini ve döngüsünü başlatan ana tetikleyici."""
        self.ses_cal(600, 150)
        self.menu_frame.pack_forget()

        # Değişken Sıfırlamaları (Temizlik)
        self.skor = 0
        self.hiz = self.baslangic_hizi
        self.oyuncu_serit_idx = 1
        self.duraklatildi = False
        self.tanri_modu = False
        self.engeller = []
        self.serit_cizgileri = []

        # Üst Arayüz Paneli (Duraklat Butonu ve Canlı Skor)
        self.ust_panel = tk.Frame(self.root, bg="#111111")
        self.ust_panel.pack(fill="x")

        self.btn_duraklat = tk.Button(self.ust_panel, text="⏸️ Duraklat", font=("Arial", 10, "bold"), bg="#ff9900", fg="white", width=12, command=self.duraklat_tetikle)
        self.btn_duraklat.pack(side="left", padx=10, pady=5)

        self.skor_etiketi = tk.Label(self.ust_panel, text="🏆 Skor: 0", font=("Arial", 14, "bold"), bg="#111111", fg="#00ff66")
        self.skor_etiketi.pack(side="right", padx=20)

        # Grafik Çizim Ekranı (Canvas)
        self.canvas = tk.Canvas(self.root, width=self.genislik, height=self.yukseklik, bg="#333333", highlightthickness=0)
        self.canvas.pack()

        # Gizli Hile Konsolu Alt Paneli (Sadece `"` tuşuyla aktifleşir)
        self.konsol_aktif = False
        self.konsol_frame = tk.Frame(self.root, bg="black", height=130)
        self.konsol_output = tk.Text(self.konsol_frame, bg="black", fg="lightgreen", font=("Courier", 9), height=5, state="disabled")
        self.konsol_output.pack(fill="x", padx=5, pady=2)
        self.konsol_girdi = tk.Entry(self.konsol_frame, bg="#222222", fg="white", font=("Courier", 10), insertbackground="white")
        self.konsol_girdi.pack(fill="x", padx=5, pady=2)
        self.konsol_girdi.bind("<Return>", self.hile_calistir)

        # Klavye Olaylarını Dinleme
        self.root.bind("<KeyPress>", self.tus_basildi)

        # İlk Yol ve Oyuncu Çizimlerini Yap
        self.yolu_hazirla()
        self.oyuncu_araba_olustur()
        
        # Oyun Döngüsünü ve Trafiği Başlat
        self.oyun_aktif = True
        self.engel_uret()
        self.oyun_dongusu()

    def yolu_hazirla(self):
        """Yol sınır çizgilerini ve kesikli şeritleri Canvas'a basar."""
        self.canvas.create_line(30, 0, 30, self.yukseklik, fill="white", width=4)
        self.canvas.create_line(370, 0, 370, self.yukseklik, fill="white", width=4)
        for y in range(-40, self.yukseklik, 80):
            c1 = self.canvas.create_line(145, y, 145, y + 40, fill="yellow", width=3)
            c2 = self.canvas.create_line(255, y, 255, y + 40, fill="yellow", width=3)
            self.serit_cizgileri.extend([c1, c2])

    def oyuncu_araba_olustur(self):
        """Kırmızı yarış arabasını tekerlekleri ve camıyla detaylıca çizer."""
        x = self.seritler[self.oyuncu_serit_idx]
        y = self.yukseklik - 90
        
        self.araba_govde = self.canvas.create_rectangle(x-20, y, x+20, y+70, fill="#cc0000", outline="#880000", width=2)
        self.araba_cam = self.canvas.create_rectangle(x-15, y+15, x+15, y+35, fill="#aaddff", outline="")
        self.t1 = self.canvas.create_rectangle(x-25, y+5, x-20, y+20, fill="black")
        self.t2 = self.canvas.create_rectangle(x+20, y+5, x+25, y+20, fill="black")
        self.t3 = self.canvas.create_rectangle(x-25, y+50, x-20, y+65, fill="black")
        self.t4 = self.canvas.create_rectangle(x+20, y+50, x+25, y+65, fill="black")
        
        self.oyuncu_parcalari = [self.araba_govde, self.araba_cam, self.t1, self.t2, self.t3, self.t4]

    def oyuncu_araba_guncelle(self):
        """Arabanın tüm alt görsel parçalarını yeni şeride pürüzsüz kaydırır."""
        hedef_x = self.seritler[self.oyuncu_serit_idx]
        coords = self.canvas.coords(self.araba_govde)
        if not coords or len(coords) < 3: return
        su_anki_x = (coords[0] + coords[2]) / 2
        fark = hedef_x - su_anki_x
        for parca in self.oyuncu_parcalari:
            self.canvas.move(parca, fark, 0)

    def duraklat_tetikle(self):
        """Sol üstteki buton tıklandığında oyunu dondurur veya çözer."""
        if not self.oyun_aktif: return
        self.duraklatildi = not self.duraklatildi
        if self.duraklatildi:
            self.btn_duraklat.config(text="▶️ Devam Et", bg="#00cc44")
            self.ses_cal(350, 150)
        else:
            self.btn_duraklat.config(text="⏸️ Duraklat", bg="#ff9900")
            self.ses_cal(450, 150)
            self.oyun_dongusu()

    def tus_basildi(self, event):
        """Klavye basışlarını yakalayan ana girdi fonksiyonu."""
        tus = event.keysym.lower()

        # Konsol Tetikleme (Çift tırnak, tek tırnak veya é tuşu varyasyonları için)
        if event.char == '"' or tus in ['quoteright', 'dead_diaeresis', 'asterisk', 'acute']:
            self.konsol_toggle()
            return

        # Oyun duraklatılmışsa veya konsol açıksa sürüş tuşlarını kilitle
        if not self.oyun_aktif or self.duraklatildi or self.konsol_aktif:
            return

        if tus in ['a', 'left'] and self.oyuncu_serit_idx > 0:
            self.oyuncu_serit_idx -= 1
            self.oyuncu_araba_guncelle()
            self.ses_cal(700, 40)
        elif tus in ['d', 'right'] and self.oyuncu_serit_idx < 2:
            self.oyuncu_serit_idx += 1
            self.oyuncu_araba_guncelle()
            self.ses_cal(700, 40)
        elif tus in ['w', 'up'] and self.hiz < 22:
            self.hiz += 1.5
        elif tus in ['s', 'down'] and self.hiz > 5:
            self.hiz -= 1.5

    def konsol_toggle(self):
        """Hile panelini açarken oyunu durdurur, kapatırken ise oyunu devam ettirir."""
        if not self.oyun_aktif: return
        
        self.konsol_aktif = not self.konsol_aktif
        if self.konsol_aktif:
            self.duraklatildi = True
            self.btn_duraklat.config(text="⚙️ Konsol Açık", bg="#555555")
            self.konsol_frame.pack(fill="x", side="bottom")
            self.konsol_girdi.focus_set()
            self.konsol_yaz("--- GELİŞMİŞ HİLE KONSOLU AKTİF ---")
            self.konsol_yaz("Mevcut hile listesi ve kodlar için 'help' yazın.")
        else:
            self.konsol_frame.pack_forget()
            self.duraklatildi = False
            self.btn_duraklat.config(text="⏸️ Duraklat", bg="#ff9900")
            self.oyun_dongusu()

    def konsol_yaz(self, metin):
        self.konsol_output.config(state="normal")
        self.konsol_output.insert("end", metin + "\n")
        self.konsol_output.see("end")
        self.konsol_output.config(state="disabled")

    def hile_calistir(self, event):
        komut = self.konsol_girdi.get().strip().lower()
        self.konsol_girdi.delete(0, "end")
        
        if not komut: return
        self.konsol_yaz(f"> {komut}")

        if komut == "help":
            self.konsol_yaz("[help]  : Tüm hile komutlarını listeler.")
            self.konsol_yaz("[god]   : Ölümsüzlük (God Modu) açar. Araba altın rengi olur.")
            self.konsol_yaz("[score+]: Skora anında +500 puan ekler.")
            self.konsol_yaz("[slow]  : Trafiği en yavaş/başlangıç hızına çeker.")
            self.konsol_yaz("[clear] : O an ekranda görünen tüm aktif engelleri patlatır.")
            self.konsol_yaz("[exit]  : Konsolu kapatır激活 ve oyunu devam ettirir.")
        elif komut == "god":
            self.tanri_modu = not self.tanri_modu
            renk = "#ffcc00" if self.tanri_modu else "#cc0000"
            self.canvas.itemconfig(self.araba_govde, fill=renk)
            durum = "AKTİF" if self.tanri_modu else "KAPALI"
            self.konsol_yaz(f"🔮 Tanrı Modu Durumu: {durum}")
        elif komut == "score+":
            self.skor += 500
            self.skor_etiketi.config(text=f"🏆 Skor: {self.skor}")
            self.konsol_yaz("💰 +500 Skor puanı eklendi.")
        elif komut == "slow":
            self.hiz = self.baslangic_hizi
            self.konsol_yaz("🐢 Hız minimuma indirildi.")
        elif komut == "clear":
            for e in self.engeller:
                for parca in e["parcalar"]: self.canvas.delete(parca)
            self.engeller.clear()
            self.konsol_yaz("💥 Tüm trafik temizlendi!")
        elif komut == "exit":
            self.konsol_toggle()
        else:
            self.konsol_yaz("❌ Geçersiz kod! Listeyi görmek için 'help' yazın.")

    def engel_uret(self):
        if not self.oyun_aktif or self.duraklatildi:
            if self.oyun_aktif: self.root.after(1000, self.engel_uret)
            return

        serit_x = random.choice(self.seritler)
        y = -80
        e_govde = self.canvas.create_rectangle(serit_x-22, y, serit_x+22, y+60, fill="#1a5276", outline="#113355", width=2)
        e_kasa = self.canvas.create_rectangle(serit_x-18, y+5, serit_x+18, y+40, fill="#2980b9", outline="")
        
        self.engeller.append({"parcalar": [e_govde, e_kasa], "govde": e_govde})
        self.root.after(random.randint(1000, 2000), self.engel_uret)

    def oyun_dongusu(self):
        if self.oyun_aktif and not self.duraklatildi:
            # Yol Çizgilerini Aşağı Kaydır
            for cizgi in self.serit_cizgileri:
                self.canvas.move(cizgi, 0, self.hiz)
                if self.canvas.coords(cizgi)[1] >= self.yukseklik:
                    self.canvas.move(cizgi, 0, -(self.yukseklik + 40))

            # Engelleri Aşağı Kaydır
            oyuncu_coords = self.canvas.coords(self.araba_govde)
            silinecekler = []

            for engel in self.engeller:
                for parca in engel["parcalar"]:
                    self.canvas.move(parca, 0, self.hiz)
                
                engel_coords = self.canvas.coords(engel["govde"])

                if engel_coords[1] >= self.yukseklik:
                    silinecekler.append(engel)
                    self.skor += 10
                    self.skor_etiketi.config(text=f"🏆 Skor: {self.skor}")
                    self.ses_cal(1000, 25)
                    if self.skor % 100 == 0: self.hiz += 0.5

                # Gelişmiş Kutu Çarpışma Testi (AABB)
                if not self.tanri_modu and oyuncu_coords and engel_coords:
                    if (oyuncu_coords[0] < engel_coords[2] and oyuncu_coords[2] > engel_coords[0] and
                        oyuncu_coords[1] < engel_coords[3] and oyuncu_coords[3] > engel_coords[1]):
                        self.oyun_bitti_ekrani()
                        return

            for e in silinecekler:
                for parca in e["parcalar"]: self.canvas.delete(parca)
                self.engeller.remove(e)

            self.root.after(16, self.oyun_dongusu)

    def oyun_bitti_ekrani(self):
        """Kaza gerçekleştiğinde oyunu bitiren ve Yeniden Dene seçeneği sunan ekran."""
        self.oyun_aktif = False
        self.skoru_kaydet()
        self.skorlari_yukle()  # Değerleri ana menü için tazele
        self.ses_cal(140, 650)
        
        # Ekranın ortasına bitiş paneli yerleştir
        self.canvas.create_rectangle(50, 180, 350, 420, fill="#111111", outline="white", width=2)
        self.canvas.create_text(200, 220, text="💥 KAZA YAPTINIZ! 💥", font=("Arial", 20, "bold"), fill="red")
        self.canvas.create_text(200, 270, text=f"Skorunuz: {self.skor}", font=("Arial", 16, "bold"), fill="white")
        
        # Yeniden Dene Butonu (Doğrudan ana menüye döner)
        self.btn_yeniden_dene = tk.Button(self.root, text="🔄 Yeniden Dene (Menü)", font=("Arial", 12, "bold"), bg="#00cc44", fg="white", command=self.menuye_don)
        self.canvas.create_window(200, 350, window=self.btn_yeniden_dene)

    def menuye_don(self):
        """Tüm mevcut oyun arayüzünü temizler ve güncel skorlarla ana menüyü yeniden basar."""
        self.ses_cal(500, 100)
        
        # Üst paneli ve canvası yok et
        if hasattr(self, 'ust_panel'): self.ust_panel.destroy()
        if hasattr(self, 'canvas'): self.canvas.destroy()
        if hasattr(self, 'konsol_frame'): self.konsol_frame.destroy()
        
        # Ana Menüyü Yeniden Yükle
        self.ana_menu_olustur()

if __name__ == "__main__":
    pencere = tk.Tk()
    oyun = ArabaYarisiGelisimis(pencere)
    pencere.mainloop()