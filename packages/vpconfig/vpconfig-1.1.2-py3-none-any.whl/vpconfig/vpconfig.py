import os
from configparser import ConfigParser

class ParamConfig(ConfigParser):
    def __init__(self):
        self.file_path = self.create_config_file()
        super().__init__()
    def up_file_data(self,file_path):
        f=open(file_path,"rd")
        data=f.read().decode('utf-8')
        config_file=open(self.file_path,"w", encoding="utf-8")
        config_file.write(data)
        config_file.close()
        f.close()

    def create_config_file(self):
        base_path = os.path.split(os.path.realpath(__file__))[0]
        file_path = os.path.join(base_path, "config.ini")
        if not os.path.exists(file_path):
            open(file_path, "w", encoding="utf-8")
        return file_path

    def write_config(self):
        self.write(open(self.file_path, "w"))

    def get_sections(self):
        self.read(self.file_path, encoding="utf-8")
        sections = self.sections()
        return sections

    def get_options(self, section):
        self.read(self.file_path, encoding="utf-8")
        sections = self.options(section)
        return sections

    def get_all_sections_options(self):
        sections = self.get_sections()
        sections_options = []
        for x in sections:
            options = self.get_section_item(x)
            sections_options.append({x: options})
        return sections_options

    def get_section_option(self, section, option, type=None):
        self.read(self.file_path, encoding="utf-8")
        if type == None:
            option_value = self.options(section)
        elif type == "int":
            option_value = self.getint(section, option)
        elif type == "bool":
            option_value = self.getboolean(section, option)
        elif type == "float":
            option_value = self.getfloat(section, option)
        else:
            option_value = self.get(section, option)
        return option_value

    def get_section_item(self, section):
        self.read(self.file_path, encoding="utf-8")
        section_item = self.items(section)
        return section_item

    def check_section(self, section):
        self.read(self.file_path, encoding="utf-8")
        check_result = self.has_section(section)
        return check_result

    def check_option(self, option):
        self.read(self.file_path, encoding="utf-8")
        check_result = self.has_option(option)
        return check_result

    def set_option(self, section, option, value):
        self.read(self.file_path, encoding="utf-8")
        self.set(section, option, value)
        self.write_config()

    def add_section_or_option(self, section, option=None, value=None):
        self.read(self.file_path, encoding="utf-8")
        if not option:
            self.add_section(section)
        else:
            self.set_option(section, option, value)
        self.write_config()

    def delete_section(self, section):
        self.read(self.file_path, encoding="utf-8")
        self.remove_section(section)
        self.write_config()

    def delete_option(self, option):
        self.read(self.file_path, encoding="utf-8")
        self.remove_option(option)
        self.write_config()


if __name__ == '__main__':
    param_config = ParamConfig()
