import random
class PackageDelivery:
    def __init__(self):
        self.has_package = False
        self.package_delivered = False
        self.current_goal = "find_package"
        

    def percieve(self, status):
        self.world = status

    def act(self):
        if self.current_goal == "find_package":
            return self.achieve_find_and_deliver_package()
        elif self.current_goal == "pickup_package":
            return self.achieve_pickup_package()
        elif self.current_goal == "deliver_package":
            return self.achieve_find_and_deliver_package()
    def achieve_find_and_deliver_package(self):
        if not self.has_package:

            if self.world.agent_loc == self.world.package_loc:
                self.current_goal = "pickup_package"
                return "find_package"
            else:
                if self.world.agent_loc < self.world.package_loc:
                    self.world.agent_loc += 1
                    return "move_right"
                else:
                    self.world.agent_loc -= 1
                    return "move_left"
        else:
            if self.world.agent_loc == self.world.delivery_loc:
                self.current_goal = "complete"
                self.package_delivered = True
                self.has_package = False
                return "deliver_package"
            else:
                if self.world.agent_loc < self.world.delivery_loc:
                    self.world.agent_loc += 1
                    return "move_right"
                else:
                    self.world.agent_loc -= 1
                    return "move_left"

    def achieve_pickup_package(self):
        if self.world.agent_loc == self.world.package_loc:
            self.has_package = True
            self.current_goal = "deliver_package"
            return "pickup_package"
        else:
            self.current_goal = "find_package"
            return "re-plan"

    def run(self, status):
        self.percieve(status)
        print("Goal-Based Agent Starting!")
        print(f"Agent Location: {self.world.agent_loc}")
        print(f"Package at: {self.world.package_loc}, Deliver to: {self.world.delivery_loc}")
        print("=" * 40)
        step = 0
        while True:
           action = self.act()
           print(f"Step {step + 1}: Pos={self.world.agent_loc}, Action={action}, Goal={self.current_goal}")
           step += 1
           if self.package_delivered:
               print("Package delivered successfully!")
               return True

class WorldStatus:
    def __init__(self, agent_loc, package_loc, delivery_loc):
        self.agent_loc = agent_loc
        self.package_loc = package_loc
        self.delivery_loc = delivery_loc

agent = int(input("enter agent location: "))
package = int(input("enter package location: "))
deliver = int(input("enter deliver location: "))

if package == deliver:
    print("invalid")
else:
    ws = WorldStatus(agent_loc=agent, package_loc=package, delivery_loc=deliver)

    package_delivery = PackageDelivery()
    package_delivery.run(ws)