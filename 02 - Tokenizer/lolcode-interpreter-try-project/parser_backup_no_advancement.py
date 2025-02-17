from lexer import *

#################################
class Error:
  def __init__(self, token, details, error_name):
    self.token = token
    self.details = details
    self.error_name = error_name
  def as_string(self):
    return f"{self.error_name}: '{self.token[TOKEN_VALUE]}' at line {self.token[TOKEN_LINE_NUMBER]}\nDetails: {self.details}\n"

class InvalidSyntaxError(Error):
  def __init__(self, token, details):
    super().__init__(token, details, error_name='Invalid Syntax')


class RuntimeError(Error):
  def __init__(self, token, details):
    super().__init__(token, details, error_name='Runtime Error')

#######################################
# NODES
#######################################
class IntegerNode:
  def __init__(self, token):
    self.token = token

  def __repr__(self):
    return f'{self.token[TOKEN_VALUE]}'

class FloatNode:
  def __init__(self, token):
    self.token = token

  def __repr__(self):
    return f'{self.token[TOKEN_VALUE]}'

class ArithmeticBinaryOpNode:
  def __init__(self, left_node, operation, right_node):
    self.operation = operation
    self.left_node = left_node
    self.right_node = right_node

  def __repr__(self):
    return f'{self.operation[TOKEN_VALUE]}({self.left_node}, {self.right_node})'

class VarAccessNode:
  def __init__(self, var_name_token):
    self.var_name_token = var_name_token

  def __repr__(self):
    return f"VarAccess({self.var_name_token[TOKEN_VALUE]})"

class VarAssignNode:
  def __init__(self, var_name_token, value_node):
    self.var_name_token = var_name_token
    self.value_node = value_node

  def __repr__(self):
    return f"VarAssign({self.var_name_token[TOKEN_VALUE]}, {self.value_node})"

#######################################
# PARSE RESULT
#######################################
class ParseResult:
  def __init__(self):
    self.error = None
    self.node = None

  def register(self, res):
    if isinstance(res, ParseResult):
      if res.error: self.error = res.error
      return res.node
    return res

  def success(self, node):
    self.node = node
    return self

  def failure(self, error):
    if self.error is None: self.error = error
    return self
  
#######################################
# PARSER
#######################################

class Parser:
  def __init__(self, tokens):
    self.tokens = tokens
    self.token_index = -1
    self.advance()

  def advance(self):
    self.token_index += 1
    if (self.token_index < len(self.tokens)):
      self.current_token = self.tokens[self.token_index]
    return self.current_token

  def parse(self):
    res = self.expr()

    # Unparsed tokens
    if res is None or (not res.error and self.current_token[TOKEN_TAG] != EOF):
      return ParseResult().failure(InvalidSyntaxError(self.current_token, 'Unexpected Syntax'))
    return res


  def expr(self):
    if self.current_token[TOKEN_TAG] in (PRODUKT_OF, QUOSHUNT_OF, SUM_OF, DIFF_OF, BIGGR_OF, SMALLR_OF):
      return self.arithmetic_binary_operation()

    elif self.current_token[TOKEN_TAG] in (NUMBR, NUMBAR):
      return self.atom()

    elif self.current_token[TOKEN_TAG] in (I_HAS_A):
      return self.variable_declaration()

  def variable_declaration(self):
    res = ParseResult()

    if self.current_token[TOKEN_TAG] in (I_HAS_A):
      res.register(self.advance()) # eats I has a

      if (self.current_token[TOKEN_TAG] != IDENTIFIER):
        return res.failure(InvalidSyntaxError(self.current_token, "Expected Identifier!"))

      var_name_token = self.current_token
      res.register(self.advance()) # eats var name
      
      if (self.current_token[TOKEN_TAG] != ITZ):
        return res.failure(InvalidSyntaxError(self.current_token, "Expected 'ITZ'!"))

      res.register(self.advance()) # eats ITZ

      expr = res.register(self.expr())
      if res.error: return res

      return res.success(VarAssignNode(var_name_token, expr))

  def arithmetic_binary_operation(self):
    res = ParseResult()
    
    if self.current_token[TOKEN_TAG] in (PRODUKT_OF, QUOSHUNT_OF, SUM_OF, DIFF_OF, BIGGR_OF, SMALLR_OF):
      operation = self.current_token
      res.register(self.advance())
      
      # Parse the left operand
      left = res.register(self.arithmetic_factor())  # Recursive call to handle the left side
      if res.error: return res

      # check for 'AN' keyword 
      if self.current_token[TOKEN_TAG] != AN:
          # print(self.current_token[TOKEN_VALUE])
          return res.failure(InvalidSyntaxError(self.current_token, "Expected an 'AN' keyword!"))
          
      # Advance past the 'AN' keyword
      res.register(self.advance())

      # Parse the right operand which may also be an expression
      right = res.register(self.arithmetic_factor())  # Recursive call to handle right side
      if res.error: return res

      # Return an operation node with left and right operands
      return res.success(ArithmeticBinaryOpNode(left, operation, right))

  def arithmetic_factor(self):
    res = ParseResult()
    token = self.current_token

    if token[TOKEN_TAG] in (NUMBR, NUMBAR):
      return res.register(self.atom())
    
    elif token[TOKEN_TAG] in (PRODUKT_OF, QUOSHUNT_OF, SUM_OF, DIFF_OF, BIGGR_OF, SMALLR_OF):
      return res.register(self.arithmetic_binary_operation())

  def atom(self):
    res = ParseResult()
    token = self.current_token

    if token[TOKEN_TAG] in (NUMBR, NUMBAR):
      res.register(self.advance())
      
      if token[TOKEN_TAG] == NUMBR:
        return res.success(IntegerNode(token))
      else:
        return res.success(FloatNode(token))

    elif token[TOKEN_TAG] == IDENTIFIER:
      res.register(self.advance())
      return res.success(VarAccessNode(token))

    return res.failure(InvalidSyntaxError(token, 'Expected int or float!'))
  

