import json
import os
import re
import shutil
import mmap
import hashlib
import socket

info_file = 'resources/info.json'
config_file = 'config.json'
dics_folder = 'resources/dics'
models_folder = 'resources/models'
tmp_folder = 'resources/tmp'


# IO

def check_file(path):
    """
    TODO DOCUMENTATION
    :param path:
    :return:
    """
    if not os.path.isfile(path):
        raise Exception("File not found")


def read_json(path):
    """
    TODO DOCUMENTATION
    :param path:
    :return:
    """
    check_file(path)
    with open(path) as f:
        data = json.load(f)
    return data


def save_json(data, path):
    """
    TODO DOCUMENTATION
    :param data:
    :param path:
    :return:
    """
    with open(path, 'w') as out:
        json.dump(data, out, indent=4, ensure_ascii=False)
    return path


def read_info_file():
    """
    TODO DOCUMENTATION
    :return:
    """
    check_file(info_file)
    return json.load(open(info_file))


def read_config_file():
    """
    TODO DOCUMENTATION
    :return:
    """
    check_file(config_file)
    return read_json(config_file)


# GETS
def get_last_model_number():
    """
    TODO DOCUMENTATION
    :return:
    """
    return int("".join(re.findall(r"\d+", get_last_model().split('/')[-1].split('.')[0])))


def get_last_model():
    """
    TODO DOCUMENTATION
    :return:
    """
    return read_info_file()['last_model']


def get_last_dic():
    """
    TODO DOCUMENTATION
    :return:
    """
    return read_info_file()['last_dic']


def get_last_vocab():
    """
    TODO DOCUMENTATION
    :return:
    """
    return read_info_file()['last_vocab']


def get_base_dic():
    """
    TODO DOCUMENTATION
    :return:
    """
    return read_config_file()['base_dict']


# SAVE
def save_last_model(path):
    """
    TODO DOCUMENTATION
    :param path:
    :return:
    """
    info = read_info_file()
    info['last_model'] = path
    save_json(info, info_file)
    return path


def save_last_dic(path):
    """
    TODO DOCUMENTATION
    :param path:
    :return:
    """
    info = read_info_file()
    info['last_dic'] = path
    save_json(info, info_file)
    return path


def save_response(output_path, files):
    """
    TODO DOCUMENTATION
    :param output_path:
    :param files:
    :return:
    """
    if type(files) is not list:
        files = [files]
    out = []
    for i in files:
        output = os.path.join(output_path, os.path.basename(i))
        shutil.copyfile(i, output)
        out.append(output)

    return out


# CLEAN
def clean_older_models():
    """
    TODO DOCUMENTATION
    :return:
    """
    models = [os.path.join(models_folder, i) for i in os.listdir(models_folder) if re.match(r"model[0-9]*\.pm", i)]
    models.remove(get_last_model())
    for model in models:
        os.remove(model)


def clean_older_dics():
    """
    TODO DOCUMENTATION
    :return:
    """
    pass  # TODO IMPLEMENTATION - REMOVE ALL DICS AND VOCABS BELOW N-LAST


def clean_tmp_folder():
    """
    TODO DOCUMENTATION
    :return:
    """
    shutil.rmtree(tmp_folder)


# MISC
def search_file(word, file):
    """
    TODO DOCUMENTATION
    :param word:
    :param file:
    :return:
    """
    s = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
    result = s.find(word) != -1
    return result


def check_word(word, hash_set):
    """
    TODO DOCUMENTATION
    :param word:
    :type word: str
    :param hash_set:
    :type hash_set: set
    :return:
    """
    hash_value = hashlib.md5(word.rstrip()).hexdigest()
    if hash_value not in hash_set:
        hash_set.add(hash_value)
        return False
    return True


def get_ip():
    """
    TODO DOCUMENTATION
    :return:
    """
    return socket.gethostbyname(socket.gethostname())