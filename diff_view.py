#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

if sys.hexversion < 0x3040000:
    print('Python >= 3.4 required')
    sys.exit(1)

import os
import argparse

generators_dir = os.path.dirname(os.path.realpath(__file__))

os.system('pyuic5 -o {0} {1}'.format(os.path.join(generators_dir, 'ui_diff_view.py'), os.path.join(generators_dir, 'diff_view.ui')))

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont

from ui_diff_view import Ui_DiffView

class DiffHighlighter(QSyntaxHighlighter):
    def highlightBlock(self, text):
        if text.startswith('-'):
            self.setFormat(0, len(text), Qt.red)
        elif text.startswith('+'):
            self.setFormat(0, len(text), Qt.darkGreen)
        elif text.startswith('@'):
            self.setFormat(0, len(text), Qt.darkCyan)
        elif not text.startswith(' '):
            self.setFormat(0, len(text), Qt.darkBlue)

class DiffBlock:
    def __init__(self):
        self.kind = None
        self.text = None
        self.visible = True

class DiffView(QMainWindow, Ui_DiffView):
    def __init__(self, path):
        super().__init__()

        self.setupUi(self)
        self.setWindowTitle(path + ' - DiffView')

        self.path = path
        self.highlighter = DiffHighlighter(self.edit_diff.document())
        self.blocks = []

        with open(path, 'r') as f:
            block = DiffBlock()
            lines = []

            for line in f.readlines():
                if block.kind == 'hunk':
                    if line[0] not in [' ', '-', '+']:
                        if block.kind != None:
                            block.text = ''.join(lines)

                            self.blocks.append(block)

                        block = DiffBlock()
                        lines = []

                if block.kind == 'meta':
                    if line[0] in ['@']:
                        if block.kind != None:
                            block.text = ''.join(lines)

                            self.blocks.append(block)

                        block = DiffBlock()
                        lines = []

                if block.kind == None:
                    if line.startswith('@'):
                        block.kind = 'hunk'
                    else:
                        block.kind = 'meta'

                lines.append(line)

            if block.kind != None:
                block.text = ''.join(lines)

                self.blocks.append(block)

        self.update_edit()

        self.button_hide_selection.clicked.connect(self.hide_selection)
        self.button_overwrite_file.clicked.connect(self.overwrite_file)

    def update_edit(self):
        total = 0
        visible = 0
        text = ''

        for block in self.blocks:
            total += 1

            if block.visible:
                visible += 1
                text += block.text

        self.edit_diff.setPlainText(text)
        self.label_status.setText('{0} / {1}'.format(visible, total))

    def hide_selection(self):
        text = self.edit_diff.textCursor().selectedText().replace('\u2029', '\n')

        for block in self.blocks:
            if block.kind == 'hunk' and text in block.text:
                block.visible = False

        if self.check_hide_empty_meta.isChecked():
            meta = None
            visible = False

            for block in self.blocks:
                if block.kind == 'meta':
                    if meta != None:
                        meta.visible = visible

                    meta = block
                    visible = False
                elif block.kind == 'hunk':
                    if block.visible:
                        visible = True

            if meta != None:
                meta.visible = visible

        self.update_edit()

    def overwrite_file(self):
        with open(self.path + '.tmp', 'w') as f:
            f.write(self.edit_diff.document().toPlainText())

        os.rename(self.path + '.tmp', self.path)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('patch')

    args = parser.parse_args()

    app = QApplication([])
    window = DiffView(args.patch)

    window.show()

    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())
