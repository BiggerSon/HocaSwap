🎬 HocaSwap

<p align="center">
  **Yapay Zekâ Destekli Yüz Değiştirme ve Video İşleme Uygulaması**
  <br>
  Python ve FaceFusion altyapısıyla geliştirilmiş masaüstü uygulaması.
</p>

⚠️ Sorumluluk ve Kullanım

HocaSwap, izinli ve yasal medya düzenleme işlemleri için geliştirilmiştir.

Başka kişilere ait fotoğraf, video veya ses kayıtlarını kullanmadan önce gerekli izinlerin alınması kullanıcıların sorumluluğundadır.

Uygulamanın kişileri yanıltmak, taklit etmek, dolandırıcılık yapmak veya rızaya aykırı içerik üretmek amacıyla kullanılması uygun değildir.

Yapay zekâ ile değiştirilmiş içeriklerin gerektiğinde açıkça belirtilmesi önerilir.

📌 Proje Hakkında

HocaSwap, yapay zekâ teknolojilerini kullanarak fotoğraf ve videolarda yüz değiştirme işlemlerini kolaylaştırmak amacıyla geliştirilmiş bir masaüstü uygulamasıdır.

Proje, FaceFusion'ın güçlü yüz değiştirme altyapısını modern ve kullanıcı dostu bir grafik arayüzüyle bir araya getirir. Kullanıcıların karmaşık komutlarla uğraşmadan fotoğraf ve video işlemlerini gerçekleştirebilmesini hedefler.

HocaSwap yalnızca yüz değiştirme işlemiyle sınırlı değildir. FFmpeg entegrasyonu sayesinde video parçalama, birleştirme, ses işlemleri ve çeşitli medya düzenleme süreçlerini de destekleyen bir çalışma ortamı sunar.

Uygulama, özellikle uzun videoların işlenmesini daha yönetilebilir hâle getirmek ve bütün işlemleri tek bir arayüz üzerinden kontrol edebilmek için tasarlanmıştır.

✨ Özellikler

Yapay Zekâ ile Yüz Değiştirme: FaceFusion altyapısıyla yüz değiştirme işlemleri.

Çoklu Referans Fotoğrafı: Birden fazla referans fotoğrafıyla çalışma.

Video İşleme: Video dosyalarında yüz değiştirme.

Modern Arayüz: PySide6 ile hazırlanmış karanlık ve sade tasarım.

Sürükle ve Bırak: Medya dosyalarını kolayca uygulamaya ekleme.

Parçalı Video İşleme: Büyük videoları daha küçük parçalara ayırarak işleme.

Video Birleştirme: İşlenen parçaları yeniden birleştirme.

Ses Entegrasyonu: Video ve ses dosyaları üzerinde işlemler gerçekleştirme.

İlerleme Takibi: İşlem yüzdesini ve tahmini kalan süreyi görüntüleme.

Canlı İşlem Kayıtları: Arka planda gerçekleşen işlemleri takip etme.

Arka Plan İşlemleri: Uzun süren işlemler sırasında arayüzün yanıt vermeye devam etmesi.

Magic Commands: Desteklenen komutlarla çeşitli görsel efektler uygulama.

🖥️ Kullanılan Teknolojiler

Teknoloji

Kullanım Amacı

Python

Ana programlama dili

PySide6

Masaüstü arayüzü

FaceFusion

Yapay zekâ ile yüz değiştirme

FFmpeg

Video ve ses işleme

FFprobe

Medya dosyalarını analiz etme

QThread

Arka plan işlemlerini yönetme

🎨 Magic Commands

HocaSwap içerisinde desteklenen bazı görsel efektler için metin tabanlı komut sistemi bulunmaktadır.

Bu sistem sayesinde kullanıcılar belirli efektleri komutlar aracılığıyla uygulayabilir.

Örnek efekt kategorileri:

Yaşlandırma efektleri

Renk ve ton düzenlemeleri

