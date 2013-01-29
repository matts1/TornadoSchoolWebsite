def table(name, fields, table):
    for row in table:
        if len(row) != len(fields):
            raise IndexError("Length of all rows must be the same")

    from template_engine.main import render
    context = {
        "title": name,
        "thead": fields,
        "content": table,
    }
    return render("nodes/table.html", None, context)