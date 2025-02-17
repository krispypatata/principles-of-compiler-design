from equality import *

class Statement(Equality):
    pass

class ArithmeticExpression(Equality):
    pass

class BooleanExpression(Equality):
    pass

# ========================================================================================
# PRIMITIVES
class Integer:
    def __init__(self, i):
        self.i = i

    def __repr__(self):
        return 'Integer(%d)' % self.i

    def eval(self, env):
        return self.i

class Float:
    def __init__(self, i):
        self.i = i

    def __repr__(self):
        return 'Float(%d)' % self.i

    def eval(self, env):
        return self.i

class Boolean:
    def __init__(self, i):
        self.i = i

    def __repr__(self):
        return 'Boolean(%d)' % self.i

    def eval(self, env):
        return self.i

class String():
    def __init__(self, i):
        self.i = i
    
    def __repr__(self):
        return f'Identifier({self.i})'

    def eval(self, env):
        return self.i    
    
class Identifier():
    def __init__(self, i):
        self.i = i

    def __repr__(self):
        return f'Identifier({self.i})'

    def eval(self, env):
        return self.i
# ========================================================================================


class Program:
    def __init__(self, varsection, body):
        self.varsection = varsection
        self.body = body

    def __repr__(self):
        return f'Program({self.varsection}, {self.body})'

    def eval(self, env):
        if self.varsection:
            self.varsection.eval(env)  # Evaluate the variable declarations (if present)
        # self.body.eval(env)  # Evaluate the statements in the body
        for statement in self.body:
            statement.eval(env)


class PrintStatement(Statement):
    def __init__(self, expression):
        self.expression = expression  # The expression to print

    def __repr__(self):
        return f'PrintStatement({self.expression})'

    def eval(self, env):
        # Case 1: If the expression is a BinaryOperationAE (like SUM OF 2 AN 4)
        if isinstance(self.expression, BinaryOperationAE):
            result = self.expression.eval(env)  # Evaluate the expression (SUM OF, etc.)
            print(result)  # Print the result of the operation
            return  # Exit the function early since we've printed the result

        # Case 2: If the expression is a literal string (like "Hello World")
        if isinstance(self.expression, String):
            print(self.expression.eval(None)[1:-1])  # Print the literal string directly
            return  # Exit the function early

        # Case 3: If the expression is an identifier (like a variable name)
        if isinstance(self.expression, Identifier):
            if self.expression.eval(None) in env:
                print(env[self.expression.eval(None)])  # Print the value from the environment
            else:
                raise NameError(f"Identifier '{self.expression.eval(None)}' is not defined.")
            return  # Exit the function early

        # Case 4: If it's a direct value (e.g., number, float), print it directly
        print(self.expression.eval(None))


class VariableSection(Statement):
    def __init__(self, declarations):
        self.declarations = declarations

    def __repr__(self):
        return 'VariableSection(%s)' % self.declarations

    def eval(self, env):
        for declaration in self.declarations:
            declaration.eval(env)

class VariableDeclaration(Statement):
    def __init__(self, name, initial_value=None):
        self.name = name.eval(None)
        self.initial_value = initial_value

    def __repr__(self):
        return 'VariableDeclaration(%s, %s)' % (self.name, self.initial_value)

    def eval(self, env):
        if self.initial_value is not None:
            env[self.name] = self.initial_value.eval(env)  # Store variable in environment
        else:
            env[self.name] = None  # Default to None

class CompoundStatement(Statement):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return 'CompoundStatement(%s, %s)' % (self.first, self.second)
    
    def eval(self, env):
        self.first.eval(env)
        self.second.eval(env)

class BinaryOperationAE:
    def __init__(self, operation, left, right):
        self.operation = operation  # This stores the full operation keyword (e.g., "SUM OF")
        self.left = left
        self.right = right

    def __repr__(self):
        return f'BinaryOperationAE({self.operation}, {self.left}, {self.right})'

    def eval(self, env):
        # Initialize result to None
        result = None

        # Evaluate left and right, handling literals or identifiers
        left_value = self.left.eval(None) if not isinstance(self.left, Identifier) else env.get(self.left.eval(None), None)
        right_value = self.right.eval(None) if not isinstance(self.right, Identifier) else env.get(self.right.eval(None), None)

        # Now handle the operation
        if self.operation == "SUM OF":
            result = left_value + right_value
        elif self.operation == "DIFF OF":
            result = left_value - right_value
        elif self.operation == "PRODUKT OF":
            result = left_value * right_value
        elif self.operation == "QUOSHUNT OF":
            result = left_value / right_value
        elif self.operation == "MOD OF":
            result = left_value % right_value
        elif self.operation == "BIGGR OF":
            result = max(left_value, right_value)
        elif self.operation == "SMALLR OF":
            result = min(left_value, right_value)
        else:
            raise RuntimeError(f'Unknown operation: {self.operation}')

        # Store the result in the temporary 'IT' variable
        env['IT'] = result
        return result

