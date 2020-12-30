from VBParser import SimpleTokenParser
from pygments.token import Token
from ysj_io import printResult

def _getTokens(src: str):
    # remove underline '_'
    src = src.replace('_\n', '')
    src = src.strip().split('\n')
    token_list = []
    for s in src:
        if s != '':
            token_list.append(SimpleTokenParser(s))
    return token_list
def FunctionChain(src: str):
    token_list = _getTokens(src)
    class FuncNode:
        def __init__(self, name):
            self.next = list()
            self.name = name
        def GetName(self):
            return self.name
        def SetNext(self, next):
            if next not in self.next:
                self.next.append(next)
        def __str__(self) -> str:
            return self.name
    class FuncDict:
        def __init__(self):
            self.nodes = dict()
            self.traversed = None
        def GetNode(self, name: str):
            ret_node = None
            if name in self.nodes:
                ret_node = self.nodes[name]
            else:
                ret_node = FuncNode(name)
                self.nodes[name] = ret_node
            return ret_node
        def GetNodeCount(self):
            return len(self.nodes)
        def _doTraverse(self, root: FuncNode, now: FuncNode):
            assert self.traversed is not None
            if self.traversed[now.GetName()] and now.GetName() == root.GetName():
                # Avoid recursion
                return 0
            self.traversed[now.GetName()] = True
            max_child_count = 0
            for node in now.next:
                child_count = self._doTraverse(root, node)
                if child_count > max_child_count:
                    max_child_count = child_count
            return max_child_count + 1 # self
        def CalculateMaxLength(self):
            self.traversed = dict()
            for name in self.nodes:
                self.traversed[name] = False
            max_len = 0
            for node in self.nodes.values():
                if not self.traversed[node.GetName()]:
                    now_len = self._doTraverse(node, node)
                    if now_len > max_len:
                        max_len = now_len
            return max_len
    func_dict = FuncDict()
    now_func = None
    for tokens in token_list:
        for i, token in enumerate(tokens):
            if token[0] == Token.Name.Function:
                now_func = func_dict.GetNode(token[1])
            elif token == (Token.Keyword, 'End'):
                now_func = None
            elif token == (Token.Keyword, 'Call'):
                if i + 1 < len(tokens):
                    func_node = func_dict.GetNode(tokens[i + 1][1])
                    now_func.SetNext(func_node)
    ret_val = 0
    if func_dict.GetNodeCount() > 0:
        ret_val = func_dict.CalculateMaxLength() / func_dict.GetNodeCount()
    io_data = {'Max Function Chain': (ret_val, 0.25)}
    printResult('Jumping Control Flow', io_data)
    return io_data
if __name__ == "__main__":
    print('==========================')
    with open('test_cases/test_array_detect_2.txt', 'r') as f:
        code = f.read()
    print(FunctionChain(code))