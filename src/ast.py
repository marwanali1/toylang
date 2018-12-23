from llvmlite import ir


class Number:

    def __init__(self, module, builder, value):
        self.module = module
        self.builder = builder
        self.value = value

    def eval(self):
        i = ir.Constant(ir.IntType(8), int(self.value))
        return i


class BinaryOp:

    def __init__(self, module, builder, left, right):
        self.module = module
        self.builder = builder
        self.left = left
        self.right = right


class Add(BinaryOp):

    def eval(self):
        i = self.builder.add(self.left.eval(), self.right.eval())
        return i


class Sub(BinaryOp):

    def eval(self):
        i = self.builder.sub(self.left.eval(), self.right.eval())
        return i


class Print:

    def __init__(self, module, builder, printf, value):
        self.module = module
        self.builder = builder
        self.printf = printf
        self.value = value

    def eval(self):
        value = self.value.eval()

        # Declare argument list
        voidptr_type = ir.IntType(8).as_pointer()
        fmt = "%i \n\0"
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)), bytearray(fmt.encode('utf8')))

        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name='fstr')
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt

        fmt_arg = self.builder.bitcast(global_fmt, voidptr_type)

        # Call Print Function
        self.builder.call(self.printf, [fmt_arg, value])