#######################################
# RUNTIME RESULT
#######################################
class RTResult:
  def __init__(self):
    self.value = None
    self.error = None
  
  def register(self, res):
    if res.error: self.error = res.error
    return res.value
  
  def success(self, value):
    self.value = value
    return self
  
  def failure(self, error):
    self.error = error
    return self

#######################################
# VALUES
#######################################
class Number:
  def __init__(self, value, line_number=None):
    self.value = value
    self.line_number = line_number
    self.set_context()

  def set_context(self, context=None):
    self.context = context
    return self

  def added_by(self, other):
    if isinstance(other, Number):
      return Number(self.value + other.value).set_context(self.context) , None

  def subtracted_by(self, other):
    if isinstance(other, Number):
      return Number(self.value - other.value).set_context(self.context) , None
  
  def multiplied_by(self, other):
    if isinstance(other, Number):
      return Number(self.value * other.value).set_context(self.context) , None
  
  def divided_by(self, other):
    if isinstance(other, Number):
      if other.value == 0:
        return None, RuntimeError(
          ('Result is Zero', None, other.line_number), 'Division by Zero'
        )
      return Number(self.value / other.value).set_context(self.context) , None
  
  def greater_than(self, other):
    if isinstance(other, Number):
      return Number(max(self.value, other.value)).set_context(self.context) , None

  def less_than(self, other):
    if isinstance(other, Number):
      return Number(min(self.value, other.value)).set_context(self.context) , None

  def __repr__(self):
    return str(self.value)
  
#######################################
# CONTEXT
#######################################
class Context:
  def __init__(self, display_name, parent=None, parent_entry_pos=None):
    self.display_name = display_name
    self.parent = parent
    self.parent_entry_pos = parent_entry_pos
    self.symbol_table = None

#######################################
# SYMBOL_TABLE
#######################################
class SymbolTable:
  def __init__(self):
    self.symbols = {}
    self.parent = None # For functions (definitions/calls)
  
  def get(self, name):
    value = self.symbols.get(name, None)
    if value == None and self.parent:
      return self.parent.get(name)
    return value

  def set(self, name, value):
    self.symbols[name] = value

  def remove(self, name):
    del self.symbols[name]

#######################################
# INTERPRETER
#######################################
class Interpreter:
  def visit(self, node, context):
    method_name = f'visit_{type(node).__name__}'
    method = getattr(self, method_name, self.no_visit_method)
    return method(node, context)
  
  def no_visit_method(self, node, context):
    raise Exception(f'No visit_{type(node).__name__} method defined')
  
  def visit_IntegerNode(self, node, context):
    # print("Found integer node")
    return RTResult().success(
      Number(int(node.token[TOKEN_VALUE]), node.token[TOKEN_LINE_NUMBER])
    )
  
  def visit_FloatNode(self, node, context):
    # print("Found float node")
    return RTResult().success(
      Number(float(node.token[TOKEN_VALUE]), node.token[TOKEN_LINE_NUMBER])
    )
  
  def visit_ArithmeticBinaryOpNode(self, node, context):
    # print("Found ar bin op node")
    res = RTResult()
    left = res.register(self.visit(node.left_node, context))
    if res.error: return res
    right = res.register(self.visit(node.right_node, context))
    if res.error: return res

    if node.operation[TOKEN_TAG] == SUM_OF:
      result, error = left.added_by(right)

    elif node.operation[TOKEN_TAG] == DIFF_OF:
      result, error = left.subtracted_by(right)
    
    elif node.operation[TOKEN_TAG] == PRODUKT_OF:
      result, error = left.multiplied_by(right) 

    elif node.operation[TOKEN_TAG] == QUOSHUNT_OF:
      result, error = left.divided_by(right)
    
    elif node.operation[TOKEN_TAG] == BIGGR_OF:
      result, error = left.greater_than(right)
    
    elif node.operation[TOKEN_TAG] == SMALLR_OF:
      result, error = left.less_than(right)

    if (error):
      return res.failure(error)
    else:
      # print(result)
      return res.success(result)

  def visit_VarAccessNode(self, node, context):
    res = RTResult()
    var_name = node.var_name_token[TOKEN_VALUE]

    value = res.register(self.visit(node.value_node, context))

    if not value:
      return res.failure(RuntimeError(node.var_name_token, f"'{var_name} is not defined!'"))
    
    return res.success(value)

  def visit_VarAssignNode(self, node, context):
    res = RTResult()
    var_name = node.var_name_token[TOKEN_VALUE]

    value = res.register(self.visit(node.value_node, context))
    if res.error: return res

    context.symbol_table.set(var_name, value)
    return res.success(value)