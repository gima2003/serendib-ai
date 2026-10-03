import ast
with open("services/destination/destination_recommender.py", encoding="utf-8") as f:
    code = f.read()
module = ast.parse(code)
for node in module.body:
    if isinstance(node, ast.FunctionDef) and node.name == "recommend_from_preferred_destinations":
        print(ast.unparse(node))
