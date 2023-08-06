# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import os
import sys
import tempfile
from copy import deepcopy
from azureml.exceptions import UserErrorException

from azure.ml.component._util._exceptions import UnsupportedError


class OperableMixin:
    SUPPORTED_CONST_TYPES = (bool, int, float, str)

    def __hash__(self):
        return id(self)

    def _validate_operation(self, other):
        from azure.ml.component._pipeline_parameters import PipelineParameter
        if not isinstance(other, self.SUPPORTED_CONST_TYPES) and \
                not isinstance(other, (PipelineParameter, PipelineExpression)):
            msg = 'Only support operation between constant, PipelineParameter and PipelineExpression.'
            raise UserErrorException(msg)

    def __add__(self, other):
        self._validate_operation(other)
        return PipelineExpression._from_python_expression(self, other, '+')

    def __radd__(self, other):
        self._validate_operation(other)
        return PipelineExpression._from_python_expression(other, self, '+')

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        self._validate_operation(other)
        return PipelineExpression._from_python_expression(self, other, '-')

    def __rsub__(self, other):
        self._validate_operation(other)
        return PipelineExpression._from_python_expression(other, self, '-')

    def __isub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        self._validate_operation(other)
        return PipelineExpression._from_python_expression(self, other, '*')

    def __rmul__(self, other):
        self._validate_operation(other)
        return PipelineExpression._from_python_expression(other, self, '*')

    def __imul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        self._validate_operation(other)
        return PipelineExpression._from_python_expression(self, other, '/')

    def __rtruediv__(self, other):
        self._validate_operation(other)
        return PipelineExpression._from_python_expression(other, self, '/')

    def __itruediv__(self, other):
        return self.__truediv__(other)

    def __mod__(self, other):
        self._validate_operation(other)
        return PipelineExpression._from_python_expression(self, other, '%')

    def __rmod__(self, other):
        self._validate_operation(other)
        return PipelineExpression._from_python_expression(other, self, '%')

    def __imod__(self, other):
        return self.__mod__(other)

    def __pow__(self, other):
        self._validate_operation(other)
        return PipelineExpression._from_python_expression(self, other, '**')

    def __rpow__(self, other):
        self._validate_operation(other)
        return PipelineExpression._from_python_expression(other, self, '**')

    def __ipow__(self, other):
        return self.__pow__(other)

    def __floordiv__(self, other):
        self._validate_operation(other)
        return PipelineExpression._from_python_expression(self, other, '//')

    def __rfloordiv__(self, other):
        self._validate_operation(other)
        return PipelineExpression._from_python_expression(other, self, '//')

    def __ifloordiv__(self, other):
        return self.__floordiv__(other)

    def __lt__(self, other):
        self._validate_operation(other)
        return PipelineExpression._from_python_expression(self, other, '<')

    def __gt__(self, other):
        self._validate_operation(other)
        return PipelineExpression._from_python_expression(self, other, '>')

    def __le__(self, other):
        self._validate_operation(other)
        return PipelineExpression._from_python_expression(self, other, '<=')

    def __ge__(self, other):
        self._validate_operation(other)
        return PipelineExpression._from_python_expression(self, other, '>=')

    def __eq__(self, other):
        self._validate_operation(other)
        return PipelineExpression._from_python_expression(self, other, '==')

    def __ne__(self, other):
        self._validate_operation(other)
        return PipelineExpression._from_python_expression(self, other, '!=')

    def __bool__(self):
        """Python method, called to implement truth value testing and the built-in operation bool().

        This method is not supported. OperableMixin is designed to record operation history,
        while __bool__ only return False or True, leading to lineage breaks here. As overloadable
        boolean operators PEP (refer to: https://www.python.org/dev/peps/pep-0335/) was rejected,
        logical operations are also not supported here.
        """
        raise UnsupportedError('operation bool() is unsupported.')

    def __and__(self, other):
        self._validate_operation(other)
        return PipelineExpression._from_python_expression(self, other, '&')

    def __or__(self, other):
        self._validate_operation(other)
        return PipelineExpression._from_python_expression(self, other, '|')

    def __xor__(self, other):
        self._validate_operation(other)
        return PipelineExpression._from_python_expression(self, other, '^')


