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
    id_values = {}

    def getLineAndColumn(self, var):
        return 'linha ' + var.getSymbol().line + ', coluna ' + var.getSymbol().column

    def visitIntExpr(self, ctx: CymbolParser.IntExprContext):
        print("visiting "+Type.INT)
        return Type.INT

    def visitFloatExpr(self, ctx: CymbolParser.FloatExprContext):
        print("visiting "+Type.FLOAT)
        return Type.FLOAT

    # Não está estrando aqui:
    def visitBoolExpr(self, ctx: CymbolParser.BoolExprContext):
        print("visiting " + Type.BOOL)
        return Type.BOOL

    def visitStringExpr(self, ctx: CymbolParser.StringExprContext):
        print("visiting "+Type.STRING)
        return Type.STRING

    def visitVarDecl(self, ctx: CymbolParser.VarDeclContext):
        var_name = ctx.ID().getText()
        tyype = ctx.tyype().getText()
        print("tyype = " + tyype)

        if (tyype == Type.VOID):
            result = Type.VOID
            print("Erro: Variavel {} do tipo {}: {}".format(var_name, tyype, ))
            exit(1)
        else:
            if ctx.expr() != None:
                init = ctx.expr().accept(self)
                print("init = " + init)
                if init != tyype:
                    print("Mensagem de erro 2...")
                    exit(2)

            result = tyype
            self.id_values[var_name] = tyype

        print("saved variable " + var_name + " of type " + tyype)
        return result

    def visitAddSubExpr(self, ctx: CymbolParser.AddSubExprContext):
        left = ctx.expr()[0].accept(self)
        right = ctx.expr()[1].accept(self)

        if left == Type.INT and right == Type.INT:
            result = Type.INT
        elif left == Type.INT and right == Type.FLOAT:
            result = Type.FLOAT
        elif left == Type.INT and right == Type.STRING:
            result = Type.STRING
        elif left == Type.FLOAT and right == Type.FLOAT:
            result = Type.FLOAT
        elif left == Type.FLOAT and right == Type.INT:
            result = Type.FLOAT
        elif left == Type.FLOAT and right == Type.STRING:
            result = Type.STRING
        elif left == Type.STRING and right == Type.STRING:
            result = Type.STRING
        elif left == Type.STRING and right == Type.INT:
            result = Type.STRING
        elif left == Type.STRING and right == Type.FLOAT:
            result = Type.STRING

        else:
            result = Type.VOID
            print("Error: wrong type assignment in AddSubExpr.")
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
            print("Error: wrong type assignment in SignedExpr.")
            exit()

        print("Signed " + element + " results in a " + result)
        return result

    def visitNotExpr(self, ctx: CymbolParser.NotExprContext):
        element = ctx.expr().accept(self)
        if element == Type.BOOL:
            result = Type.BOOL
        else:
            result = Type.VOID
            print("Error: wrong type assignment in NotExpr.")
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

        # Como separar mul de div? usar op :)

        # para div:
        if left == Type.INT and right == Type.INT:
            result = Type.FLOAT
        # para mul daria INT
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

        print("MulDiv of " + left + " " + right +
              " that results in a " + result)
        return result

    def visitEqExpr(self, ctx: CymbolParser.EqExprContext):
        left = ctx.expr()[0].accept(self)
        right = ctx.expr()[1].accept(self)

        # Sempre pode fazer EqExpr?
        result = Type.BOOL

        print("EqExpr of " + left + " " + right +
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
