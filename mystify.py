import sys
import os
import sublime_plugin
import sublime
from collections import defaultdict

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

import json

"""
Takes a string and filters out everything but alphanumeric characters.
"""

# Someone somewhere probably wants a cooler filename, this is V where V you V do that...
def filter_arb(_string):
    return ''.join(ch for ch in _string if ch.isalpha() or ch in ['.', '-', '_'])  # Here

import subprocess
import os
import sys

third_party_libraries = [
    'git+https://github.com/goodmami/wn'
]

wn_library = 'git+https://github.com/goodmami/wn'

def pip_install(mod):
    print(str(subprocess.check_output(f'pip3.8 install {mod}', shell=True)))

def get_user_site():
    output = subprocess.getoutput('python3.8 -m site')
    print(output)


class MystifyRunnerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.edit = edit
        self.view.window().show_input_panel('Run:', '', self.on_done, None, None)

    def on_done(self, text):
        try:
            print(str(subprocess.getoutput(text)))
        except Exception as e:
            print(e.args)




"""
try:
    import pexpect
except:
    pip_install('pexpect')
    import pexpect"""


"""
Allows user input a string. Filters out everything but alphanumeric, dashes, and underscores.
"""
class AddModelCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.edit = edit
        self.view.window().show_input_panel('Model:', '', self.on_done, None, None)

    def on_done(self, text):
        settings_data = read_json(CURRENT_DIR + '/mystify.sublime-settings')
        try:
            settings_data['models'].append(text)
        except Exception as e:
            print(e.args)

        # TODO: Create all the default engine parameters. Have a settings thing where you can turn models on or off
        # TODO: Set default generator. Then the Generate command won't require the user to constantly switch models.


        # create new fine-tuned model from template. This will always be a model parameter, presets saved a bit diff.
        # Low on priority list: presets.

        


class FilterCommand(sublime_plugin.TextCommand):
    def run(self, edit, text=""):
        if not text: return

        view = self.view

        newSelections = []

        for selection in view.sel():
            lines = view.lines(selection)

            newSelections += [sublime.Region(view.full_line(line).begin(), view.full_line(line).end()) for line in lines]

            newSelections += [sublime.Region(view.full_line(line).end(), line) for line in lines]

            newSelections += [sublime.Region(line, view.full_line(line).begin()) for line in lines]

            newSelections += [sublime.Region((view.full_line)(line).begin(), line) for line in lines]

        view.sel().clear()
        [view.sel().add(region) for region in newSelections]








class OpenFileFromListCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.files = []
        self.view.window().show_quick_panel(self.files, self.open_file)

    def open_file(self, index):
        if index == -1:
            return

        file = self.files[index]

        if os.path.isfile(file):
            self.view.window().open_file(file)











def read_text(path):
    with open(path, errors="replace") as file:
        text = file.read()
    return text


def write_text(path, output):
    with open(path, 'w+') as file:
        file.write(output)


def read_json(path):
    with open(path) as data_file:
        json_data = json.load(data_file)
    return json_data


def write_json(path, data):
    with open(path, 'w+') as outfile:
        json.dump(data, outfile, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False)


# How to do this: command to edit the settings for a model, open the settings file in a new scratch window and
# allow the user to fill it in, save it



CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MYSTIFY_LIBRARY_PATH = CURRENT_DIR + '/lib'
SITE_PACKAGES_DIR = '/Users/saya/.pyenv/versions/3.8.0/lib/python3.8/site-packages'

os.environ["PYTHONPACKAGES"] = SITE_PACKAGES_DIR

CONTEXT_MENU_DIR = os.path.join(sublime.packages_path(), 'User', 'mystify')


sys.path.append(MYSTIFY_LIBRARY_PATH)
sys.path.append(CURRENT_DIR)
sys.path.append(os.environ['PYTHONPACKAGES'])

CONTEXT_MENU_PATH = CONTEXT_MENU_DIR + '/Context.sublime-menu'


if not os.path.exists(CONTEXT_MENU_DIR):
    os.makedirs(CONTEXT_MENU_DIR)



from lib.context_menu import ContextMenuBuilder
from lib.wordnet_api import WordnetApi


from typing import List
# import pysnooper

import inspect

#inspect.getmembers(sublime)



