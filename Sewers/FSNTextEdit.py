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
        if '"' in text_edit_contents:
            text_edit_contents.replace('"',"")
            #print "Removing quotes"
        if " " in text_edit_contents:
            text_edit_contents.replace(' ', "")
            #print "Removing spaces"
        if "\n" in text_edit_contents:
            search_items = list(set(text_edit_contents.split("\n")))
        if "," in text_edit_contents:
            search_items = list(set(text_edit_contents.split(",")))
        if len(text_edit_contents) in [13, 16]:
            search_items = [text_edit_contents]
        #print search_items
        fsn_list = [fsn for fsn in search_items if ((len(fsn) == 16) or (len(fsn) == 13))]
        return fsn_list