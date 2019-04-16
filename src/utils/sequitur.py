import os.path
import subprocess

from utils.IO import *


# SEQUITUR
def generate_phonetic_dic(words_path):
    """
    TODO DOCUMENTATION
    :param words_path:
    :return:
    """
    config = read_config_file()

    # base = '/Users/pablomaciasmunoz/anaconda3/envs/S2T_G2P/bin/python'  # TODO DELETE IN CONTAINER
    # command = os.path.join(config['sequitur_path'], 'g2p.py')
    command = 'g2p.py'

    out_words_path = os.path.join(tmp_folder, 'words.dic')
    f = open(out_words_path, 'w')

    script = [command,
              '--model', get_last_model(),
              '--apply', words_path]
    p = subprocess.call(script, stdout=f)
    f.close()
    if p != 0:
        raise Exception('Error in phonetic dictionary generation')

    return out_words_path


def improve_dic(phonetic_dic):
    """
    TODO DOCUMENTATION
    :param phonetic_dic:
    :return:
    """
    vocab_in = open(get_last_vocab())
    vocab_out = open(get_last_vocab(), 'a')
    dic_out = open(get_last_dic(), 'a')
    completed_lines_hash = set()

    for word in open(phonetic_dic):
        word_sim = word.split()[0]
        word_encode = word_sim.encode('utf8')
        if not check_word(word_encode, completed_lines_hash) and not search_file(word_encode, vocab_in):
            vocab_out.write(word_sim + '\n')
            dic_out.write(word)

    vocab_out.close()
    vocab_in.close()
    dic_out.close()


def convert_words(words_path):
    """
    TODO DOCUMENTATION
    :param words_path:
    :return:
    """

    # DICT
    dic = get_dic()

    # MODEL
    get_model(dic)

    return generate_phonetic_dic(words_path)


def get_model(dic):
    """
    TODO DOCUMENTATION
    :param dic:
    :return:
    """
    model = get_last_model()
    if model == '':
        config = read_config_file()
        model = create_phonetic_model(dic)
        for i in range(config['max_improving']):
            improve_model(model)


def get_dic():
    """
    TODO DOCUMENTATION
    :return:
    """
    dic = get_last_dic()
    if dic == '' or not os.path.isfile(dic):
        dic = get_base_dict()
        save_last_dic(dic)
    return dic


def improve_model(model):
    """
    TODO DOCUMENTATION
    :param model:
    :return:
    """
    config = read_config_file()

    # base = '/Users/pablomaciasmunoz/anaconda3/envs/S2T_G2P/bin/python'  # TODO DELETE IN CONTAINER
    # command = os.path.join(config['sequitur_path'], 'g2p.py')
    command = 'g2p.py'

    n = get_last_model_number() + 1

    out_model_path = os.path.join(models_folder, 'model{}.pm'.format(n))
    script = [command,
              '--model', model, '--ramp-up',
              '--train', config['train_devel'],
              '--write-model',
              out_model_path]
    p = subprocess.call(script)
    if p != 0:
        raise Exception('Error in phonetic model generation')

    return save_last_model(out_model_path)


# def install_sequitur():
#     """
#     TODO DOCUMENTATION
#     :return:
#     """
#     script = ['pip', 'install', 'numpy']
#     p = subprocess.Popen(script, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     p.wait()
#     script = ['pip', 'install', 'git+https://github.com/sequitur-g2p/sequitur-g2p@master']
#     p = subprocess.Popen(script, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     p.wait()


def create_phonetic_model(dic):
    """
    TODO DOCUMENTATION
    :param dic:
    :return:
    """
    config = read_config_file()
    init_devel = config['init_devel']
    max_iters = config['max_iterations']

    # base = '/Users/pablomaciasmunoz/anaconda3/envs/S2T_G2P/bin/python'  # TODO DELETE IN CONTAINER
    # command = os.path.join(read_config_file()['sequitur_path'], 'g2p.py')
    command = 'g2p.py'

    out_model_path = os.path.join(models_folder, 'model0.pm')
    script = [command,
              '--train', dic,
              '-I', str(max_iters),
              '--devel', '{}%'.format(init_devel),
              '--write-model', out_model_path]
    p = subprocess.call(script)
    if p != 0:
        raise Exception('Error in phonetic model generation')

    return save_last_model(out_model_path)


def get_base_dict():
    """
    TODO DOCUMENTATION
    :return:
    """
    return os.path.join(dics_folder, 'es.dic')
