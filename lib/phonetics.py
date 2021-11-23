# import phonetics
import pronouncing

import inspect
import subprocess



def get_user_site():
    output = subprocess.getoutput('python3.8 -m site')
    return output


def main():

    user_site = get_user_site()
    stop_here = ''

    for _inspect_name, _inspect_data in inspect.getmembers(inspect, inspect.isfunction):
        stop_here = ''
        if '_' not in _inspect_name[0]:
            stop_here = ''
            if 'get' in _inspect_name:
                stop_here = ''
            #output.extend(_get_all_of(sublime_api, '', _inspect_data))

        print(f'{_inspect_name} {_inspect_data}')


    #inspiration_words = ['lovely', 'pretty', 'sweet', 'joy']

    #print(pronouncing.rhymes('mary'))


if __name__ == '__main__':
    main()
