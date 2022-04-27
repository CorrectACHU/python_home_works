import json


class Converter_json_to_csv:
    def __init__(self, file):
        self.file = file
        with open(file, 'r') as read_json:
            json_ = read_json.read()
        self.json = json.loads(json_)

    def make_items_lists(self):
        json_ = self.json
        list_with_elements = [*json_.items()]
        list_with_elements = [list_with_elements[i][1] for i in range(len(list_with_elements))]
        list_with_keys = [*list_with_elements[0].keys()]
        list_with_values = [[*list_with_elements[i].values()] for i in range(len(list_with_elements))]
        return list_with_keys, list_with_values

    def go_to_csv(self):
        our_lists = self.make_items_lists()
        list_with_fields = our_lists[0]
        list_with_values = our_lists[1]
        str_with_elements = ','.join(list_with_fields) + '\n'
        for i in range(len(list_with_values)):
            for j in range(len(list_with_values[i])):
                if list_with_values[i][j] == list(list_with_values[i][j]):
                    list_with_values[i][j] = ', '.join(list_with_values[i][j])
            str_with_elements += ','.join(list_with_values[i]) + '\n'
        return str_with_elements

    def do_it(self):
        str_with_elements = self.go_to_csv()
        with open('output_csv.csv', 'w') as write_csv:
            write_csv.write(str_with_elements)
            print('converter complete')


x = Converter_json_to_csv('input_json.json')
x.do_it()