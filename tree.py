# coding=utf-8

'''
    树型结构
    二叉树
    完全二叉树'''

class Tree(object):
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, child):
        if not isinstance(child, Tree):
            return 'not a child node'
        self.children.append(child)

    def output_depth(self):
        print self.name,
        for n in self.children:
            n.output_depth()

    def output_breadth(self):
        def gen(root):
            children_list = [root,]
            while children_list:
                node = children_list.pop(0)
                children_list.extend(node.children)
                yield node
        for e in gen(self):
            print e.name,


class BiTree(object):
    def __init__(self, name):
        self.name = name
        self.l_child = ''
        self.r_child = ''

    def add_child(self, child):
        if not isinstance(child, BiTree):
            print '{} is not a BiTree Node'.format(child.name)
        if not self.l_child:
            self.l_child = child
        elif not self.r_child:
            self.r_child = child
        else:
            print '{} cannot add, coz {} has two children already.'.format(child.name, self.name)

    def output_depth(self):
        print self.name,
        if self.l_child:
            self.l_child.output_depth()
        if self.r_child:
            self.r_child.output_depth()

    def output_breadth(self):
        def gen(o):
            children_list = [o]
            while children_list:
                node = children_list.pop(0)
                if node.l_child:
                    children_list.append(node.l_child)
                if node.r_child:
                    children_list.append(node.r_child)
                yield node
        for n in gen(self):
            print n.name,

    def swap(self):
        if self.l_child or self.r_child:
            self.l_child, self.r_child = self.r_child, self.l_child
            if self.l_child:
                self.l_child.swap()
            if self.r_child:
                self.r_child.swap()


class ComBiTree(BiTree):
    def __init__(self, name):
        super(ComBiTree, self).__init__(name)
        self.q = [self]

    def add_child(self, _name):
        node = BiTree(_name)
        for i in self.q:
            if not i.l_child:
                i.l_child = node
                break
            if not i.r_child:
                i.r_child = node
                break
        self.q.append(node)


a = ComBiTree('root_0')
for i in range(1, 11):
    name = 'node_{}'.format(i)
    a.add_child(name)
a.output_depth()
print ''
a.output_breadth()
print ''
a.swap()
print ''
a.output_depth()
print ''
a.output_breadth()
