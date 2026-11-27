"""Small, explicitly allowlisted local tool registry. No arbitrary command execution."""
from datetime import datetime, timezone
import ast, operator

_ALLOWED={
 ast.Add:operator.add, ast.Sub:operator.sub, ast.Mult:operator.mul,
 ast.Div:operator.truediv, ast.FloorDiv:operator.floordiv, ast.Mod:operator.mod,
 ast.Pow:operator.pow, ast.USub:operator.neg, ast.UAdd:operator.pos
}
def _calc_node(node):
 if isinstance(node,ast.Constant) and isinstance(node.value,(int,float)): return node.value
 if isinstance(node,ast.BinOp) and type(node.op) in _ALLOWED:
  if isinstance(node.op,ast.Pow) and abs(node.right.value if isinstance(node.right,ast.Constant) else 999)>8: raise ValueError("Exponent too large")
  return _ALLOWED[type(node.op)](_calc_node(node.left),_calc_node(node.right))
 if isinstance(node,ast.UnaryOp) and type(node.op) in _ALLOWED: return _ALLOWED[type(node.op)](_calc_node(node.operand))
 raise ValueError("Only basic arithmetic is supported.")
def calculate(expression):
 if len(expression)>120: raise ValueError("Expression is too long.")
 tree=ast.parse(expression,mode="eval")
 result=_calc_node(tree.body)
 if abs(result)>1e100: raise ValueError("Result outside supported range.")
 return {"expression":expression,"result":result}
def current_time():
 return {"utc":datetime.now(timezone.utc).isoformat(),"note":"UTC timestamp"}
def list_tools():
 return [
  {"name":"calculator","description":"Evaluate a basic arithmetic expression safely.","risk":"read-only","confirmation_required":False,"input_schema":{"expression":"string"}},
  {"name":"current_time","description":"Get the current UTC timestamp.","risk":"read-only","confirmation_required":False,"input_schema":{}}
 ]
def execute_tool(name,args):
 if name=="calculator":
  if not isinstance(args,dict) or not isinstance(args.get("expression"),str): raise ValueError("expression string is required")
  return calculate(args["expression"])
 if name=="current_time":
  return current_time()
 raise KeyError("Tool not found or not enabled.")