class PipelineExpression(OperableMixin):
    SUPPORTED_OPERATORS = ('+', '-', '*', '/', '%', '**', '//',  # numerical operators
                           '<', '>', '<=', '>=', '==', '!=',  # comparison operators
                           '&', '|', '^')  # bitwise operators
    DEFAULT_RETURN_TYPE_FROM_PYTHON_EXPRESSION = 'Any'
    IMPORT_DSL_LINE = 'from azure.ml.component import dsl'
    IMPORT_DSL_TYPES_LINE = 'from azure.ml.component.dsl.types import Output, @@component_return_type@@\n'
    DSL_DECORATOR_LINE = "@dsl.command_component(display_name='expression: @@infix_notation@@')"
    COMPONENT_FUNC_NAME = 'expression_generated_component'
    COMPONENT_FUNC_DECLARATION_LINE = f'def {COMPONENT_FUNC_NAME}(@@component_parameters@@)' \
                                      f' -> Output(type=@@component_return_type@@.TYPE_NAME, is_control=True):'

    def __init__(self, expression, return_type, is_rpn=False, pipeline_parameter_cache=None):
        """Define an expression in a pipeline execution.

        Use PipelineExpression to support simple and trivial parameter transformations tasks.
        Expression will be saved after several process, which can be recovered if needed.

        :param expression: Expression doing trivial parameter transformations tasks.
        :type expression: str
        :param return_type: Return type of the expression.
        :type return_type: str
        :param is_rpn: Parameter related to inner implementation, keep it default value as False.
        :type is_rpn: bool
        :param pipeline_parameter_cache: Parameter related to inner implementation, keep it default value as None.
        :type pipeline_parameter_cache: dict
        """
        self._created_component = None  # cache for created component
        self._return_type = return_type
        if is_rpn is True:
            self._rpn = expression.split()
            self._pipeline_parameter_cache = pipeline_parameter_cache
        else:
            raise UnsupportedError('')

    @staticmethod
    def _from_python_expression(operand1, operand2, operator):
        """Construct PipelineExpression from python expression.

        :param operand1: First operand of the expression. Valid type includes simple constant
            (currently bool, int, float and str), PipelineParameter and PipelineExpression.
        :type operand1: Union[bool, int, float, str, PipelineParameter, PipelineExpression]
        :param operand2: Second operand of the expression. Same valid type as operand1.
        :type operand2: Union[bool, int, float, str, PipelineParameter, PipelineExpression]
        :param operator: Operator of the expression. Valid value includes numerical operators
            ('+', '-', '*', '/', '%', '**', '//'), comparison operators ('<', '>', '<=', '>=', '==', '!=')
            and bitwise operators ('&', '|', '^').
        :type operator: str
        """
        rpn = []
        pipeline_parameter_cache = {}
        for operand in [operand1, operand2]:
            if operand is None:
                continue
            from azure.ml.component._pipeline_parameters import PipelineParameter
            if isinstance(operand, PipelineParameter):
                rpn.append(operand.name)
                pipeline_parameter_cache[operand.name] = operand
            elif isinstance(operand, PipelineExpression):
                rpn.extend(deepcopy(operand._rpn))
                pipeline_parameter_cache.update(operand._pipeline_parameter_cache.copy())
            elif isinstance(operand, PipelineExpression.SUPPORTED_CONST_TYPES):
                rpn.append(repr(operand))
        if operator not in PipelineExpression.SUPPORTED_OPERATORS:
            msg = f"'{operator}' is not supported operator for PipelineParameter and PipelineExpression, " \
                  f"currently supported operators include {', '.join(PipelineExpression.SUPPORTED_OPERATORS)}."
            raise UserErrorException(msg)
        rpn.append(operator)
        return PipelineExpression(expression=' '.join(rpn),
                                  return_type=PipelineExpression.DEFAULT_RETURN_TYPE_FROM_PYTHON_EXPRESSION,
                                  is_rpn=True, pipeline_parameter_cache=pipeline_parameter_cache)

    def __repr__(self):
        return f"PipelineExpression(expression={repr(' '.join(self._rpn))}, " \
               f"return_type={repr(self._return_type)}, " \
               f"is_rpn=True, pipeline_parameter_cache={repr(self._pipeline_parameter_cache)})"

    def set_return_type(self, typ):
        """Manually set return type for expression."""
        self._return_type = typ

    @property
    def _infix_notation(self):
        """Generate infix notation of expression."""
        stack = []
        tokens = deepcopy(self._rpn)
        for token in tokens:
            if token not in self.SUPPORTED_OPERATORS:
                stack.append(token)
                continue
            operand2, operand1 = stack.pop(), stack.pop()
            stack.append(f'({operand1} {token} {operand2})')
        return stack.pop()

    @property
    def _postfix_notation(self):
        return self._rpn

    @property
    def _rtype(self):
        if self._return_type != self.DEFAULT_RETURN_TYPE_FROM_PYTHON_EXPRESSION:
            return self._return_type
        # 'infer' return type only via last operator, bool if comparison operator, else raise
        last_operator = self._rpn[-1]
        if last_operator in ('<', '>', '<=', '>=', '==', '!='):
            return 'bool'
        raise UserErrorException("Indeterminate return type, please specify by method 'set_return_type'.")

    @staticmethod
    def _to_dsl_type(typ):
        if typ == 'bool':
            return 'Boolean'
        elif typ == 'int':
            return 'Integer'
        elif typ == 'float':
            return 'Float'
        return 'String'

    @staticmethod
    def _to_python_type(typ):
        if typ == 'string':
            return 'str'
        else:
            return typ

    @property
    def _component_func_code_block(self):
        res = []
        # RPN calculator
        stack = []
        tokens = deepcopy(self._rpn)
        intermediate_id = 0
        expression_recorder = {}
        for token in tokens:
            if token not in self.SUPPORTED_OPERATORS:
                stack.append(token)
                continue
            operand2, operand1 = stack.pop(), stack.pop()
            python_expression = f'{operand1} {token} {operand2}'
            if python_expression not in expression_recorder:
                intermediate_param = f'intermediate_param_{intermediate_id}'
                intermediate_id += 1
                res.append(f'    {intermediate_param} = {python_expression}')
                expression_recorder[python_expression] = intermediate_param
            else:
                intermediate_param = expression_recorder[python_expression]
            stack.append(intermediate_param)
        ret_name = stack.pop()
        res.append(f'    return {ret_name}')
        dsl_type = self._to_dsl_type(self._rtype)
        # construct parameters name and type
        parameters = []
        for parameter_name in sorted(self._pipeline_parameter_cache.keys()):
            pipeline_parameter = self._pipeline_parameter_cache[parameter_name]
            parameters.append(f'{parameter_name}: {self._to_python_type(pipeline_parameter._type)}')
        component_func_declaration_line = self.COMPONENT_FUNC_DECLARATION_LINE\
            .replace('@@component_parameters@@', ', '.join(parameters))\
            .replace('@@component_return_type@@', dsl_type)
        res = [self.IMPORT_DSL_LINE,
               self.IMPORT_DSL_TYPES_LINE.replace('@@component_return_type@@', dsl_type),
               self.DSL_DECORATOR_LINE.replace('@@infix_notation@@', self._infix_notation),
               component_func_declaration_line] + res
        return '\n'.join(res) + '\n'  # extra newline for blank line at end of file

    @property
    def _component_func_call_line(self):
        parameters_from_thread_local = [f"{pipeline_parameter}=self._pipeline_parameter_cache['{pipeline_parameter}']"
                                        for pipeline_parameter in self._pipeline_parameter_cache.keys()]
        parameters = ', '.join(sorted(parameters_from_thread_local))
        return f'{self.COMPONENT_FUNC_NAME}({parameters})'

    def _create_dynamic_component(self):
        if self._created_component is None:
            # need to dump generated code to file for snapshot (dsl.command_component logic)
            tmp_py_folder = tempfile.mkdtemp()
            module_name = self.COMPONENT_FUNC_NAME
            tmp_filename = module_name + '.py'
            with open(os.path.join(tmp_py_folder, tmp_filename), 'w') as fp:
                fp.write(self._component_func_code_block)
            original_sys_path = sys.path.copy()
            sys.path.insert(0, str(tmp_py_folder))
            exec(f'from {module_name} import {self.COMPONENT_FUNC_NAME}')
            sys.path = original_sys_path
            self._created_component = eval(self._component_func_call_line)
        return self._created_component
