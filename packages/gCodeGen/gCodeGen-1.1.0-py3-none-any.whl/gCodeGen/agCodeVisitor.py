# Generated from C:/Users/dennis.schwebius/PycharmProjects/advGcode\agCode.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .agCodeParser import agCodeParser
else:
    from agCodeParser import agCodeParser

# This class defines a complete generic visitor for a parse tree produced by agCodeParser.

class agCodeVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by agCodeParser#prog.
    def visitProg(self, ctx:agCodeParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by agCodeParser#statement.
    def visitStatement(self, ctx:agCodeParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by agCodeParser#gLine.
    def visitGLine(self, ctx:agCodeParser.GLineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by agCodeParser#logic.
    def visitLogic(self, ctx:agCodeParser.LogicContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by agCodeParser#repeatStmt.
    def visitRepeatStmt(self, ctx:agCodeParser.RepeatStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by agCodeParser#ifStmt.
    def visitIfStmt(self, ctx:agCodeParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by agCodeParser#trueStats.
    def visitTrueStats(self, ctx:agCodeParser.TrueStatsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by agCodeParser#falseStats.
    def visitFalseStats(self, ctx:agCodeParser.FalseStatsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by agCodeParser#condition.
    def visitCondition(self, ctx:agCodeParser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by agCodeParser#varDecl.
    def visitVarDecl(self, ctx:agCodeParser.VarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by agCodeParser#assign.
    def visitAssign(self, ctx:agCodeParser.AssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by agCodeParser#printLn.
    def visitPrintLn(self, ctx:agCodeParser.PrintLnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by agCodeParser#add.
    def visitAdd(self, ctx:agCodeParser.AddContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by agCodeParser#number.
    def visitNumber(self, ctx:agCodeParser.NumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by agCodeParser#not.
    def visitNot(self, ctx:agCodeParser.NotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by agCodeParser#paren.
    def visitParen(self, ctx:agCodeParser.ParenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by agCodeParser#bool.
    def visitBool(self, ctx:agCodeParser.BoolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by agCodeParser#mul.
    def visitMul(self, ctx:agCodeParser.MulContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by agCodeParser#var.
    def visitVar(self, ctx:agCodeParser.VarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by agCodeParser#text.
    def visitText(self, ctx:agCodeParser.TextContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by agCodeParser#unary.
    def visitUnary(self, ctx:agCodeParser.UnaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by agCodeParser#power.
    def visitPower(self, ctx:agCodeParser.PowerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by agCodeParser#compar.
    def visitCompar(self, ctx:agCodeParser.ComparContext):
        return self.visitChildren(ctx)



del agCodeParser