import argparse
from abc import ABC, abstractmethod
from itertools import islice


class Converter(ABC):
    @abstractmethod
    def convert(self):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self):
        pass


class SCVHandler(Converter):
    def __init__(self, input_file, output_file):
        self._input_file = input_file
        self._output_file = output_file
        self._lines = None
        self._titles = None
        self._objects = self.parse()
        self._converted = self.convert()

    def convert(self):
        result_string = ""
        if len(self) > 1:
            result_string += "[ \n"
            for obj in self:
                result_string += "{ \n"
                for key, value in obj.items():
                    result_string += f'"{key}": "{value}", \n'
                result_string = result_string[0:-3] + " \n"
                result_string += "}, \n"
            result_string = result_string[0:-3] + " \n"
            result_string += "] \n"
        else:
            for obj in self:
                result_string += "{ \n"
                for key, value in obj.items():
                    result_string += f'"{key}": "{value}", \n'
                result_string = result_string[0:-3] + " \n"
                result_string += "} \n"
        return result_string

    def write(self):
        with open(self._output_file, "w") as file:
            file.write(self._converted)

    def parse(self):
        self.read()
        self._titles = self.parse_titles()
        data = []
        for index, line in enumerate(islice(self._lines, 1, None)):
            object_ = {}
            coll_patterns = self._find_collection_patterns(line)

            titles = list(self._titles)
            for part in line.split('"'):
                if part not in coll_patterns:
                    for value in part.split(","):
                        if value.replace(" ", "") != "":
                            try:
                                if value != '':
                                    object_.update({titles[0]: value})
                                    titles.remove(titles[0])
                                else:
                                    object_.update({titles[0]: value})
                                    titles.remove(titles[0])
                            except IndexError:
                                pass
                else:
                    try:
                        object_.update({titles[0]: part})
                        titles.remove(titles[0])
                    except IndexError:
                        pass
            data.append(object_)
        return data

    def read(self):
        try:
            with open(self._input_file) as file:
                self._lines = file.readlines()
                self._format_lines()
        except FileNotFoundError:
            print("File not found")

    def parse_titles(self):
        return tuple(self._lines[0].split(","))

    @staticmethod
    def _find_collection_patterns(line):
        patterns = []
        pattern = ""
        opened = False
        for symb in line:
            if opened:
                pattern += symb

            if symb == '"':
                if opened:
                    opened = False
                    patterns.append(pattern.replace('"', ''))
                    pattern = ""
                elif not opened:
                    opened = True
        return patterns

    def _format_lines(self):
        for index, line in enumerate(self._lines):
            self._lines[index] = line.strip("\n")

    def __iter__(self):
        return iter(self._objects)

    def __getitem__(self, item):
        for obj in self:
            for key, value in obj.items():
                if key == item:
                    yield value

    def __len__(self):
        return len(self._objects)


def convert(input_file, output_file):
    scv_handler = SCVHandler(input_file, output_file)
    scv_handler.write()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('output_file')
    input_file = parser.parse_args().input_file
    output_file = parser.parse_args().output_file
    convert(input_file, output_file)
    # convert(r"data/data_file.scv", "converted.json")

