from antlr4 import *
from autogen.CymbolParser import CymbolParser
from autogen.CymbolVisitor import CymbolVisitor


class Type:
    VOID = "void"
    INT = "int"
    STRING = "string"
    BOOL = "bool"
    FLOAT = "float"


class CymbolCheckerVisitor(CymbolVisitor):
    vars_types = {}
    functions_info = {}
    # UTILS

    def getLineAndColumnTyped(self, var, tyype):
        ctx = getattr(var, str(tyype).upper())
        # ingenious, right? :) Go to CymbolParser.py to understand.
        return self.getLineAndColumn(ctx())

    def getLineAndColumn(self, var):
        return 'line ' + str(var.getSymbol().line) + ', column ' + str(var.getSymbol().column)

    # START TYPES
    def visitIntExpr(self, ctx: CymbolParser.IntExprContext):
        print("visting "+Type.INT)
        return Type.INT

    def visitFloatExpr(self, ctx: CymbolParser.FloatExprContext):
        print("visting "+Type.FLOAT)
        return Type.FLOAT

    def visitBoolExpr(self, ctx: CymbolParser.BoolExprContext):
        print("visting "+Type.BOOL)
        return Type.BOOL

    def visitStringExpr(self, ctx: CymbolParser.StringExprContext):
        print("visting "+Type.STRING)
        return Type.STRING
    # END TYPES

    # START OPERATIONS
    def visitVarIdExpr(self, ctx: CymbolParser.VarIdExprContext):
        ctx.ID().accept(self)
        return self.vars_types[ctx.ID().getText()]

    def visitAddSubExpr(self, ctx: CymbolParser.AddSubExprContext):
        left = ctx.expr()[0].accept(self)
        right = ctx.expr()[1].accept(self)
        op = ctx.op.text
        types = [left, right]
        print('left', left, 'right', right)

        if left == Type.INT and right == Type.INT:
            result = Type.INT
        elif left == Type.FLOAT and right == Type.FLOAT:
            result = Type.FLOAT
        elif left == Type.STRING and right == Type.STRING:
            result = Type.STRING
        elif Type.INT in types and Type.FLOAT in types:
            result = Type.FLOAT
        elif Type.INT in types and Type.STRING in types:
            result = Type.STRING
        elif Type.FLOAT in types and Type.STRING in types:
            result = Type.STRING
        else:
            result = Type.VOID
            operation = op
            if(op == '+'):
                operation = 'sum'
            else:
                operation = 'subtract'
            print(
                "Error in {}, operator {}: trying to {} a value of type {} with another of type {}."
                .format(self.getLineAndColumnTyped(ctx.expr()[1], right), op, operation, left, right)
            )
            exit(0)

        print("AddSub of " + left + " " + right +
              " that results in a " + result)
        return result

    def visitSignedExpr(self, ctx: CymbolParser.SignedExprContext):
        element = ctx.expr().accept(self)
        if element == Type.INT:
            result = Type.INT
        elif element == Type.FLOAT:
            result = Type.FLOAT
        else:
            result = Type.VOID
            print(
                "Error in {}, operator {}: the type {} can't be signed"
                .format(self.getLineAndColumnTyped(ctx.expr(), element), ctx.op.text, element)
            )
            exit(0)

        print("Signed " + element + " results in a " + result)
        return result

    def visitNotExpr(self, ctx: CymbolParser.NotExprContext):
        # element = ctx.expr()
        # print('ctx', dir(ctx))
        # exit(0)
        typ = ctx.expr().accept(self)
        if typ == Type.BOOL:
            result = Type.BOOL
        else:
            result = Type.VOID

            print(
                "Error in {}, operator !: the ! operator can't be used with the type {}"
                .format(self.getLineAndColumnTyped(ctx, 'NOT'), typ)
            )
            exit(0)
        # print("Not " + element + " results in a " + result)

        return result

    def visitComparisonExpr(self, ctx: CymbolParser.ComparisonExprContext):
        left = ctx.expr()[0].accept(self)
        right = ctx.expr()[1].accept(self)
        op = ctx.op.text

        if left == Type.INT and right == Type.INT:
            result = Type.BOOL
        elif left == Type.INT and right == Type.FLOAT:
            result = Type.BOOL
        elif left == Type.FLOAT and right == Type.FLOAT:
            result = Type.BOOL
        elif left == Type.FLOAT and right == Type.INT:
            result = Type.BOOL
        else:
            result = Type.VOID
            print(
                "Error in {}, operator {}: the {} {} {} operation isn't supported, the types don't match."
                .format(self.getLineAndColumnTyped(ctx.expr()[1], right), op, left, op, right)
            )
            exit(0)

        return result

    def visitMulDivExpr(self, ctx: CymbolParser.MulDivExprContext):
        left = ctx.expr()[0].accept(self)
        right = ctx.expr()[1].accept(self)
        op = ctx.op.text

        if left == Type.INT and right == Type.INT:
            if op == '/':
                result = Type.FLOAT
            else:
                result = Type.INT
        elif left == Type.INT and right == Type.FLOAT:
            result = Type.FLOAT
        elif left == Type.FLOAT and right == Type.FLOAT:
            result = Type.FLOAT
        elif left == Type.FLOAT and right == Type.INT:
            result = Type.FLOAT

        else:
            result = Type.VOID
            print(
                "Error in {}, operator {}: the {} {} {} operation isn't supported, the types don't match."
                .format(self.getLineAndColumnTyped(ctx.expr()[1], right), op, left, op, right)
            )
            exit(0)

        print("MulDiv (" + op + ") of " + left + " " + right +
              " that results in a " + result)
        return result

    def visitAndOrExpr(self, ctx: CymbolParser.AndOrExprContext):
        left = ctx.expr()[0].accept(self)
        right = ctx.expr()[1].accept(self)
        op = ctx.op.text

        if left == Type.BOOL and right == Type.BOOL:
            result = Type.BOOL

        else:
            result = Type.VOID
            print(
                "Error in {}, operator {}: the {} {} {} operation isn't supported, the types don't match."
                .format(self.getLineAndColumnTyped(ctx.expr()[1], right), op, left, op, right)
            )
            exit(0)
        print("AndOr of " + left + " " + right +
              " that results in a " + result)
        return result
    # END OPERATIONS

    # START DECLARATIONS
    def visitFuncDecl(self, ctx: CymbolParser.FuncDeclContext):
        function_name = ctx.ID().getText()
        print('funcDecl', function_name)
        typ = ctx.tyype().getText()
        # self.functions_info[function_name] = typ
        params = []
        paramList = []
        if ctx.paramTypeList != None:
            paramList = ctx.paramTypeList().paramType()
        for param in paramList:
            self.vars_types[param.ID().getText()] = param.tyype().getText()
            params.append({
                'id': param.ID().getText(),
                'type': param.tyype().getText()
            })

        self.functions_info[function_name] = {
            'type': typ,
            'params': params
        }
        print('params', params)
        return self.visitChildren(ctx)

    def visitVarDecl(self, ctx: CymbolParser.VarDeclContext):
        print('var decl')
        var_name = ctx.ID().getText()
        tyype = ctx.tyype().getText()
        print("tyype = " + tyype)

        if (tyype == Type.VOID):
            print(
                "Error in {}: Variable '{}' of the type '{}' can't be declared"
                .format(self.getLineAndColumn(ctx.ID()), var_name, tyype)
            )
            exit(0)
        else:
            if ctx.expr() != None:
                init = ctx.expr().accept(self)
                print("init = " + init)
                if init != tyype:
                    print(
                        "Error in {}, operator =: Variable '{}': The declaration type ({}) is different than the assignment type ({})"
                        .format(self.getLineAndColumn(ctx.ID()), var_name, tyype, init)
                    )
            self.vars_types[var_name] = tyype

        print("saved variable " + var_name + " of type " + tyype)
        return tyype
    # END DECLARATIONS

    def visitBlock(self, ctx: CymbolParser.BlockContext):
        return self.visitChildren(ctx)

    # RETURN STAT
    def visitReturnStat(self, ctx: CymbolParser.ReturnStatContext):

        # Find the function declaration context by recursively checking
        # if a context contains the 'functionType' attribute which
        # only function declarations contain
        parent = ctx.parentCtx
        functionType = getattr(parent, 'functionType', True)
        while (functionType == True):
            parent = parent.parentCtx
            if (parent == None):
                print(
                    'Error in {}: Misplaced return statement.'
                    .format(self.getLineAndColumnTyped(ctx, 'RETURN'))
                )
                exit(0)
            functionType = getattr(parent, 'functionType', True)

        functionType = functionType.getText()
        retType = None

        if(ctx.expr() != None):
            retType = ctx.expr().accept(self)

        print('ft', functionType, 'rt', retType)
        if(functionType != retType):
            print(
                'Error in {}: function type ({}) differs from return type ({})'
                .format(self.getLineAndColumnTyped(ctx, 'RETURN'), functionType, retType)
            )
            exit(0)

    def visitFunctionCallExpr(self, ctx: CymbolParser.FunctionCallExprContext):
        func_name = ctx.ID().getText()
        # print('function call', func_name)
        paramList = ctx.exprList()
        # print(paramList)
        if paramList != None:
            paramList = ctx.exprList().expr()
            if len(paramList) > len(self.functions_info[func_name]['params']):
                print(
                    'Error in {}: function call {} has too many parameters'
                    .format(self.getLineAndColumn(ctx.ID()), ctx.getText())
                )
                exit(0)
            elif len(paramList) < len(self.functions_info[func_name]['params']):
                print(
                    'Error in {}: function call {} doesn\'t have enough parameters'
                    .format(self.getLineAndColumn(ctx.ID()), ctx.getText())
                )
                exit(0)
            i = 0
            for param in paramList:
                givenParamType = param.accept(self)
                funcParamType = self.functions_info[func_name]['params'][i]['type']
                if(givenParamType != funcParamType):
                    print(
                        'Error in {}: when calling function \'{}\': the parameter of number {} of type {} doesn\'t match expected type {}'
                        .format(self.getLineAndColumnTyped(param, givenParamType), func_name, i+1, givenParamType, funcParamType)
                    )
                    exit(0)
                i += 1
        else:
            if len(self.functions_info[func_name]['params']) != 0:
                print(
                    'Error in {}: function call {} doesn\'t have enough parameters'
                    .format(self.getLineAndColumn(ctx.ID()), ctx.getText())
                )
                exit(0)
        return self.functions_info[ctx.ID().getText()]["type"]

    def visitAssignStat(self, ctx: CymbolParser.AssignStatContext):
        varName = ctx.ID().getText()
        varType = self.vars_types[varName]
        exprType = ctx.expr().accept(self)
        if varType != exprType:
            print(
                "Error in {}, operator =: assignment '{}': The variable's type ({}) is different than the expression type ({})"
                .format(self.getLineAndColumn(ctx.ID()), varName, varType, exprType)
            )
            exit(0)

    def aggregateResult(self, aggregate: Type, next_result: Type):
        return next_result if next_result != None else aggregate
