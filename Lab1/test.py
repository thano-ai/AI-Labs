import random
class PackageDelivery:
    def __init__(self):
        self.position = 0
        self.has_package = False
        self.package_delivered = False

    def perceive(self, world_status):
        self.world = world_status

    def calculate_utility(self, action):
        utilities = {
            "move_left": self._utility_move(-1),
            "move_right": self._utility_move(1),
            "pickup_package": self._utility_pickup(),
            "package_delivered": self._utility_deliver(),
        }
        return utilities.get(action, -100)  # Unknown actions have very low utility

    def _utility_move(self, direction):
        new_pos = self.position + direction

        if new_pos < 0 or new_pos > 10:
            return "invalid move"

        utility = -1

        if self.has_package:
            distance_to_deliver = abs(new_pos - self.world.delivery_location)
            utility -= distance_to_deliver * 0.5
            if distance_to_deliver < abs(self.position - self.world.delivery_location):
                utility += 2
        else:
            distance_to_package = abs(new_pos - self.world.package_location)
            utility -= distance_to_package * 0.5
            if distance_to_package < abs(self.position - self.world.package_location):
                utility += 2

        return utility

    def _utility_pickup(self):
        """Calculate utility for picking up package"""
        if (not self.has_package and
                self.position == self.world.package_location):
            return 10  # High reward for successful pickup
        return -10  # Penalty for impossible pickup

    def _utility_deliver(self):
        """Calculate utility for delivering package"""
        if (self.has_package and
                self.position == self.world.delivery_location):
            return 20  # Very high reward for delivery
        return -20  # Penalty for impossible delivery

    def act(self):




    def run(self, world_status, steps=21):
        self.perceive(world_status)
        print("Goal-Based Agent Starting!")
        print(f"Package at: {self.world.package_location}, Deliver to: {self.world.delivery_location}")
        print("=" * 40)
        print(self.position)
        for step in range(steps):
            action = self.act()

            print(f"Step {step + 1}: Pos={self.position}, Action={action}, Goal={self.current_goal}")

            if self.package_delivered:
                print("Package delivered successfully!")
                return True

        print("Failed to deliver package")
        return False

class WorldStatus:
    def __init__(self, package_loc, delivery_loc):
        self.package_location = package_loc
        self.delivery_location = delivery_loc

ws = WorldStatus(package_loc=9, delivery_loc=0)
package_delivery = PackageDelivery()
package_delivery.run(ws)

