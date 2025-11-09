class GoalBasedDeliveryAgent:
    def __init__(self):
        self.position = 0
        self.has_package = False
        self.package_delivered = False
        self.current_goal = "find_package"

    def perceive(self, world_state):
        """Perceive the environment"""
        self.world = world_state

    def act(self):
        """Take action based on current goal"""
        if self.current_goal == "find_package":
            return self._achieve_find_package()
        elif self.current_goal == "pickup_package":
            return self._achieve_pickup_package()
        elif self.current_goal == "package_delivered":
            return self._achieve_deliver_package()
        elif self.current_goal == "complete":
            return "task_complete"

    def _achieve_find_package(self):
        """Work toward finding the package"""
        if self.position == self.world.package_location:
            self.current_goal = "pickup_package"
            return "arrived_at_package"
        else:
            # Move toward package
            if self.position < self.world.package_location:
                self.position += 1
                return "move_right"
            else:
                self.position -= 1
                return "move_left"

    def _achieve_pickup_package(self):
        """Work toward picking up package"""
        if self.position == self.world.package_location:
            self.has_package = True
            self.current_goal = "package_delivered"
            return "pickup_package"
        else:
            # Shouldn't happen if planning is correct
            self.current_goal = "find_package"
            return "re-plan"

    def _achieve_deliver_package(self):
        """Work toward delivering package"""
        if self.position == self.world.delivery_location:
            self.has_package = False
            self.package_delivered = True
            self.current_goal = "complete"
            return "package_delivered"
        else:
            # Move toward delivery location
            if self.position < self.world.delivery_location:
                self.position += 1
                return "move_right"
            else:
                self.position -= 1
                return "move_left"

    def run(self, world_state, max_steps=20):
        """Run the goal-based agent"""
        self.perceive(world_state)
        print("Goal-Based Agent Starting!")
        print(f"Package at: {self.world.package_location}, Deliver to: {self.world.delivery_location}")
        print("=" * 40)

        for step in range(max_steps):
            action = self.act()
            print(f"Step {step + 1}: Pos={self.position}, Action={action}, Goal={self.current_goal}")

            if self.package_delivered:
                print("Package delivered successfully!")
                return True

        print("Failed to deliver package")
        return False


# World state for goal-based agent
class WorldState:
    def __init__(self, package_loc, delivery_loc):
        self.package_location = package_loc
        self.delivery_location = delivery_loc


# Test Goal-Based Agent
print("GOAL-BASED AGENT DEMONSTRATION")
world = WorldState(package_loc=-2, delivery_loc=2)
goal_agent = GoalBasedDeliveryAgent()
goal_agent.run(world)