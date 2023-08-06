from .agCodeParser import agCodeParser
from .agCodeVisitor import agCodeVisitor
import operator
import re

class Collector(agCodeVisitor):
    ops = {
        ">": operator.gt,
        ">=": operator.ge,
        "==": operator.eq,
        "<=": operator.le,
        "<": operator.lt,
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
        # "**": operator.pow
        # "!": operator.not_,
    }

    @staticmethod
    def getParts(text) -> (list, str):
        textParts = text.split('{}')
        subParts = []
        for tp in textParts[:-1]:
            subParts.append(tp + '{}')
        return subParts, textParts[-1]

    def __init__(self, doLog=False):
        self.memory = {}
        self.doLog = doLog

    def log(self, prefix, msg):
        if self.doLog:
            print(f'{prefix}: {msg}')

    def visitProg(self, ctx: agCodeParser.ProgContext):
        lines = []
        numberedLines = []
        for sctx in ctx.statement():
            res = self.visit(sctx)
            if res is not None:
                lines.extend(res)

        for i, line in enumerate(lines, 1):
            n = i * 10
            if "(" in line:
                numberedLines.extend(line + '\n')
                continue
            numberedLines.extend(f'N{n} ' + line + '\n')
        return ''.join(numberedLines)

    def visitStatement(self, ctx: agCodeParser.StatementContext) -> list:
        return self.visitChildren(ctx)

    def visitGLine(self, ctx: agCodeParser.GLineContext) -> list:
        values = []
        for ectx in ctx.expr():
            values.append(self.visit(ectx))
        line = ctx.GCMD().getText() + " "
        for i, value in enumerate(values, 0):
            line += ctx.COORD(i).getText() + f'{value:.2f} '
        return [line]

    def visitLogic(self, ctx: agCodeParser.LogicContext) -> list:
        rctx = ctx.repeatStmt()
        ictx = ctx.ifStmt()

        if rctx is not None:
            self.log("visit logic", "repeat stat")
            return self.visit(rctx)
        self.log("visit logic", "if stat")
        return self.visit(ictx)

    def visitRepeatStmt(self, ctx: agCodeParser.RepeatStmtContext) -> list:
        lines = []
        repeats = int(ctx.expr().getText())
        for i in range(repeats):
            for sctx in ctx.statement():
                subList = self.visit(sctx)
                if subList is not None:
                    assert (isinstance(subList, list))
                    lines.extend(subList)
        return lines

    def visitIfStmt(self, ctx: agCodeParser.IfStmtContext):
        truth = self.visit(ctx.condition())
        if truth:
            return self.visit(ctx.trueStats())
        try:
            return self.visit(ctx.falseStats())
        except AttributeError:
            return None

    def visitTrueStats(self, ctx: agCodeParser.TrueStatsContext) -> list:
        lines = []
        for sctx in ctx.statement():
            res = self.visit(sctx)
            if res is not None:
                lines.extend(res)
        return lines

    def visitFalseStats(self, ctx: agCodeParser.FalseStatsContext) -> list:
        lines = []
        for sctx in ctx.statement():
            res = self.visit(sctx)
            if res is not None:
                lines.extend(res)
        return lines

    def visitCondition(self, ctx: agCodeParser.ConditionContext) -> bool:
        expr = self.visit(ctx.expr())
        assert(isinstance(expr, bool))
        return expr

    def visitVarDecl(self, ctx: agCodeParser.VarDeclContext) -> None:
        varName = ctx.ID().getText()
        # value may be None, when variable is not initialized
        try:
            value = self.visit(ctx.expr())
        except AttributeError:
            value = None
        self.memory[varName] = value

    def visitAssign(self, ctx: agCodeParser.AssignContext) -> None:
        varName = ctx.ID().getText()
        value = self.visit(ctx.expr())
        self.memory[varName] = value

    def visitPrintLn(self, ctx: agCodeParser.PrintLnContext) -> list:
        line = "( "
        text = ctx.TEXT().getText().strip('\"')
        if text is not None:
            subParts, endPart = Collector.getParts(text)
            for i in range(ctx.getChildCount()):
                if hasattr(ctx.expr(i), 'accept'):
                    strExpr = str(self.visit(ctx.expr(i)))
                    try:
                        line += re.sub(r'{}', strExpr, subParts[0])
                    except IndexError:
                        raise Exception("Print statement has less placeholders than arguments!")
                    del subParts[0]

            if len(subParts) > 0:
                raise Exception("Print statement has more placeholders than arguments!")

            line += " " + endPart
        line += " )"

        return [line]

    def visitVar(self, ctx: agCodeParser.VarContext) -> float:
        varName = ctx.ID().getText()
        try:
            value = self.memory[varName]
            self.log("Variable accessed", f'{varName} = {value}')
        except KeyError:
            raise Exception(f'Variable \'{varName}\' is not defined')
        assert(isinstance(value, (float, bool, str)))
        return value

    def visitNumber(self, ctx: agCodeParser.NumberContext) -> float:
        return float(ctx.NUM().getText())

    def visitBool(self, ctx:agCodeParser.BoolContext) -> bool:
        expr = ctx.BOOL().getText()
        if expr == 'True':
            return True
        elif expr == 'False':
            return False
        # unreachable:
        raise Exception(f'Boolean must be \'true\' or \'false\'. Given {expr}')

    def visitText(self, ctx: agCodeParser.TextContext) -> str:
        return ctx.TEXT().getText().strip('\"')

    def visitPower(self, ctx: agCodeParser.PowerContext) -> float:
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        return left ** right

    def visitMul(self, ctx: agCodeParser.MulContext) -> float:
        strOp = ctx.op.text
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        self.log("Mul-left: ", left)
        self.log("Mul-right: ", right)
        result = Collector.ops[strOp](left, right)
        self.log("Mul-result: ", result)
        return Collector.ops[strOp](left, right)

    def visitAdd(self, ctx: agCodeParser.AddContext) -> float:
        strOp = ctx.op.text
        return Collector.ops[strOp](self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))

    def visitCompar(self, ctx:agCodeParser.ComparContext) -> bool:
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        strOp = ctx.op.text
        return Collector.ops[strOp](left, right)

    def visitUnary(self, ctx: agCodeParser.UnaryContext) -> float:
        value = self.visit(ctx.expr())
        assert(isinstance(value, float))
        return -value

    def visitNot(self, ctx:agCodeParser.NotContext) -> bool:
        value = self.visit(ctx.expr())
        assert(isinstance(value, bool))
        return not value

    def visitParen(self, ctx:agCodeParser.ParenContext):
        return self.visit(ctx.expr())
