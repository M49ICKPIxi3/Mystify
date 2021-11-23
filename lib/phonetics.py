# import phonetics
import pronouncing

import subprocess


# Possible to installing wordnet at runtime? Not necessary probably
def get_user_site():
    output = subprocess.getoutput('python3.8 -m site')
    return output


def main():

    user_site = get_user_site()
    stop_here = ''

    #inspiration_words = ['lovely', 'pretty', 'sweet', 'joy']

    #print(pronouncing.rhymes('mary'))


if __name__ == '__main__':
    main()
