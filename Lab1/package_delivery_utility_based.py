class UtilityBasedDeliveryAgent:
    def __init__(self):
        self.position = 0
        self.has_package = False
        self.package_delivered = False

    def perceive(self, world_state):
        """Perceive the environment"""
        self.world = world_state

    def calculate_utility(self, action):
        """Calculate utility for each possible action"""
        utilities = {
            "move_left": self._utility_move(-1),
            "move_right": self._utility_move(1),
            "pickup_package": self._utility_pickup(),
            "package_delivered": self._utility_deliver(),
            "wait": -10  # Waiting is usually bad
        }
        return utilities.get(action, -100)  # Unknown actions have very low utility

    def _utility_move(self, direction):
        """Calculate utility for moving"""
        new_pos = self.position + direction

        # Check if move is valid
        if new_pos < 0 or new_pos > 10:  # Assuming world bounds
            return -100  # Invalid move

        utility = -1  # Base cost for moving

        if self.has_package:
            # Carrying package - utility based on distance to delivery
            distance_to_delivery = abs(new_pos - self.world.delivery_location)
            utility -= distance_to_delivery * 0.5
            # High reward for getting closer to delivery
            if distance_to_delivery < abs(self.position - self.world.delivery_location):
                utility += 2
        else:
            # Not carrying package - utility based on distance to package
            distance_to_package = abs(new_pos - self.world.package_location)
            utility -= distance_to_package * 0.5
            # High reward for getting closer to package
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
            return 25  # Very high reward for delivery
        return -20  # Penalty for impossible delivery

    def act(self):
        """Choose and execute best action based on utility"""
        possible_actions = ["move_left", "move_right"]

        # Add special actions if conditions are met
        if self.position == self.world.package_location and not self.has_package:
            possible_actions.append("pickup_package")
        if self.position == self.world.delivery_location and self.has_package:
            possible_actions.append("package_delivered")

        # Calculate utilities for all possible actions
        action_utilities = {action: self.calculate_utility(action) for action in possible_actions}

        # Choose action with higher utility
        best_action = max(action_utilities, key=action_utilities.get)
        best_utility = action_utilities[best_action]

        # Execute the action
        if best_action == "move_left":
            self.position -= 1
        elif best_action == "move_right":
            self.position += 1
        elif best_action == "pickup_package":
            self.has_package = True
        elif best_action == "package_delivered":
            self.has_package = False
            self.package_delivered = True

        return best_action, best_utility

    def run(self, world_state, max_steps=20):
        """Run the utility-based agent"""
        self.perceive(world_state)
        print("\nUtility-Based Agent Starting!")
        print(f"Package at: {self.world.package_location}, Deliver to: {self.world.delivery_location}")
        print("=" * 40)

        for step in range(max_steps):
            action, utility = self.act()
            print(
                f"Step {step + 1}: Pos={self.position}, Action={action}, Utility={utility:.1f}, HasPackage={self.has_package}")

            if self.package_delivered:
                print("Package delivered successfully!")
                return True

        print("Failed to deliver package")
        return False

class WorldState:
    def __init__(self, package_loc, delivery_loc):
        self.package_location = package_loc
        self.delivery_location = delivery_loc

# Test Utility-Based Agent
print("\n" + "=" * 50)
print("UTILITY-BASED AGENT DEMONSTRATION")
world = WorldState(package_loc=3, delivery_loc=6)
utility_agent = UtilityBasedDeliveryAgent()
utility_agent.run(world)