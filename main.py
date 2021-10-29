from core.models.model_user import User

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '1600')


class MyAppMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class MyApp(App, metaclass=MyAppMeta):
    count_click = 5
    users = User.get_all_users()

    def clear_fields(self, fields):
        for item in fields:
            item.text = ''

    def create_table(self, layout, list_users):
        self.users = User.get_all_users()
        for user in self.users:
            list_users.add_widget(Label(text=str(user.id)))
            list_users.add_widget(Label(text=str(user.name)))
            list_users.add_widget(Label(text=str(user.surname)))
            list_users.add_widget(Label(text=str(user.born)))
            list_users.add_widget(Button(text='Удалить', color='red',
                                         on_press=lambda x: User.delete_user(user.id)))
        print('таблица заполнена'),
        return list_users

    def delete_table(self, layout, table):
        table.clear_widgets()
        print('таблица очищена'),
        return layout

    def update_table(self, layout, table, list_users):
        self.delete_table(layout, table)
        self.create_table(layout, list_users)
        print('таблица обновлена')

    def get_user(self, pk):
        users = User.get_all_users()
        for user in users:
            if user.id == pk:
                return user


    def set_fields(self, name_field, surname_field, born_field, name, surname, born):
        name_field.text = name
        surname_field.text = surname
        born_field.text = born

    def build(self):
        main_win = BoxLayout(orientation='vertical')

        list_layout = BoxLayout(orientation='vertical', size_hint=(1, 5))

        titles_table = GridLayout(cols=5, size_hint=(1, 0.5))
        list_users = GridLayout(cols=5, size_hint=(1, 5))

        titles_table.add_widget(Label(text='ID'))
        titles_table.add_widget(Label(text='Name'))
        titles_table.add_widget(Label(text='Surname'))
        titles_table.add_widget(Label(text='Born'))
        list_layout.add_widget(titles_table)

        list_users = self.create_table(list_layout, list_users)

        list_layout.add_widget(list_users)
        titles_table.add_widget(Button(text='Обновить', on_press=lambda x: self.update_table(list_layout,
                                                                                             list_users, list_users)))

        main_win.add_widget(list_layout)

        add_block = BoxLayout(orientation='horizontal')
        add_layout = BoxLayout(orientation='vertical', size_hint=(.8, .8))
        add_btn = Button(text='Добавить', size_hint=(.2, .5))

        add_titles = GridLayout(cols=4, size_hint=(1, 5))
        add_inputs = GridLayout(cols=4, size_hint=(1, 5))

        title_name = Label(text='Name')
        add_titles.add_widget(title_name)
        title_surname = Label(text='Surname')
        add_titles.add_widget(title_surname)
        title_born = Label(text='Born')
        add_titles.add_widget(title_born)
        add_layout.add_widget(add_titles)

        input_name = TextInput()
        add_inputs.add_widget(input_name)
        input_surname = TextInput()
        add_inputs.add_widget(input_surname)
        input_born = TextInput()
        add_inputs.add_widget(input_born)
        add_layout.add_widget(add_inputs)

        add_btn.on_press = lambda: [User.add_user(input_name.text, input_surname.text, input_born.text),
                                    self.update_table(list_layout, list_users, list_users),
                                    self.clear_fields([input_name, input_surname, input_born])
                                    ]

        add_block.add_widget(add_layout)
        add_block.add_widget(add_btn)
        main_win.add_widget(add_block)

        edit_layout = BoxLayout(padding=[0, 10])

        edit_text = BoxLayout(size_hint=(.8, .8), orientation='vertical')

        text_grid_id = BoxLayout(size_hint=(1, .5))
        search_id_field = TextInput(hint_text='Введите id')
        text_grid_id.add_widget(search_id_field)
        edit_text.add_widget(text_grid_id)

        text_grid_data = GridLayout(cols=3, size_hint=(1, .5))
        data_name = TextInput()
        text_grid_data.add_widget(data_name)
        data_surname = TextInput()
        text_grid_data.add_widget(data_surname)
        data_born = TextInput()
        text_grid_data.add_widget(data_born)
        edit_text.add_widget(text_grid_data)

        edit_layout.add_widget(edit_text)

        edit_buttons = BoxLayout(size_hint=(.2, 1), orientation='vertical')

        search_btn = Button(text='Найти', size_hint=(1, 0.5), on_press=lambda x:[self.set_fields(data_name, data_surname,
                                                                                                data_born,
                                                                                                self.get_user(int(search_id_field.text)).name,
                                                                                                self.get_user(int(search_id_field.text)).surname,
                                                                                                self.get_user(int(search_id_field.text)).born)
                                                                                ])
        edit_buttons.add_widget(search_btn)

        save_btn = Button(text='Сохранить', size_hint=(1, 0.5),
                          on_press=lambda x: [User.update_user(int(search_id_field.text), data_name.text,
                                                              data_surname.text, data_born.text),
                            self.update_table(list_layout,
                                     list_users,
                                     list_users)
        ])
        edit_buttons.add_widget(save_btn)

        edit_layout.add_widget(edit_buttons)

        main_win.add_widget(edit_layout)

        main_win.bind(minimum_height=main_win.setter('height'))
        return main_win


if __name__ == "__main__":
    MyApp().run()
