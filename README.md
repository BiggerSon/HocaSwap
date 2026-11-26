# 🎬 HocaSwap — Yapay Zekâ Destekli Yüz Değiştirme ve Video İşleme

<p align="center">
  <strong>Python ve FaceFusion altyapısıyla geliştirilmiş modern bir masaüstü uygulaması.</strong>
  <br>
  Yapay zekâ destekli yüz değiştirme, video işleme ve medya düzenleme işlemlerini tek bir arayüzde birleştirir.
</p>

---

## ⚠️ SORUMLULUK VE KULLANIM KOŞULLARI

**Lütfen yazılımı kullanmadan önce bu bölümü dikkatlice okuyun.**

1. **Yasal Kullanım:** HocaSwap, eğitim, araştırma ve izinli medya düzenleme işlemleri için geliştirilmiştir.
2. **İzin ve Rıza:** Başka kişilere ait fotoğraf, video veya ses kayıtlarını kullanmadan önce gerekli izinlerin alınması kullanıcının sorumluluğundadır.
3. **Kötüye Kullanım:** Yazılımın dolandırıcılık, kimlik taklidi, yanıltıcı içerik üretimi veya kişilerin rızası dışında görüntülerinin değiştirilmesi amacıyla kullanılması uygun değildir.
4. **Kullanıcı Sorumluluğu:** Oluşturulan içeriklerin kullanımından ve paylaşılmasından kullanıcı sorumludur.
5. **Şeffaflık:** Yapay zekâ ile değiştirilmiş içeriklerin gerektiğinde açıkça belirtilmesi önerilir.

---

## 📌 PROJE HAKKINDA

**HocaSwap**, yapay zekâ teknolojilerini kullanarak fotoğraf ve videolarda yüz değiştirme işlemlerini kolaylaştırmak amacıyla geliştirilmiş bir masaüstü uygulamasıdır.

Proje, FaceFusion'ın güçlü yüz değiştirme altyapısını modern ve kullanıcı dostu bir grafik arayüzüyle bir araya getirir. Kullanıcıların karmaşık komutlarla uğraşmadan fotoğraf ve video işlemlerini gerçekleştirebilmesini hedefler.

HocaSwap yalnızca yüz değiştirme işlemiyle sınırlı değildir. FFmpeg entegrasyonu sayesinde video parçalama, birleştirme, ses işlemleri ve çeşitli medya düzenleme süreçlerini de destekleyen bir çalışma ortamı sunar.

Uygulama, özellikle uzun videoların işlenmesini daha yönetilebilir hâle getirmek ve bütün işlemleri tek bir arayüz üzerinden kontrol edebilmek için tasarlanmıştır.

---

## ✨ ÖZELLİKLER

| Özellik | Açıklama |
|:---|:---|
| 🤖 **Yapay Zekâ ile Yüz Değiştirme** | FaceFusion altyapısıyla yüz değiştirme işlemleri. |
| 🖼️ **Çoklu Referans Fotoğrafı** | Birden fazla referans fotoğrafıyla çalışma. |
| 🎥 **Video İşleme** | Video dosyalarında yüz değiştirme. |
| 🌙 **Modern Arayüz** | PySide6 ile hazırlanmış karanlık ve sade tasarım. |
| 🖱️ **Sürükle ve Bırak** | Medya dosyalarını kolayca uygulamaya ekleme. |
| ⚡ **Parçalı Video İşleme** | Büyük videoları daha küçük parçalara ayırarak işleme. |
| 🔗 **Video Birleştirme** | İşlenen parçaları yeniden birleştirme. |
| 🎵 **Ses Entegrasyonu** | Video ve ses dosyaları üzerinde işlemler gerçekleştirme. |
| 📊 **İlerleme Takibi** | İşlem yüzdesini ve tahmini kalan süreyi görüntüleme. |
| 📋 **Canlı İşlem Kayıtları** | Arka planda gerçekleşen işlemleri takip etme. |
| ⚙️ **Arka Plan İşlemleri** | Uzun süren işlemler sırasında arayüzün yanıt vermeye devam etmesi. |
| 🎨 **Magic Commands** | Desteklenen komutlarla çeşitli görsel efektler uygulama. |

---

## 🖥️ KULLANILAN TEKNOLOJİLER

HocaSwap, farklı teknolojileri bir araya getirerek güçlü ve modüler bir medya işleme ortamı oluşturur.

| Teknoloji | Kullanım Amacı |
|:---|:---|
| **Python** | Ana programlama dili |
| **PySide6** | Masaüstü grafik arayüzü |
| **FaceFusion** | Yapay zekâ ile yüz değiştirme |
| **FFmpeg** | Video ve ses işleme |
| **FFprobe** | Medya dosyalarını analiz etme |
| **QThread** | Arka plan işlemlerini yönetme |

---

## 🎨 MAGIC COMMANDS

HocaSwap içerisinde desteklenen bazı görsel efektler için metin tabanlı komut sistemi bulunmaktadır.

Bu sistem sayesinde kullanıcılar belirli efektleri komutlar aracılığıyla uygulayabilir.

**Örnek efekt kategorileri:**

- Yaşlandırma efektleri
- Renk ve ton düzenlemeleri
- Siyah-beyaz filtreler
- Ayna efektleri

Kullanılabilen komutlar, uygulamanın mevcut sürümünde desteklenen işlemlere bağlıdır.

---

## ⚙️ ÇALIŞMA MANTIĞI

HocaSwap, farklı teknolojileri tek bir çalışma akışında birleştirir.

