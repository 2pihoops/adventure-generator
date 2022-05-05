import random


class Choice:
    _parent = None
    _children = []
    _element = -1
    _action = ""

    def __init__(self, parent, children, element, action):
        self._parent = parent
        self._children = children
        self._element = element
        self._action = action

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
        #if self._parent:
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

    def __str__(self):
        val = self._action + " @ " + str(self.get_parent_element()) + " of " + str(len(self.get_parent_choices())) + "\n"
        "blah"
        for child in self._children:
            val += "-" * self.get_depth() + "> " + str(child)
        return val


MAX_CHOICES = 4
MIN_CHOICES = 2
TREE_SIZE = 20


def validate_choice(choice: Choice):
    if choice.get_choices() is not None and len(choice.get_choices()) >= MAX_CHOICES:
        return False
    else:
        return True


def choose_wisely(choices: []):
    choice_count = len(choices)
    random_choice_number = random.choice(range(choice_count))
    for i in range(choice_count):
        if validate_choice(choices[random_choice_number]):
            return random_choice_number
        elif random_choice_number + i > choice_count:
            random_choice_number = choice_count % (random_choice_number + i)
        else:
            random_choice_number = random_choice_number + i

    return None


def generate(size):
    entrypoint = Choice(None, [], 0, "0")
    choices = [entrypoint]
    for i in range(1, size):
        next_parent_index = choose_wisely(choices)
        if next_parent_index is None:
            break
        parent_choice = choices[next_parent_index]
        new_choice = Choice(parent_choice, [], i, "Do " + str(i))
        parent_choice.add_choice(new_choice)
        choices.append(new_choice)
    return entrypoint


choice_tree = generate(TREE_SIZE)
print(choice_tree)
