class Converter_csv_to_json:
    # pass a string with the file path
    def __init__(self, file):
        with open(file, 'r') as read_csv:
            csv = read_csv.read()
        self.csv = csv
        self.list_csv = csv.split('\n')

    def find_separator(self):
        SEPARATORS = [';', ',']
        our_list = self.list_csv
        for separator in SEPARATORS:
            if our_list[0].find(separator) > 0:
                return separator

    def csv_to_list(self):
        csv = self.csv
        separator = self.find_separator()
        csv = csv.replace(', ', '~~')
        csv = csv.replace(separator, ';')
        csv = csv.replace('~~', ', ')
        csv = csv.split('\n')
        list_with_data = [i.split(';') for i in csv]
        for i in list_with_data:
            for j in range(len(i)):
                if ', ' in i[j]:
                    x = i[j].split(',')
                    x = [i.lstrip() for i in x]
                    i.remove(i[j])
                    i.insert(j, x)
        return list_with_data

    def make_dict_with_pk(self):
        our_list = self.csv_to_list()
        dict_with_pk = [(str(i), {}) for i in range(1, len(our_list))]
        dict_with_pk = dict(dict_with_pk)
        return dict_with_pk

    def make_json(self):
        count1 = 0
        count2 = 1
        our_list = self.csv_to_list()
        our_dict = self.make_dict_with_pk()
        try:
            while count2 != len(our_list):
                if count1 == len(our_list[0]):
                    count1 = 0
                    count2 += 1
                else:
                    our_dict[str(count2)][str(our_list[0][count1])] = our_list[count2][count1]
                    count1 += 1
            prepared_json = str(our_dict).replace("'", '"')
            return prepared_json
        except IndexError:
            print('your csv format is bad, json was not prepared')

    # call it and see the magic
    def do_it(self):
        prepared_json = self.make_json()
        with open('output_json.json', 'w') as write_json:
            write_json.write(prepared_json)
        print('good job, json is already prepared')


string_csv = Converter_csv_to_json('input_csv.csv')
string_csv.do_it()
