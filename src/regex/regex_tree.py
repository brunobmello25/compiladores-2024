from src.utils.symbol import Symbol


class RegexNode:
    def __init__(self, symbol: Symbol):
        self.parent: RegexNode | None = None
        self.symbol: Symbol | None = None

    def add_child(self, node: "RegexNode"):
        raise NotImplementedError


class RegexUnaryNode(RegexNode):
    def __init__(self, symbol: Symbol):
        self.symbol = symbol
        self.child: RegexNode | None = None
        self.parent: RegexNode | None = None

    def add_child(self, node: RegexNode):
        self.child = node
        node.parent = self


class RegexBinaryNode(RegexNode):
    def __init__(self, symbol: Symbol):
        self.symbol = symbol
        self.left: RegexNode | None = None
        self.right: RegexNode | None = None
        self.parent: RegexNode | None = None

    def add_child(self, node: RegexNode):
        node.parent = self
        if self.left is None:
            self.left = node
        else:
            self.right = node
