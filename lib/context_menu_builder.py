import json


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

"""
Api of this is like:
create_menu
create_submenu(menu_id)
update_menu(menu_obj)

holds a menu which is a dict of elements all tied to a menu id

[
    {
        "caption": "Word_A",
        "id": "Word_A",
        "children":
        [
            { 
                "caption": "relations",  
                "id": "relations", 
                "mnemonic": "R", 
                "children": [
                    {
                        "caption": "relation_type",
                        "id": "rel_type_name",
                        "children": [
                            { 
                                "command": "replace_word", 
                                "caption": "Rel Word A", 
                                "mnemonic": "A",         # This will be in alphabetical order, so sequence R -> A
                                "args": {
                                    "text": "...", 
                                    "new_text": "..." 
                                }
                            }
                        ]
                    }
                ]
            }
            
        ]
    }
]
"""
class ContextMenuBuilder(object):
    menu_name = 'Context.sublime-menu'
    menu_entries = {}

    def __init__(self, file_path):
        #self.menu_dir = menu_dir
        self.file_path = file_path
        #if not os.path.exists(self.menu_dir):
        #    os.makedirs(self.menu_dir)

    def create_menu(self, caption, menu_id):
        """
        Creates a new menu with the given id.
        """
        self.menu_entries[menu_id] = {
            "caption": caption,
            "id": menu_id,
            "children": []
        }

    def create_command_entry(self, parent_id, caption, command, args=None):
        self.menu_entries[parent_id]['children'].append({
            'caption': caption,
            'command': command,
            'args': args
        })

    @staticmethod
    def build_menu_or_submenu(caption, menu_id):
        """
        Creates a new menu with the given id.
        """
        return {
            "caption": caption,
            "id": menu_id,
            "children": []
        }

    @staticmethod
    def build_command_entry(caption, command, args=None):
        if args is not None:
            return {
                'caption': caption,
                'command': command,
                'args': args
            }
        else:
            return {
                'caption': caption,
                'command': command
            }


    @staticmethod
    def append_context_menu(context_menu_entries, file_path):
        with open(file_path, 'w+') as config_file:
            json.dump(context_menu_entries, config_file, indent=4, sort_keys=False)


"""
def main():
    current_dir = os.getcwd()
    parent_dir = '/'.join(current_dir.split('/')[:-1])

    CONTEXT_MENU_PATH = parent_dir + '/Context.sublime-menu'


    wordnet_api = WordnetApi()
    # synsets = wordnet_api.get_synsets_or_none('test')
    # rhymes = wordnet_api.get_rhymes_or_none('hjkl')

    text = 'running'

    text_data = wordnet_api.get_data_for_text(text)

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

    if len(text_data['definitions']) > 0:
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

        # Definitions Menu
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

    

    #print(json.dumps(text_data, indent=4, sort_keys=True))
    #senses2 = wordnet_api.get_senses('zzz')


if __name__ == '__main__':
    main()
"""

"""
# submenu_desc is a tuple.
    #   For non-commands (caption, sub_menu_id)
    #   For commands (caption, command)
    def _create_submenu(self, parent_menu: str, submenu_desc: tuple, is_cmd=False, args=None):
        
        Creates a new submenu under the given parent menu.
        
        if parent_menu not in self.menu_entries:
            raise Exception(f"Parent menu {parent_menu} does not exist")
        if is_cmd:
            self.menu_entries[parent_menu]["children"].append({
                "caption": submenu_desc[0],
                "id": submenu_desc,
                # "mnemonic": submenu_desc[0],  # First letter of the caption is the mnemonic for this item
                "children": [] if is_cmd else None,
                # If it has children then it's a menu, otherwise it's a command menu (no children)
                "args": args if args else {}
                # If there are arguments to pass to the command then add them here as a dict. They will be passed to sublime as kwargs when executing the command. Ex: replace word with text="..." new text="..." etc...
            })
        else:
            self.menu_entries[parent_menu]["children"].append({
                "caption": submenu_desc[0],
                "id": submenu_desc,
                # "mnemonic": submenu_desc[0],  # First letter of the caption is the mnemonic for this item
                "children": [] if is_cmd else None,
                # If it has children then it's a menu, otherwise it's a command menu (no children)
                "args": args if args else {}
                # If there are arguments to pass to the command then add them here as a dict. They will be passed to sublime as kwargs when executing the command. Ex: replace word with text="..." new text="..." etc...
            })

"""