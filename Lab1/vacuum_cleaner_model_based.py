import random


class ModelBasedVacuumCleaner:
    def __init__(self):
        self.rooms = {
            "A": random.choice(["clean", "dirty"]),
            "B": random.choice(["clean", "dirty"])
        }
        self.location = random.choice(["A", "B"])

        # INTERNAL MODEL - This is what makes it model-based
        self.world_model = {
            "A": "unknown",  # Initially doesn't know room status
            "B": "unknown"
        }
        self.visited_rooms = set()  # Track which rooms have been visited

        self.perceive()  # update the agent view before cleaning

    def perceive(self):
        # Update internal model with current perception
        actual_status = self.rooms[self.location]
        self.world_model[self.location] = actual_status
        self.visited_rooms.add(self.location)
        return actual_status

    def suck(self):
        if self.perceive() == "dirty":
            print(f"Cleaning Room {self.location}")
            self.rooms[self.location] = "clean"
            self.world_model[self.location] = "clean"  # Update model

    def move_to(self, new_location):
        print(f"Moving from {self.location} to {new_location}")
        self.location = new_location

    def act(self):
        current_status = self.perceive()

        # Use internal model to make smarter decisions
        if current_status == "dirty":
            self.suck()
        else:
            # SMART DECISION: Check model for uncleaned rooms
            if self.should_continue_cleaning():
                other_room = "B" if self.location == "A" else "A"
                self.move_to(other_room)
            else:
                print("All known rooms are clean - stopping or waiting")

    def should_continue_cleaning(self):
        """Check if there might be dirty rooms based on internal model"""
        # If any room is unknown or known to be dirty, continue
        for room, status in self.world_model.items():
            if status == "unknown" or status == "dirty":
                return True
        return False

    def run(self, steps=10):
        print("Initial Status:")
        print(f"Room A is {self.rooms['A']} (Agent knows: {self.world_model['A']})")
        print(f"Room B is {self.rooms['B']} (Agent knows: {self.world_model['B']})")
        print(f"Starting in Room {self.location}")
        print("=" * 40)

        for step in range(steps):
            print(f"\nStep {step + 1}")
            print(f"Internal Model: {self.world_model}")
            self.act()

            # Check actual world state
            # if all(status == "clean" for status in self.rooms.values()):
            #     print("\n All rooms are actually clean!")
            #     break
            # Check if agent believes all rooms are clean
            if all(status == "clean" for status in self.world_model.values()):
                print(f"Internal Model: {self.world_model}")
                print("\n Agent believes all rooms are clean (based on its model)")
                break


# Test both versions for comparison
print("=== MODEL-BASED AGENT ===")
model_agent = ModelBasedVacuumCleaner()
model_agent.run()
