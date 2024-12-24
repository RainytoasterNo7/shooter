from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication , QWidget, QPushButton, QLabel, QVBoxLayout, QRadioButton, QHBoxLayout, QGroupBox, QButtonGroup, QListWidget, QTextEdit, QInputDialog, QLineEdit
app = QApplication([])
import json
notes = {
    'Добро пожаловать!':
    {
        'текст':'это самое лучшее приложение для заметок в мире',
        'теги':['добро','инструкция']
    }
}
window = QWidget()
window.show()
text = QTextEdit()
list_widget = QListWidget()
list_tags = QListWidget()
with open('notes_data.json','r',encoding='utf-8') as file:
    notes = json.load(file)
    list_widget.addItems(list(notes))
def show_results():
    name = list_widget.selectedItems()[0].text()
    text.setText(notes[name]['текст'])
    list_tags.clear()
    list_tags.addItems(notes[name]['теги'])
def add_note():
    note_name , result = QInputDialog.getText(
        window,'Добавить заметку','Название заметки:'
    )
    notes[note_name] = {'текст':'','теги':[]}
    list_widget.addItem(note_name)
    with open('notes_data.json','w',encoding='utf-8') as file:
        json.dump(notes,file)
def save_notes():
    if list_widget.selectedItems():
        name = list_widget.selectedItems()[0].text()
        note_text = text.toPlainText()
        notes[name]['текст'] = note_text
        with open('notes_data.json','w',encoding='utf-8') as file:
            json.dump(notes,file)
def del_note():
    if list_widget.selectedItems():
        name = list_widget.selectedItems()[0].text()
        del notes[name]
        list_widget.clear()
        list_widget.addItems(list(notes))
        with open('notes_data.json','w',encoding='utf-8') as file:
            json.dump(notes,file)
def add_tag():
    if list_widget.selectedItems():
        tag_name = tag_line.text()
        name = list_widget.selectedItems()[0].text()
        notes[name]['теги'].append(tag_name)
        list_tags.clear()
        list_tags.addItems(notes[name]['теги'])
        with open('notes_data.json','w',encoding='utf-8') as file:
            json.dump(notes,file)
def del_tag():
    if list_widget.selectedItems():
        if list_tags.selectedItems():
            name = list_widget.selectedItems()[0].text()
            tag_text = list_tags.selectedItems()[0].text()
            notes[name]['теги'].remove(tag_text)
            list_tags.clear()
            list_tags.addItems(notes[name]['теги'])
            with open('notes_data.json','w',encoding='utf-8') as file:
                json.dump(notes,file)
def search_tag():
    if save_tags.text() == 'Искать заметки по тегу':
        tag_search = tag_line.text()
        if tag_search != '':
            list_widget.clear()
            for name in notes:
                if tag_search in notes[name]['теги']:
                    list_widget.addItem(name)
                    tag_line.clear()
            save_tags.setText('Вернуться обратно')
    else:
        list_widget.clear()
        list_widget.addItems(notes)
        save_tags.setText('Искать заметки по тегу')
delete_note = QPushButton('Удалить заметку')
create_note = QPushButton('Создать заметку')
save_note = QPushButton('Сохранить заметку')
add_tags = QPushButton('Добавить к заметке')
delete_tag = QPushButton('Открепить от заметки')
save_tags = QPushButton('Искать заметки по тегу')
tag_line = QLineEdit('')
hhighline = QHBoxLayout()
hcenterline = QHBoxLayout()
hlowerline = QHBoxLayout()
vleftline = QVBoxLayout()
vrightline = QVBoxLayout()
vrightline.addWidget(list_widget)
vrightline.addLayout(hhighline)
hhighline.addWidget(create_note)
hhighline.addWidget(delete_note)
vrightline.addWidget(save_note)
vrightline.addWidget(list_tags)
vrightline.addWidget(tag_line)
vrightline.addLayout(hlowerline)
hlowerline.addWidget(add_tags)
hlowerline.addWidget(delete_tag)
vrightline.addWidget(save_tags)
vleftline.addWidget(text)
list_widget.itemClicked.connect(show_results)
save_note.clicked.connect(save_notes)
create_note.clicked.connect(add_note)
delete_note.clicked.connect(del_note)
add_tags.clicked.connect(add_tag)
delete_tag.clicked.connect(del_tag)
save_tags.clicked.connect(search_tag)
hcenterline.addLayout(vleftline)
hcenterline.addLayout(vrightline)
window.setLayout(hcenterline)
app.exec()