class ReplaceWordCommand(sublime_plugin.TextCommand):
    def run(self, edit, new_text):
        for region in self.view.sel():
            if not region.empty():

                self.view.replace(edit, region, new_text)

class DoNothingCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print('nothing!')



# TO LOG COMMANDS: sublime.log_input(True); sublime.log_commands(True); sublime.log_result_regex(True)
class EventListener(sublime_plugin.EventListener):
    wordnet_api = WordnetApi()
    simple_cache_synsets = {}
    simple_cache_relations = {}

    plugin_event_name = 'mystify'

    @staticmethod
    def get_selected(view, event):
        pt = view.window_to_text((event["x"], event["y"]))
        selected = view.sel()
        if len(selected):
            selection = selected[0]
            if not selection.empty() and selection.contains(pt):
                content = view.substr(selected[0]).strip()
                if content:
                    return content
        return None


    def on_post_text_command(self, view, command, args):
        if command == "context_menu":
            pass
            #if os.path.exists(CONTEXT_MENU_PATH):
            #    os.remove(CONTEXT_MENU_PATH)

    def _on_generate(self, view: sublime.View, command: sublime_plugin.TextCommand, args):
        content = EventListener.get_selected(view, args['event'])
        view.run_command('generate_from_selection')



    def on_text_command(self, view, command, args):
        if command == 'context_menu':
            pip_install(wn_library)

            content = EventListener.get_selected(view, args['event'])
            if content is None:
                return #(self.plugin_event_name, 'no selected text')

            # TODO: Implement top level caching if necessary. LRU cache in
            #       wordnet_api should do this...

            #if content not in self.simple_cache_synsets:
                #wn_text_data = self.wordnet_api.get_data_for_text(content)
                #self.simple_cache_synsets[content] = wn_text_data

            text_data = self.wordnet_api.get_data_for_text(content)

            synsets_caption = 'synset'
            synsets_menu_id = 'synset'
            synset_menu = ContextMenuBuilder.build_menu_or_submenu(synsets_caption, synsets_menu_id)
            words_list = text_data['words']
            if len(words_list) >= 20:
                words_list = words_list[:18]

            for word in words_list:
                word_command = ContextMenuBuilder.build_command_entry(
                    caption=word,
                    command='replace_word',
                    args={
                        'new_text': word
                    })
                synset_menu['children'].append(word_command)

            # Adding Synsets Menu
            context_menu_entries = [synset_menu]

            print('before definitions')
            if text_data['definitions'] is not None:
                definitions_caption = 'definition'
                definitions_menu_id = 'definition'
                definitions_menu = ContextMenuBuilder.build_menu_or_submenu(definitions_caption, definitions_menu_id)

                definitions_by_pos = defaultdict(list)
                for definition_data in text_data['definitions']:
                    definitions_by_pos[definition_data[1]].append(definition_data[0])

                for pos, definitions in definitions_by_pos.items():
                    pos_submenu = ContextMenuBuilder.build_menu_or_submenu(pos, pos)
                    for definition in definitions:
                        word_command = ContextMenuBuilder.build_command_entry(
                            caption=definition,
                            command='do_nothing'
                        )
                        pos_submenu['children'].append(word_command)
                    definitions_menu['children'].append(pos_submenu)

                print('got definitions')
                context_menu_entries.append(definitions_menu)

            if len(text_data['relations'].keys()) > 0:
                relations_caption = 'relations'
                relations_menu_id = 'relations'
                relations_menu = ContextMenuBuilder.build_menu_or_submenu(relations_caption, relations_menu_id)

                for rel_type, rel_words in text_data['relations'].items():
                    rel_type_submenu = ContextMenuBuilder.build_menu_or_submenu(
                        caption=rel_type,
                        menu_id=rel_type
                    )

                    for rel_word in rel_words:
                        rel_word_command = ContextMenuBuilder.build_command_entry(
                            caption=rel_word,
                            command='replace_word',
                            args={
                                'new_text': rel_word
                            }
                        )
                        rel_type_submenu['children'].append(rel_word_command)

                    relations_menu['children'].append(rel_type_submenu)

                context_menu_entries.append(relations_menu)

            ContextMenuBuilder.append_context_menu(
                context_menu_entries=context_menu_entries,
                file_path=CONTEXT_MENU_PATH
            )

            print('it worked!')
            #return (self.plugin_event_name, 'command successful!')

