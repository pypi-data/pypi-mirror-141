import os
import shutil
import tempfile
from datetime import datetime
import unicodedata

import cv2
import numpy as np

from AnyQt.QtCore import Qt, QTimer, QSize
from AnyQt.QtWidgets import QLabel, QPushButton, QSizePolicy
from AnyQt.QtGui import QImage, QPixmap, QImageReader

from Orange.data import Table, Domain, StringVariable, ContinuousVariable
from Orange.widgets import gui, widget, settings


face_cascade_classifier = cv2.CascadeClassifier(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data',
                 'haarcascade_frontalface_default.xml'))


class OWNWebcamCapture(widget.OWWidget):
    name = "Webcam Capture"
    description = "Capture a still image using the first detected webcam."
    icon = "icons/WebcamCapture.svg"

    class Output:
        SNAPSHOT = 'Snapshot'
        SNAPSHOT_ASPECT = 'Snapshot (1:1)'

    outputs = [
        (Output.SNAPSHOT, Table),
        (Output.SNAPSHOT_ASPECT, Table),
    ]

    want_main_area = False

    avatar_filter = settings.Setting(False)
    image_title = ''

    DEFAULT_TITLE = 'Snapshot'

    class Error(widget.OWWidget.Error):
        no_webcam = widget.Msg("Couldn't acquire webcam")

    def __init__(self):
        super().__init__()
        self.cap = None
        self.snapshot_flash = 0
        self.IMAGE_DIR = tempfile.mkdtemp(prefix='Orange-WebcamCapture-')

        self.setSizePolicy(QSizePolicy.MinimumExpanding,
                           QSizePolicy.MinimumExpanding)
        box = self.controlArea
        image = self.imageLabel = QLabel(
            margin=0,
            alignment=Qt.AlignCenter,
            sizePolicy=QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored))
        box.layout().addWidget(image, 100)

        self.name_edit = line_edit = gui.lineEdit(
            box, self, 'image_title', 'Title:', orientation=Qt.Horizontal)
        line_edit.setPlaceholderText(self.DEFAULT_TITLE)

        hbox = gui.hBox(box)
        gui.checkBox(hbox, self, 'avatar_filter', 'Avatar filter')
        button = self.capture_button = QPushButton('Capture', self,
                                                   clicked=self.capture_image)
        hbox.layout().addWidget(button, 1000)
        box.layout().addWidget(hbox)

        timer = QTimer(self, interval=40)
        timer.timeout.connect(self.update_webcam_image)
        timer.start()

    def sizeHint(self):
        return QSize(160, 210)

    @staticmethod
    def bgr2rgb(frame):
        return frame[:, :, ::-1].copy()

    def update_webcam_image(self):
        if not self.isVisible():
            if self.cap is not None:
                self.cap.release()
                self.cap = None
            return
        if self.cap is None:
            # Try capture devices in LIFO order
            for dev in range(5, -1, -1):
                cap = self.cap = cv2.VideoCapture(dev)
                if cap.isOpened():
                    break
        cap = self.cap
        self.capture_button.setDisabled(not cap.isOpened())
        success, frame = cap.read()
        if not cap.isOpened() or not success:
            self.Error.no_webcam()
            return
        else:
            self.Error.no_webcam.clear()
        if self.snapshot_flash > 0:
            np.clip(frame.astype(np.int16) + self.snapshot_flash, 0, 255, out=frame)
            self.snapshot_flash -= 15
        image = QImage(frame if self.avatar_filter else self.bgr2rgb(frame),
                       frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pix = QPixmap.fromImage(image).scaled(self.imageLabel.size(),
                                              Qt.KeepAspectRatio | Qt.FastTransformation)
        self.imageLabel.setPixmap(pix)

    @staticmethod
    def clip_aspect_frame(frame):
        """Get the best 1:1 rect around the first face or center of the image"""
        ASPECT_RATIO = 1

        faces = face_cascade_classifier.detectMultiScale(
            cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
        fh, fw = frame.shape[:2]
        if len(faces):
            x, y, w, h = faces[0]
            cx, cy = x + w // 2, y + h // 2
        else:
            cx, cy = fw // 2, fh // 2

        clip_width = fw / fh > ASPECT_RATIO

        if clip_width:
            w, h = int(np.round(fh * ASPECT_RATIO)), fh
            x, y = cx - w // 2, 0
            if x < 0:
                x = 0
            if cx + w // 2 > fw:
                x -= cx + w // 2 - fw
        else:  # clip height
            w, h = fw, int(np.round(fw / ASPECT_RATIO))
            x, y = 0, cy - h // 2
            if y < 0:
                y = 0
            if cy + h // 2 > fh:
                y -= cy + h // 2 - fh

        return frame[y:y + h, x:x + w, :]

    def capture_image(self):
        cap = self.cap
        for i in range(3):  # Need some warmup time; use the last frame
            success, frame = cap.read()
            if success:
                self.Error.no_webcam.clear()
            else:
                self.Error.no_webcam()
                return

        def normalize(name):
            return ''.join(ch for ch in unicodedata.normalize('NFD', name.replace(' ', '_'))
                           if unicodedata.category(ch) in 'LuLlPcPd')

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S.%f')
        image_title, self.image_title = self.image_title or self.DEFAULT_TITLE, ''
        normed_name = normalize(image_title)

        for image, suffix, output in (
                (frame, '', self.Output.SNAPSHOT),
                (self.clip_aspect_frame(frame), '_aspect', self.Output.SNAPSHOT_ASPECT)):
            path = os.path.join(
                self.IMAGE_DIR, '{normed_name}_{timestamp}{suffix}.png'.format(**locals()))
            cv2.imwrite(path,
                        # imwrite expects original bgr image, so this is reversed
                        self.bgr2rgb(image) if self.avatar_filter else image)

            size = ContinuousVariable.make('size')
            width = ContinuousVariable.make('width')
            height = ContinuousVariable.make('height')
            s, w, h = self.image_meta_data(path)
            image_var = StringVariable.make('image')
            image_var.attributes['type'] = 'image'
            metas = np.array([[image_title, path, s, w, h]], dtype=object)
            table = Table.from_numpy(Domain([],
                                     metas=[StringVariable.make('image name'),
                                     image_var, size, width, height]),
                                     np.empty((1, 0)), metas=metas)
            self.send(output, table)

        self.snapshot_flash = 80

    def image_meta_data(self, path):
        reader = QImageReader(path)
        size = os.stat(path).st_size
        width = reader.size().width()
        height = reader.size().height()
        return (size, width, height)


    def __del__(self):
        shutil.rmtree(self.IMAGE_DIR, ignore_errors=True)


if __name__ == "__main__":
    from AnyQt.QtWidgets import QApplication
    a = QApplication([])
    ow = OWNWebcamCapture()
    ow.show()
    a.exec()
