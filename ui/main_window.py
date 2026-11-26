import os

from PySide6.QtWidgets import (
    QComboBox, QFileDialog, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMessageBox, QProgressBar, QPushButton,
    QTextEdit, QVBoxLayout, QWidget,
)

from ui.worker import VideoProcessingWorker


class DropLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            self.setText(files[0])


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hoca Studio FaceSwapper")
        self.resize(920, 820)
        self.setStyleSheet(self._stylesheet())

        self.worker: VideoProcessingWorker | None = None
        self.image_paths: list[str] = []

        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(16)
        layout.setContentsMargins(30, 30, 30, 30)
        title = QLabel("Hoca Studio FaceSwapper")
        title.setObjectName("title")
        layout.addWidget(title)
        layout.addWidget(self._build_file_panel())
        layout.addWidget(self._build_settings_panel())
        btn_row = QHBoxLayout()
        self.start_button = QPushButton("🚀 İşlemi Başlat")
        self.start_button.setObjectName("start_btn")
        self.start_button.clicked.connect(self._on_start_clicked)
        self.cancel_button = QPushButton("İptal")
        self.cancel_button.setObjectName("cancel_btn")
        self.cancel_button.clicked.connect(self._on_cancel_clicked)
        self.cancel_button.setEnabled(False)
        btn_row.addWidget(self.start_button)
        btn_row.addWidget(self.cancel_button)
        layout.addLayout(btn_row)
        prog_row = QHBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.status_label = QLabel("Hazır")
        self.status_label.setObjectName("status_label")
        prog_row.addWidget(self.progress_bar, stretch=1)
        prog_row.addWidget(self.status_label)
        layout.addLayout(prog_row)
        log_label = QLabel("Log")
        layout.addWidget(log_label)
        self.log_text_edit = QTextEdit()
        self.log_text_edit.setReadOnly(True)
        layout.addWidget(self.log_text_edit, stretch=1)

    def _build_file_panel(self) -> QWidget:
        panel = QWidget()
        panel.setObjectName("panel")
        panel_layout = QVBoxLayout(panel)
        img_row = QHBoxLayout()
        img_label = QLabel("Referans Fotoğraf(lar):")
        img_label.setFixedWidth(170)
        self.img_path_edit = QLineEdit()
        self.img_path_edit.setReadOnly(True)
        self.img_path_edit.setPlaceholderText("Çoklu fotoğraf seç (farklı açılar daha iyi sonuç verir)")
        img_btn = QPushButton("Seç...")
        img_btn.clicked.connect(self._browse_images)
        img_row.addWidget(img_label)
        img_row.addWidget(self.img_path_edit)
        img_row.addWidget(img_btn)
        panel_layout.addLayout(img_row)
        vid_row = QHBoxLayout()
        vid_label = QLabel("Hedef Video:")
        vid_label.setFixedWidth(170)
        self.vid_path_edit = DropLineEdit()
        self.vid_path_edit.setPlaceholderText("Sürükle-bırak veya Seç...")
        vid_btn = QPushButton("Seç...")
        vid_btn.clicked.connect(self._browse_video)
        vid_row.addWidget(vid_label)
        vid_row.addWidget(self.vid_path_edit)
        vid_row.addWidget(vid_btn)
        panel_layout.addLayout(vid_row)
        audio_row = QHBoxLayout()
        audio_label = QLabel("Yeni Müzik (Opsiyonel):")
        audio_label.setFixedWidth(170)
        self.audio_path_edit = DropLineEdit()
        self.audio_path_edit.setPlaceholderText("Boş bırakılırsa orijinal ses korunur")
        audio_btn = QPushButton("Seç...")
        audio_btn.clicked.connect(self._browse_audio)
        audio_row.addWidget(audio_label)
        audio_row.addWidget(self.audio_path_edit)
        audio_row.addWidget(audio_btn)
        panel_layout.addLayout(audio_row)
        out_row = QHBoxLayout()
        out_label = QLabel("Çıktı Dosyası:")
        out_label.setFixedWidth(170)
        self.out_path_edit = QLineEdit()
        self.out_path_edit.setReadOnly(True)
        out_btn = QPushButton("Seç...")
        out_btn.clicked.connect(self._browse_output)
        out_row.addWidget(out_label)
        out_row.addWidget(self.out_path_edit)
        out_row.addWidget(out_btn)
        panel_layout.addLayout(out_row)

        return panel

    def _build_settings_panel(self) -> QWidget:
        panel = QWidget()
        panel.setObjectName("panel")
        panel_layout = QVBoxLayout(panel)

        prompt_row = QHBoxLayout()
        prompt_label = QLabel("Sihirli Komut:")
        prompt_label.setFixedWidth(170)
        self.prompt_edit = QLineEdit()
        self.prompt_edit.setPlaceholderText("Örn: 'esmer yap', 'siyah beyaz yap', 'ayna yap', 'yaşlandır'...")
        prompt_row.addWidget(prompt_label)
        prompt_row.addWidget(self.prompt_edit)
        panel_layout.addLayout(prompt_row)

        opt_row = QHBoxLayout()
        opt_row.addWidget(QLabel("Yüz Seçimi:"))
        self.face_mode_combo = QComboBox()
        self.face_mode_combo.addItems(["Tüm Yüzler", "Sadece En Büyük Yüz"])
        opt_row.addWidget(self.face_mode_combo)

        opt_row.addWidget(QLabel("   Kalite:"))
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["Hizli", "Dengeli", "Yuksek"])
        self.quality_combo.setCurrentText("Dengeli")
        opt_row.addWidget(self.quality_combo)
        opt_row.addStretch(1)

        panel_layout.addLayout(opt_row)
        return panel

    def _browse_images(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Referans Fotoğraf(lar) Seç", "", "Görseller (*.jpg *.jpeg *.png)"
        )
        if paths:
            self.image_paths = paths
            if len(paths) == 1:
                self.img_path_edit.setText(paths[0])
            else:
                self.img_path_edit.setText(f"{len(paths)} adet fotoğraf seçildi.")

    def _browse_video(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Hedef Video Seç", "", "Videolar (*.mp4 *.mov *.mkv *.avi)"
        )
        if path:
            self.vid_path_edit.setText(path)

    def _browse_audio(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Müzik Seç", "", "Ses Dosyaları (*.mp3 *.wav *.m4a)"
        )
        if path:
            self.audio_path_edit.setText(path)

    def _browse_output(self):
        path, _ = QFileDialog.getSaveFileName(self, "Çıktı Dosyasını Seç", "", "MP4 Video (*.mp4)")
        if path:
            if not path.lower().endswith(".mp4"):
                path += ".mp4"
            self.out_path_edit.setText(path)

    def _on_start_clicked(self):
        video_path = self.vid_path_edit.text().strip()
        output_path = self.out_path_edit.text().strip()
        audio_path = self.audio_path_edit.text().strip()
        quality = self.quality_combo.currentText()
        prompt = self.prompt_edit.text().strip()
        face_mode = "one" if self.face_mode_combo.currentText() == "Sadece En Büyük Yüz" else "many"

        missing = []
        if not self.image_paths:
            missing.append("Referans fotoğraf(lar)")
        if not video_path or not os.path.isfile(video_path):
            missing.append("Hedef video (dosya bulunamadı)")
        if not output_path:
            missing.append("Çıktı dosyası yolu")

        if missing:
            QMessageBox.warning(self, "Eksik Bilgi", "Eksik/geçersiz alanlar:\n- " + "\n- ".join(missing))
            return

        self._set_busy_state(True)
        self.log_text_edit.clear()
        self.progress_bar.setValue(0)
        self.status_label.setText("Başlatılıyor...")

        self.worker = VideoProcessingWorker(
            image_paths=self.image_paths,
            video_path=video_path,
            audio_path=audio_path,
            quality_label=quality,
            output_path=output_path,
            prompt_text=prompt,
            face_mode=face_mode,
            chunk_seconds=30,
        )
        self.worker.log_signal.connect(self._append_log)
        self.worker.progress_signal.connect(self.progress_bar.setValue)
        self.worker.status_signal.connect(self.status_label.setText)
        self.worker.finished_signal.connect(self._on_worker_finished)
        self.worker.start()

    def _on_cancel_clicked(self):
        if self.worker and self.worker.isRunning():
            self._append_log("İptal isteği gönderildi, bekleniyor...")
            self.worker.request_cancel()
            self.cancel_button.setEnabled(False)

    def _on_worker_finished(self, success: bool, message: str):
        self._set_busy_state(False)
        if success:
            self._append_log(f"BAŞARILI: {message}")
            self.status_label.setText("Tamamlandı")
            QMessageBox.information(self, "Tamamlandı", f"Video başarıyla kaydedildi:\n{message}")
        else:
            self._append_log(f"HATA: {message}")
            self.status_label.setText("Hata oluştu")
            QMessageBox.critical(self, "Hata", message)

    def _set_busy_state(self, busy: bool):
        self.start_button.setEnabled(not busy)
        self.cancel_button.setEnabled(busy)
        self.img_path_edit.setEnabled(not busy)
        self.vid_path_edit.setEnabled(not busy)
        self.audio_path_edit.setEnabled(not busy)
        self.out_path_edit.setEnabled(not busy)
        self.prompt_edit.setEnabled(not busy)
        self.quality_combo.setEnabled(not busy)
        self.face_mode_combo.setEnabled(not busy)

    def _append_log(self, text: str):
        self.log_text_edit.append(text)
        scrollbar = self.log_text_edit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def closeEvent(self, event):
        if self.worker and self.worker.isRunning():
            self.worker.request_cancel()
            self.worker.wait(3000)
        event.accept()


    @staticmethod
    def _stylesheet() -> str:
        return """
        QMainWindow { background-color: #0D0D0D; }
        QWidget#panel { background-color: #1A1A1A; border-radius: 12px; padding: 16px; }
        QLabel { color: #E0E0E0; font-family: 'Segoe UI'; font-size: 13px; }
        QLabel#title { font-size: 24px; font-weight: bold; color: #FFFFFF; margin-bottom: 4px; }
        QLabel#status_label { font-weight: bold; color: #FFC107; font-size: 14px; padding-left: 10px; }

        QLineEdit, QComboBox, QTextEdit {
            background-color: #2D2D2D; color: #FFFFFF;
            border: 1px solid #3D3D3D; border-radius: 8px;
            padding: 8px; font-family: 'Segoe UI'; font-size: 13px;
        }
        QLineEdit:focus, QComboBox:focus { border: 1px solid #4CAF50; }

        QPushButton {
            background-color: #333333; color: white;
            border: none; border-radius: 8px; padding: 8px 16px;
            font-family: 'Segoe UI'; font-weight: bold;
        }
        QPushButton:hover { background-color: #444444; }
        QPushButton:disabled { background-color: #222222; color: #777777; }

        QPushButton#start_btn { background-color: #4CAF50; font-size: 15px; padding: 12px; }
        QPushButton#start_btn:hover { background-color: #45A049; }
        QPushButton#start_btn:disabled { background-color: #2E4F30; color: #8FAF90; }

        QPushButton#cancel_btn { background-color: #F44336; }
        QPushButton#cancel_btn:hover { background-color: #D32F2F; }

        QProgressBar {
            background-color: #2D2D2D; border: 1px solid #3D3D3D; border-radius: 8px;
            text-align: center; color: white; font-weight: bold; height: 22px;
        }
        QProgressBar::chunk { background-color: #2196F3; border-radius: 7px; }
        """