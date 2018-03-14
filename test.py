
import os

t = "/home/haoming/Desktop/Data/new_data"


dirs = os.walk(t)

a = str("a")

a.split("a")


file_dict = dict()

for d in dirs:
    if d[2]:
        _sub_dirs = [s for s in d[0].split("/") if s not in t.split("/")]

        if _sub_dirs[0] not in file_dict.keys():
            file_dict.update({_sub_dirs[0]: dict()})

        if _sub_dirs[1] not in file_dict[_sub_dirs[0]].keys():
            file_dict[_sub_dirs[0]].update({_sub_dirs[1]: dict()})

        if _sub_dirs[2] not in file_dict[_sub_dirs[0]][_sub_dirs[1]].keys():
            file_dict[_sub_dirs[0]][_sub_dirs[1]].update({_sub_dirs[2]: dict()})

        for file in d[2]:
            if '.asc' in file:
                _began_read_line = False
                with open(d[0]+'/'+file, 'r') as this_file:
                    _lines = this_file.readlines()
                    for line in _lines:
                        _line = [s for s in line.split(' ') if s is not '']
                        if _began_read_line:
                            try:
                                if _line[0] not in file_dict[_sub_dirs[0]][_sub_dirs[1]][_sub_dirs[2]].keys():
                                    #print(_line)
                                    file_dict[_sub_dirs[0]][_sub_dirs[1]][_sub_dirs[2]].update({_line[0]: {file.replace('.asc', ''): float(_line[1])}})
                                else:
                                    file_dict[_sub_dirs[0]][_sub_dirs[1]][_sub_dirs[2]][_line[0]].update({file.replace('.asc', ''): float(_line[1])})

                            except IndexError:
                                pass
                        if all(s in _line for s in ['Number']):
                            _began_read_line = True


print(file_dict)








































