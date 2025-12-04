import ast
import astor
import uuid
import json

class StepInjector(ast.NodeTransformer):
    def __init__(self):
        super().__init__()

    def visit_Assign(self, node):
        new_node = self.generic_visit(node)
        return [
            new_node,
            ast.parse(f"print(json.dumps({{'event': 'assign', 'target': '{node.targets[0].id}'}}))").body[0]
        ]

def instrument(file_path, output_path):
    with open(file_path, "r") as f:
        tree = ast.parse(f.read())

    injector = StepInjector()
    new_tree = injector.visit(tree)
    ast.fix_missing_locations(new_tree)

    with open(output_path, "w") as f:
        f.write("import json\n")
        f.write(astor.to_source(new_tree))

    return output_path
