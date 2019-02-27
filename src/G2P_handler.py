import Pyro4

from ContainerHandler import ContainerHandler
from utils.IO import read_json, check_file, get_last_dic, save_response
from utils.sequitur import convert_words, improve_dic


@Pyro4.expose
class G2PHandler(ContainerHandler):
    def __init__(self, container_name, main_uri):
        super(G2PHandler, self).__init__(container_name, main_uri)
        # install_sequitur()

    def run(self, **kwargs):
        if 'input_json' in kwargs and 'output_folder' in kwargs:
            print("Container {}: Runned with {}".format(self.container_name, kwargs))
            self.running = True
            result = self.generate_dic(kwargs['input_json'], kwargs['output_folder'])
            self.running = False
            return result
        else:
            raise TypeError('input_json and output_folder required')

    def info(self):
        pass

    def generate_dic(self, input_json, output_folder):
        json_info = read_json(input_json)
        words_path = json_info['words_path']
        check_file(words_path)

        words_dic_path = convert_words(words_path)

        improve_dic(words_dic_path)

        return save_response(output_folder, get_last_dic())


if __name__ == '__main__':
    handler = G2PHandler('G2P', 'PYRO:MainController@localhost:4040')
    handler.generate_dic('resources/tmp/input.json', 'resources/tmp')
