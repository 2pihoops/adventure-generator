def define_character(element:str, name:str):
    return f"define {element} = Character(\"{name}\")"

def initialize():
    return """
label start:
"""

def make_choice(choice_node) -> str:
    menu_val = f"""
    "{choice_node._action} has {len(choice_node._children)} choices"
"""
    if len(choice_node._children) == 0:
        menu_val += f"""
    "Terminus = {choice_node._terminus}"
    
    return
"""
        return menu_val

    menu_val +="""
    menu:

        "Decision Time"

"""
    for choice in choice_node._children:
        menu_val += f"""
        "{choice._action}":

            jump {choice._action.replace(" ", "_")}
"""
    for choice in choice_node._children:
        menu_val += f"""
label {choice._action.replace(" ", "_")}:
[[{choice._action}]]"""

    return menu_val


def interpolate_choice(choice_node, story:str) -> str:
    return story.replace(f"[[{choice_node._action}]]", make_choice(choice_node))
