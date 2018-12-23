from llvmlite import ir, binding


class CodeGen:
    """
    Transforms an AST into LLVM IR (intermediate representation). Responsible
    for configuring LLVM and creating and saving IR code.
    """

    def __init__(self):
        self.binding = binding
        self.binding.initialize()
        self.binding.initialize_native_target()
        self.binding.initialize_native_asmprinter()

        self.__config_llvm()
        self.__create_execution_engine()
        self.__declare_print_function()

    def __config_llvm(self):
        self.module = ir.Module(name=__file__)
        self.module.triple = self.binding.get_default_triple()

        func_type = ir.FunctionType(ir.VoidType, [], False)
        base_func = ir.Function(self.module, func_type, name='main')
        block = base_func.append_basic_block(name='entry')
        self.builder = ir.IRBuilder(block)

    def __create_execution_engine(self):
        """
        Create an ExecutionEngine suitable for JIT code generation on the host
        CPU. The engine is reusable for an arbitrary number of modules.
        """
        target = self.binding.Target.from_default_triple()
        target_machine = target.create_target_machine()
        backing_mod = binding.parse_assembly("")
        engine = binding.create_mcjit_compiler(backing_mod, target_machine)
        self.engine = engine

    def __declare_print_function(self):
        voidptr_type = ir.IntType(8).as_pointer()
        printf_type = ir.FunctionType(ir.IntType(32), [voidptr_type], var_arg=True)
        printf = ir.Function(self.module, printf_type, name='printf')
        self.printf = printf

    def __compile_ir(self):
        """
        Compile the LLVM IR string with the given engine. The compiled module
        object is returned.
        """
        self.builder.ret_void()
        llvm_ir = str(self.module)
        mod = self.binding.parse_assembly(llvm_ir)
        mod.verify()

        self.engine.add_module(mod)
        self.engine.finalize_object()
        self.engine.run_static_constructors()
        return mod

    def create_ir(self):
        self.__compile_ir()

    def save_ir(self, filename):
        with open(filename, 'w') as output_file:
            output_file.write(str(self.module))