class BooleanBinaryOperationAE(BinaryOperationAE):
    def __init__(self, operation, left, right=None):
        self.operation = operation
        self.left = left
        self.right = right

    def __repr__(self):
        if self.operation == "NOT":
            return 'BooleanBinaryOperationAE(%s, %s)' % (self.operation, self.left)

        return 'BooleanBinaryOperationAE(%s, %s, %s)' % (self.operation, self.left, self.right)

    def eval(self, env):
        # Initialize result to None
        result = None

        left_value = self.left.eval(None)
        right_value = self.right.eval(None) if self.right is not None else None

        if self.operation == "BOTH OF":
            result = left_value and right_value
        elif self.operation == "EITHER OF":
            result = left_value or right_value
        elif self.operation == "WON OF":
            result = left_value ^ right_value
        elif self.operation == "NOT":
            result = not left_value
        else:
            raise RuntimeError(f'Unknown operation: {self.operation}')
        
        # Store the result in the temporary 'IT' variable
        env['IT'] = result
        return result


class IfStatement(Statement):
    def __init__(self, condition, true_statement, false_statement):
        self.condition = condition
        self.true_statement = true_statement
        self.false_statement = false_statement

    def __repr__(self):
        return 'IfStatement(%s, %s, %s)' % (self.condition, self.true_statement, self.false_statement)

    def eval(self, env):
        condition_value = self.condition.eval(env)
        if condition_value:
            self.true_statement.eval(env)
        else:
            if self.false_statement:
                self.false_statement.eval(env)


class FunctionDefinition(Statement):
    def __init__(self, name, parameters, body):
        self.name = name          # The name of the function
        self.parameters = parameters  # List of parameter names
        self.body = body          # The body of the function (usually a statement or expression)

    def __repr__(self):
        return 'FunctionDefinition(%s, %s, %s)' % (self.name, self.parameters, self.body)

    # def eval(self, env):
    #     env[self.name] = self  # Store the function definition in the environment

class FunctionCall(ArithmeticExpression):
    def __init__(self, name, arguments):
        self.name = name          # The name of the function being called
        self.arguments = arguments  # The list of argument expressions

    def __repr__(self):
        return 'FunctionCall(%s, %s)' % (self.name, self.arguments)

    # def eval(self, env):
    #     # First, find the function definition in the environment
    #     if self.name in env:
    #         function = env[self.name]  # Retrieve the function definition
    #         if isinstance(function, FunctionDefinition):
    #             # Check if the number of arguments matches the number of parameters
    #             if len(self.arguments) == len(function.parameters):
    #                 # Create a new environment for the function call
    #                 local_env = env.copy()
    #                 for param, arg in zip(function.parameters, self.arguments):
    #                     local_env[param] = arg.eval(env)  # Assign argument values to parameters
    #                 return function.body.eval(local_env)  # Evaluate the function body
    #     raise RuntimeError(f"Function {self.name} is not defined or arguments do not match.")




class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'WhileStatement(%s, %s)' % (self.condition, self.body)

    # def eval(self, env):
    #     condition_value = self.condition.eval(env)
    #     while condition_value:
    #         self.body.eval(env)
    #         condition_value = self.condition.eval(env)

class IntegerAE(ArithmeticExpression):
    def __init__(self, i):
        self.i = i

    def __repr__(self):
        return 'IntegerAE(%d)' % self.i

    # def eval(self, env):
    #     return self.i

class FloatAE(ArithmeticExpression):  # New class for float numbers
    def __init__(self, f):
        self.f = f

    def __repr__(self):
        return 'FloatAE(%f)' % self.f

    # def eval(self, env):
    #     return self.f

class VariableAE(ArithmeticExpression):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'VariableAE(%s)' % self.name

    # def eval(self, env):
    #     if self.name in env:
    #         return env[self.name]
    #     else:
    #         return 0



class AndBexp(BinaryOperationAE):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return 'AndBexp(%s, %s)' % (self.left, self.right)

    # def eval(self, env):
    #     left_value = self.left.eval(env)
    #     right_value = self.right.eval(env)
    #     return left_value and right_value

class OrBexp(BinaryOperationAE):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return 'OrBexp(%s, %s)' % (self.left, self.right)

    # def eval(self, env):
    #     left_value = self.left.eval(env)
    #     right_value = self.right.eval(env)
    #     return left_value or right_value

class NotBexp(BinaryOperationAE):
    def __init__(self, exp):
        self.exp = exp

    def __repr__(self):
        return 'NotBexp(%s)' % self.exp

    # def eval(self, env):
    #     value = self.exp.eval(env)
    #     return not value