Siyah-beyaz filtreler

Ayna efektleri

⚙️ Çalışma Mantığı

HocaSwap, farklı teknolojileri tek bir çalışma akışında birleştirir.

Kullanıcı değiştirmek istediği yüzün bulunduğu referans fotoğraflarını seçer.

Hedef video veya medya dosyasını uygulamaya ekler.

İlgili işlem ayarlarını yapılandırır.

Uygulama, FaceFusion altyapısını kullanarak yüz değiştirme işlemini başlatır.

Uzun videolar gerektiğinde parçalara ayrılarak işlenir.

FFmpeg kullanılarak gerekli video ve ses işlemleri gerçekleştirilir.

İşlem tamamlandığında çıktı dosyası oluşturulur.

📂 Proje Yapısı

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

Temel dosyalar:

main.py: Uygulamanın başlangıç noktası.

ui/main_window.py: Ana kullanıcı arayüzü.

ui/worker.py: Arka plan işlemlerini yönetir.

core/process_runner.py: Harici programların çalıştırılmasını yönetir.

core/video_utils.py: Video parçalama, birleştirme ve ses işlemlerini gerçekleştirir.

requirements.txt: Python bağımlılıklarını içerir.

config.py: FaceFusion kurulumuna ait yapılandırma bilgilerini tutar.

📥 Kurulum

HocaSwap'ı bilgisayarınızda çalıştırmak için aşağıdaki adımları takip edebilirsiniz.

1. Gereksinimler

Kuruluma başlamadan önce aşağıdaki yazılımların bilgisayarınızda bulunması gerekir:

Python 3.10 veya üzeri

Git

FFmpeg

FFprobe

FaceFusion

FaceFusion'ın gerektirdiği donanım ve Python bağımlılıkları

2. Projeyi İndirin

Öncelikle GitHub deposunu bilgisayarınıza klonlayın:

git clone https://github.com/BiggerSon/HocaSwap.git

Proje klasörüne girin:

cd HocaSwap

3. Sanal Ortam Oluşturun

Python bağımlılıklarını diğer projelerden izole etmek için sanal ortam oluşturun:

python -m venv .venv

Windows üzerinde sanal ortamı etkinleştirin:

.venv\Scripts\activate

4. Gerekli Kütüphaneleri Yükleyin

Öncelikle pip paket yöneticisini güncelleyin:

python -m pip install --upgrade pip

Ardından proje bağımlılıklarını yükleyin:

pip install -r requirements.txt

5. FaceFusion Yapılandırması

HocaSwap'ın yüz değiştirme işlemlerini gerçekleştirebilmesi için bilgisayarınızda çalışan bir FaceFusion kurulumu bulunmalıdır.

Proje ana dizininde config.py dosyasını oluşturun ve FaceFusion kurulumunuza uygun yolları tanımlayın:

FACEFUSION_PYTHON = r"C:\FaceFusion\python.exe"

FACEFUSION_SCRIPT = r"C:\FaceFusion\facefusion.py"

FACEFUSION_CWD = r"C:\FaceFusion"

Önemli: Yukarıdaki yollar örnektir. Kendi FaceFusion kurulumunuzun bulunduğu dizinlere göre değiştirilmelidir.

6. FFmpeg Kurulumu

FFmpeg ve FFprobe araçlarının bilgisayarınızda kurulu olması gerekir.

Kurulumdan sonra Windows PATH değişkenine FFmpeg'in bin klasörünü ekleyin.

Kurulumun başarılı olduğunu kontrol etmek için terminalde şu komutları çalıştırın:

ffmpeg -version

ffprobe -version

Her iki komut da sürüm bilgisi döndürüyorsa kurulum tamamlanmıştır.

7. Uygulamayı Başlatın

Bütün kurulum adımları tamamlandıktan sonra HocaSwap'ı çalıştırabilirsiniz:

python main.py

Uygulamanın grafik arayüzü açılacaktır.
