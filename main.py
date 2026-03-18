import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QVBoxLayout, QFileDialog, QLabel
)
from hwpx_merge import merge_hwpx


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HWPX 병합 프로그램")
        self.setGeometry(300, 300, 400, 200)

        self.files = []

        layout = QVBoxLayout()

        self.label = QLabel("파일을 선택하세요")
        layout.addWidget(self.label)

        btn_select = QPushButton("HWPX 파일 선택")
        btn_select.clicked.connect(self.select_files)
        layout.addWidget(btn_select)

        btn_merge = QPushButton("병합하기")
        btn_merge.clicked.connect(self.merge_files)
        layout.addWidget(btn_merge)

        self.setLayout(layout)

    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "파일 선택",
            "",
            "HWPX Files (*.hwpx)"
        )
        if files:
            self.files = files
            self.label.setText(f"{len(files)}개 파일 선택됨")

    def merge_files(self):
        if not self.files:
            self.label.setText("파일을 먼저 선택하세요")
            return

        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "저장 위치",
            "merged.hwpx",
            "HWPX Files (*.hwpx)"
        )

        if save_path:
            merge_hwpx(self.files, save_path)
            self.label.setText("병합 완료!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
