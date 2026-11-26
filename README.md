🎬 Hoca Studio FaceSwapper

Hoca Studio FaceSwapper, PySide6 tabanlı modern ve koyu temalı bir arayüz ile yerel FaceFusion ve FFmpeg altyapısını birleştiren profesyonel bir AI yüz değiştirme (Face Swap) masaüstü uygulamasıdır.

🚀 Öne Çıkan Özellikler

🌙 Modern Koyu Tema Arayüzü: Göz yormayan, şık ve kullanıcı dostu panel tasarımı.

📁 Çoklu Referans Fotoğraf Desteği: Farklı açılardan çekilmiş birden fazla fotoğraf seçerek çok daha kaliteli ve doğal sonuçlar elde edin.

🖱️ Sürükle-Bırak Desteği: Hedef videoları ve müzik dosyalarını arayüze kolayca sürükleyip bırakın.

✨ Sihirli Komutlar (Prompt): Tek bir komutla yaşlandırma, renk filtreleri (esmer/bronz yap, siyah-beyaz) veya ayna efektleri uygulayın.

📊 Canlı Takip ve ETA: Anlık ilerleme çubuğu, yüzde göstergesi ve dinamik kalan süre (ETA) hesaplaması.

⚡ Parçalı İşlem Mimarisi: Büyük videoları küçük parçalara (chunk) bölerek yüksek stabilite ve verimlilik sağlar.

🛠️ Proje Mimarisi

main.py - Uygulamanın ana giriş noktası ve pencere yöneticisi.

ui/main_window.py - PySide6 tabanlı arayüz bileşenleri ve kullanıcı etkileşimleri.

ui/worker.py - Arayüzün donmasını önleyen arka plan iş parçacığı (QThread) ve FaceFusion komut yöneticisi.

core/process_runner.py - Harici süreçleri güvenli şekilde çalıştıran alt süreç sarmalayıcısı.

core/video_utils.py - FFmpeg/FFprobe tabanlı video bölme, birleştirme, ses ekleme ve filtreleme modülü.

⚙️ Kurulum ve Çalıştırma

1. Depoyu Klonlayın

git clone https://github.com/BiggerSon/HocaSwap.git
cd HocaSwap


2. Bağımlılıkları Yükleyin

pip install -r requirements.txt


3. Konfigürasyon (config.py)

Ana dizinde config.py dosyası oluşturarak kendi FaceFusion ve Python yollarınızı tanımlayın:

FACEFUSION_PYTHON = r"Kendi_Python_Yolunuz/python.exe"
FACEFUSION_SCRIPT = r"Kendi_FaceFusion_Yolunuz/facefusion.py"
FACEFUSION_CWD = r"Kendi_FaceFusion_Klasorunuz"


4. Uygulamayı Başlatın

python main.py


💻 Kullanılan Teknolojiler

Python

PySide6 (Qt for Python)

FaceFusion
