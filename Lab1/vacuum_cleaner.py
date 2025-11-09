import random

class VacuumCleaner:
    def __init__(self):
        self.rooms = {
            "A": random.choice(["clean", "dirty"]) ,
            "B": random.choice(["clean", "dirty"])
        }

        self.location = random.choice(["A", "B"])

    def perceive(self):
        return self.rooms[self.location]

    def suck(self):
        if self.perceive() == "dirty":
            print(f"Cleaning Room {self.location}")
            self.rooms[self.location] = "clean"

    def move_to(self, new_location):
        print(f"Moving from {self.location} to {new_location}")
        self.location = new_location

    def act(self):
        if self.perceive() == "dirty":
            self.suck()
        else:
            other_room = "B" if self.location == "A" else "A"
            self.move_to(other_room)


    def run(self, steps=10):
        print("Initial Status:")
        print(f"Room A is {self.rooms['A']}")
        print(f"Room B is {self.rooms['B']}")
        print(f"Starting in Room {self.location}")
        print("="*30)

        for step in range(steps):
            print(f"Step {step+1}")
            self.act()

            # if all(status == "clean" for status in self.rooms.values()):
            #     print("All rooms are clean !")
            #     break


vacuum_cleaner = VacuumCleaner()
vacuum_cleaner.run()

