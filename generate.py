import random
import renblah
from pathlib import Path

class Choice:
    _parent = None
    _children = []
    _element = -1
    _action = ""
    _terminus = False

    def __init__(self, parent, children, element, action, terminus):
        self._parent = parent
        self._children = children
        self._element = element
        self._action = action
        self._terminus = terminus

    def get_element(self):
        return self._element

    def get_parent_element(self):
        if self._parent:
            return self._parent.get_element()
        else:
            return "start"

    def get_parent_choices(self):
        if self._parent:
            return self._parent.get_choices()
        else:
            return []

    def get_choices(self):
        choices = self._children
        # if self._parent:
        #    choices.append(self._parent)
        return choices

    def add_choice(self, choice):
        self._children.append(choice)

    def get_depth(self):
        i = 0
        node = self
        while node._parent is not None:
            node = node._parent
            i += 1
        return i

    def get_terminal(self):
        return self._terminus

    def get_dead_end(self):
        return len(self._children) == 0

    def __str__(self):
        val = self._action + " @ " + str(self.get_parent_element()) + " of " + str(
            len(self.get_parent_choices())) + "\n"
        for child in self._children:
            val += "-" * self.get_depth() + "> "
            if child.get_dead_end():
                val += "(D) "
            if child.get_terminal():
                val += "(T) "
            val += str(child)
        return val


MAX_CHOICES = 4
MIN_CHOICES = 2
TREE_SIZE = 20
MAX_DEPTH = 5


def validate_choice(choice: Choice):
    if (choice.get_choices() is not None and len(choice.get_choices()) >= MAX_CHOICES) or choice.get_terminal():
        return False
    else:
        return True


def choose_wisely(choices: []):
    choice_count = len(choices)
    random_choice_number = random.choice(range(choice_count))
    for i in range(choice_count):
        if validate_choice(choices[random_choice_number - 1]):
            return random_choice_number
        elif random_choice_number + i > choice_count:
            random_choice_number = choice_count % (random_choice_number + i)
        else:
            random_choice_number = random_choice_number + i

    return None


def generate(size):
    entrypoint = Choice(None, [], 0, "0", False)
    choices = [entrypoint]
    margin = 0
    i = 1
    while i <= size + margin:
        next_parent_index = choose_wisely(choices)
        if next_parent_index is None:
            break
        parent_choice = choices[next_parent_index - 1]
        terminus = False
        if parent_choice.get_depth() >= MAX_DEPTH - 1:
            terminus = True
        new_choice = Choice(parent_choice, [], i, "Do " + str(i), terminus)
        parent_choice.add_choice(new_choice)
        choices.append(new_choice)

        if i == size + margin:
            if not validate_tree(entrypoint, choices):
                margin += 1
        i += 1

    return (entrypoint, choices)


def validate_tree(entrypoint: Choice, choices: list) -> bool:
    # Must be at least one terminator
    terminates = False
    for choice in choices:
        if terminates:
            break
        else:
            if choice.get_terminal():
                terminates = True
    return terminates

def make_renpy(entrypoint: Choice, choices: list):
    story = ""
    story += renblah.define_character("s", "Robot")
    story += renblah.initialize()
    story += renblah.make_choice(entrypoint)
    while "[[" in story:
        for choice in choices:
            story = renblah.interpolate_choice(choice, story)
    Path("script.rpy").write_text(story)


(choice_tree, choices) = generate(TREE_SIZE)
print(choice_tree)
make_renpy(choice_tree, choices)

#choice = Choice(None, [], 0, "choice", True)
#test_story = "[[choice]]"
#print(test_story)
#print(choice)
#print(choice._action)
#print(renblah.interpolate_choice(choice, test_story))
