from random import randint

import Levenshtein


def levenshtein(input: str, data_set: list, input_error: int) -> str:

    # data_set = os.listdir(url_data_set)

    if input != "*":
        associative_table = []
        for data in data_set:
            e = Levenshtein.distance(input, data)
            if not e:
                return data
            associative_table.append(e)
        error = min(associative_table)
        if error > input_error:
            raise Exception
        else:
            return data_set[associative_table.index(error)]
    else:
        return data_set[randint(0, len(data_set) - 1)]


def random(files) -> str:
    if not len(files):
        raise Exception
    return files[randint(0, len(files) - 1)]
