from PyQt4.QtGui import QWidget, QLabel, QTextEdit, QVBoxLayout

class FSNTextEdit(QWidget):
    def __init__(self, *args, **kwargs):
        super(FSNTextEdit, self).__init__(*args, **kwargs)
        self.fsn_label = QLabel("FSN(s):")
        self.text_edit = QTextEdit()
        layout = QVBoxLayout()
        layout.addWidget(self.fsn_label,0)
        layout.addWidget(self.text_edit,2)
        self.text_edit.setToolTip("Paste a list of FSNs here. Preferably from Excel or Google Spreadsheets.\nIf you're entering more than 1 FSN yourself, then please separate them either by a comma or a new line.")
        self.setLayout(layout)

    def getFSNs(self):
        text_edit_contents = str(self.text_edit.toPlainText()).strip()
        #print "Got text!"
        fsns_string = []
        possible_separators = [" ","'",'"', ","]
        for separator in possible_separators:
            if separator in text_edit_contents:
                text_edit_contents = text_edit_contents.replace(separator,"\n")
        if "\n" in text_edit_contents:
            fsns_string = list(set(text_edit_contents.split("\n")))
        if len(text_edit_contents) in [13, 16]:
            fsns_string = [text_edit_contents]
        #print fsns_string
        if len(fsns_string)>0:
            fsn_list = [fsn for fsn in fsns_string if ((len(fsn) == 16) or (len(fsn) == 13))]
        else:
            fsn_list = fsns_string
        return list(set(fsn_list))