```text
       KULLANICI
           |
           ▼
     PySide6 Arayüzü
           |
           ▼
      Worker Thread
           |
           ▼
      Process Runner
           |
           ▼
      FaceFusion
           |
           ▼
      FFmpeg / FFprobe
           |
           ▼
     İŞLENMİŞ MEDYA
```

**İşlem adımları:**

1. Kullanıcı değiştirmek istediği yüzün bulunduğu referans fotoğraflarını seçer.
2. Hedef video veya medya dosyasını uygulamaya ekler.
3. İlgili işlem ayarlarını yapılandırır.
4. Uygulama, FaceFusion altyapısını kullanarak yüz değiştirme işlemini başlatır.
5. Uzun videolar gerektiğinde parçalara ayrılarak işlenir.
6. FFmpeg kullanılarak gerekli video ve ses işlemleri gerçekleştirilir.
7. İşlem tamamlandığında çıktı dosyası oluşturulur.

---

## 📂 PROJE YAPISI

```text
HocaSwap/
│
├── core/
│   ├── process_runner.py
│   └── video_utils.py
│
├── ui/
│   ├── main_window.py
│   └── worker.py
│
├── main.py
├── requirements.txt
├── config.py
└── README.md
```

**Temel dosyaların görevleri:**

| Dosya | Açıklama |
|:---|:---|
| `main.py` | Uygulamanın başlangıç noktası. |
| `ui/main_window.py` | Ana kullanıcı arayüzü. |
| `ui/worker.py` | Arka plan işlemlerini yönetir. |
| `core/process_runner.py` | Harici programların çalıştırılmasını yönetir. |
| `core/video_utils.py` | Video parçalama, birleştirme ve ses işlemlerini gerçekleştirir. |
| `requirements.txt` | Python bağımlılıklarını içerir. |
| `config.py` | FaceFusion kurulumuna ait yapılandırma bilgilerini tutar. |

---

## 📥 KURULUM

HocaSwap'ı bilgisayarınızda çalıştırmak için aşağıdaki adımları takip edebilirsiniz.

### 1. Gereksinimler

Kuruluma başlamadan önce aşağıdaki yazılımların bilgisayarınızda bulunması gerekir:

- Python 3.10 veya üzeri
- Git
- FFmpeg
- FFprobe
- FaceFusion
- FaceFusion'ın gerektirdiği donanım ve Python bağımlılıkları

### 2. Depoyu Klonlayın

Öncelikle GitHub deposunu bilgisayarınıza indirin:

```bash
git clone https://github.com/BiggerSon/HocaSwap.git
```

Proje klasörüne girin:

```bash
cd HocaSwap
```

### 3. Sanal Ortam Oluşturun

Python bağımlılıklarını diğer projelerden izole etmek için sanal ortam oluşturun:

```bash
python -m venv .venv
```

Windows üzerinde sanal ortamı etkinleştirin:

```powershell
.venv\Scripts\activate
```

### 4. Gerekli Kütüphaneleri Yükleyin

Öncelikle pip paket yöneticisini güncelleyin:

```bash
python -m pip install --upgrade pip
```

Ardından proje bağımlılıklarını yükleyin:

```bash
pip install -r requirements.txt
```

### 5. FaceFusion Yapılandırması

HocaSwap'ın yüz değiştirme işlemlerini gerçekleştirebilmesi için bilgisayarınızda çalışan bir FaceFusion kurulumu bulunmalıdır.

Proje ana dizininde `config.py` dosyasını oluşturun ve FaceFusion kurulumunuza uygun yolları tanımlayın:

```python
FACEFUSION_PYTHON = r"C:\FaceFusion\python.exe"

FACEFUSION_SCRIPT = r"C:\FaceFusion\facefusion.py"

FACEFUSION_CWD = r"C:\FaceFusion"
```

> **Önemli:** Yukarıdaki yollar örnektir. Kendi FaceFusion kurulumunuzun bulunduğu dizinlere göre değiştirilmelidir.

### 6. FFmpeg Kurulumu

FFmpeg ve FFprobe araçlarının bilgisayarınızda kurulu olması gerekir.

Kurulumdan sonra FFmpeg'in `bin` klasörünü Windows PATH değişkenine ekleyin.

Kurulumun başarılı olduğunu kontrol etmek için terminalde şu komutları çalıştırın:

```bash
ffmpeg -version
```

```bash
ffprobe -version
```

Her iki komut da sürüm bilgisi döndürüyorsa kurulum tamamlanmıştır.

### 7. Uygulamayı Başlatın

Bütün kurulum adımları tamamlandıktan sonra HocaSwap'ı çalıştırabilirsiniz:

```bash
python main.py
```

Uygulamanın grafik arayüzü açılacaktır.

---

## 🤝 KATKIDA BULUNMA

HocaSwap açık kaynak geliştirme yaklaşımını benimser. Projeye katkıda bulunmak, hata bildirmek veya yeni özellik önermek isteyen herkes katkı sağlayabilir.

Katkıda bulunmak için:

1. Bu depoyu Fork edin.
2. Yeni bir geliştirme dalı oluşturun.
3. Değişikliklerinizi gerçekleştirin.
4. Gerekli testleri yapın.
5. Pull Request gönderin.

Hata bildirmek veya öneride bulunmak için:

**[GitHub Issues](https://github.com/BiggerSon/HocaSwap/issues)**

---


  Geliştirici: <a href="https://github.com/BiggerSon">BiggerSon</a>
  <br><br>
  <sub>Python ile ❤️ geliştirildi.</sub>
</p>
