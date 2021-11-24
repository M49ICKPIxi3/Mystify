import sys
import os
import sublime_plugin
import sublime





def append_sys_path(paths):
    for path in paths:
        if path not in sys.path:
            sys.path.append(path)


# How to do this: command to edit the settings for a model, open the settings file in a new scratch window and
# allow the user to fill it in, save it

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MYSTIFY_LIBRARY_PATH = CURRENT_DIR + '/lib'

current_directory = os.path.join(sublime.packages_path(), 'mystify')
_library_directory = os.path.join(sublime.packages_path(), 'mystify', 'lib')

SITE_PACKAGES_DIR = '/Users/saya/.pyenv/versions/3.8.0/lib/python3.8/site-packages'

#os.environ["PYTHONPACKAGES"] = SITE_PACKAGES_DIR

CONTEXT_MENU_DIR = os.path.join(sublime.packages_path(), 'User', 'mystify')

if _library_directory not in sys.path:
    sys.path.append(_library_directory)

if _current_directory not in sys.path:
    sys.path.append(_current_directory)

if os.getenv('PYTHONPACKAGES') not in sys.path:
    sys.path.append(os.environ['PYTHONPACKAGES'])

append_sys_path([

])

from lib.wordnet_api import WordnetApi
from lib.rhymes import RhymingApi
from lib.context_menu_builder import ContextMenuBuilder

from collections import defaultdict

CONTEXT_MENU_PATH = CONTEXT_MENU_DIR + '/Context.sublime-menu'

if not os.path.exists(CONTEXT_MENU_DIR):
    os.makedirs(CONTEXT_MENU_DIR)

class ReplaceWordCommand(sublime_plugin.TextCommand):
    def run(self, edit, new_text):
        for region in self.view.sel():
            if not region.empty():
                self.view.replace(edit, region, new_text)

class DoNothingCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # TODO: Surely there's a better way to do this...
        print('nothing!')


# TO LOG COMMANDS: sublime.log_input(True); sublime.log_commands(True); sublime.log_result_regex(True)
class EventListener(sublime_plugin.EventListener):
    wordnet_api = WordnetApi()
    rhyming_api = RhymingApi()
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
            if os.path.exists(CONTEXT_MENU_PATH):
                os.remove(CONTEXT_MENU_PATH)


    def on_text_command(self, view, command, args):
        if command == 'context_menu':

            content = EventListener.get_selected(view, args['event'])
            if content is None:
                return

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

            rhymes = self.rhyming_api.get_rhymes_for_word(content)
            if len(rhymes) > 0:
                rhymes_caption = 'rhymes'
                rhymes_menu_id = 'rhymes'
                rhymes_menu = ContextMenuBuilder.build_menu_or_submenu(rhymes_caption, rhymes_menu_id)
                for rhyme in rhymes:
                    word_command = ContextMenuBuilder.build_command_entry(
                        caption=rhyme,
                        command='do_nothing'
                    )
                    rhymes_menu['children'].append(word_command)

                print('added rhymes!')
                context_menu_entries.append(rhymes_menu)

            ContextMenuBuilder.append_context_menu(
                context_menu_entries=context_menu_entries,
                file_path=CONTEXT_MENU_PATH
            )

            print('it worked!')
