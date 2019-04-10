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

    def getLineAndColumnTyped(self, var, tyype):
        ctx = getattr(var, str(tyype).upper())
        # ingenious, right? :) Go to CymbolParser.py to understand.
        return self.getLineAndColumn(ctx())

    def getLineAndColumn(self, var):
        return 'line ' + str(var.getSymbol().line) + ', column ' + str(var.getSymbol().column)

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

    def visitVarDecl(self, ctx: CymbolParser.VarDeclContext):
        var_name = ctx.ID().getText()
        tyype = ctx.tyype().getText()
        print("tyype = " + tyype)

        if (tyype == Type.VOID):
            result = Type.VOID
            print(
                "Error 1 in {}: Variable '{}' of the type '{}' can't be declared"
                .format(self.getLineAndColumn(ctx.ID().getSymbol()), var_name, tyype)
            )
            exit(1)
        else:
            if ctx.expr() != None:
                init = ctx.expr().accept(self)
                print("init = " + init)
                if init != tyype:
                    print(
                        "Error 2 in {}, operator =: Variable '{}': The declaration type ({}) is different than the assignment type ({})"
                        .format(self.getLineAndColumn(ctx.ID()), var_name, tyype, init)
                    )
                    exit(2)
            result = tyype
            self.vars_types[var_name] = tyype

        print("saved variable " + var_name + " of type " + tyype)
        return result

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
                "Error 3 in {}, operator {}: trying to {} a value of type {} with another of type {}."
                .format(self.getLineAndColumnTyped(ctx.expr()[1], right), op, operation, left, right)
            )
            exit()

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
                "Error 4 in {}, operator {}: the type {} can't be signed"
                .format(self.getLineAndColumnTyped(ctx.expr(), element), ctx.op.text, element)
            )
            exit()

        print("Signed " + element + " results in a " + result)
        return result

    def visitNotExpr(self, ctx: CymbolParser.NotExprContext):
        element = ctx.expr().accept(self)
        if element == Type.BOOL:
            result = Type.BOOL
        else:
            result = Type.VOID
            print(
                "Error in {}, operator !: the ! operator can't be used with the type {}"
                .format(self.getLineAndColumnTyped(ctx.expr(), element), element)
            )
            exit()
        print("Not " + element + " results in a " + result)
        return result

    def visitComparisonExpr(self, ctx: CymbolParser.ComparisonExprContext):
        left = ctx.expr()[0].accept(self)
        right = ctx.expr()[1].accept(self)

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
            print("Error: wrong type assignment in ComparisonExpr.")
            exit()

        print("Comparison of " + left + " " +
              right + " that results in a " + result)
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
            print("Error: wrong type assignment in MulDivExpr.")
            exit()

        print("MulDiv (" + op + ") of " + left + " " + right +
              " that results in a " + result)
        return result

    def visitAndOrExpr(self, ctx: CymbolParser.AndOrExprContext):
        left = ctx.expr()[0].accept(self)
        right = ctx.expr()[1].accept(self)

        if left == Type.BOOL and right == Type.BOOL:
            result = Type.BOOL

        else:
            result = Type.VOID
            print("Error: wrong type assignment in AndOrExpr.")
            exit()
        print("AndOr of " + left + " " + right +
              " that results in a " + result)
        return result

    def aggregateResult(self, aggregate: Type, next_result: Type):
        return next_result if next_result != None else aggregate
