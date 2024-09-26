import json

class Node:
    def __init__(self, question=None, animal=None):
        self.question = question
        self.animal = animal
        self.y = None
        self.n = None

class AnimalGame:
    def __init__(self, filename='animal_game.json'):
        self.filename = filename
        self.root = Node("Он большой?")
        self.load_game()

    def save_game(self):
        data = self._serialize(self.root)
        with open(self.filename, 'w') as f:
            json.dump(data, f)

    def load_game(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.root = self._deserialize(data)
        except FileNotFoundError:
            pass

    def _serialize(self, node):
        if node is None:
            return None
        return {
            'question': node.question,
            'animal': node.animal,
            'y': self._serialize(node.y),
            'n': self._serialize(node.n),
        }

    def _deserialize(self, data):
        if data is None:
            return None
        node = Node(data['question'], data['animal'])
        node.y = self._deserialize(data['y'])
        node.n = self._deserialize(data['n'])
        return node

    def play(self):
        current_node = self.root
        while current_node.animal is None:
            answer = input(current_node.question + " (y/n): ").lower()
            if answer == 'y':
                current_node = current_node.y
            else:
                current_node = current_node.n

        guess = input(f"Это {current_node.animal}? (y/n): ").lower()
        if guess == 'n':
            new_animal = input("Какое животное вы загадали? ")
            new_question = input(f"А чем отличается {new_animal} от {current_node.animal}? ")
            new_node = Node(new_question, new_animal)
            if answer == 'y':
                new_node.y = current_node
                new_node.n = Node()
            else:
                new_node.y = Node()
                new_node.n = current_node
            current_node.question = new_question
            current_node.animal = None
            current_node.y = new_node.y
            current_node.n = new_node.n

        self.save_game()
        print("Спасибо за игру!")

if __name__ == "__main__":
    game = AnimalGame()
    game.root.y = Node("Он большой?", "Слон")
    game.root.n = Node("Он большой?", "Мышь")
    game.play()