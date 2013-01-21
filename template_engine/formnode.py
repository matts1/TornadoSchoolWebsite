from .groupnode import BlockNode

class FormNode(BlockNode):
    def __init__(self, args, parent):
        super().__init__(args, parent)
        self.block = False
        args = args.split("[", 1)
        if len(args) != 2:
            raise SyntaxError("Form is not complete")
        self.name, args = args
        args = eval("[" + args)
        self.fields = []
        for field in args:
            if len(field) < 3:
                raise SyntaxError("Not enough arguments to field")
            attr = {}
            if field[0] not in [0, 1, False, True]:
                raise SyntaxError("required is not a boolean")
            if field[0]:
                attr["required"] = ""

            attr["placeholder"] = field[1]
            attr["name"] = field[2]
            field = field[3:]
            if field and isinstance(field[0], str):
                attr["type"] = field[0]
                field = field[1:]

            for item in field:
                if not isinstance(item, tuple) and len(item) == 2:
                    raise SyntaxError("Additional arguments must be a tuple of length 2")
                attr[item[0]] = item[1]

            self.fields.append(attr)
    def eval(self, context):
        from .main import Parser
        return Parser("nodes/form.html").parse().eval({"fields": self.fields,
            "name": self.name})


