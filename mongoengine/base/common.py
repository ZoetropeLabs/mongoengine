from mongoengine.errors import NotRegistered

__all__ = ('UPDATE_OPERATORS', 'get_document', '_document_registry')


UPDATE_OPERATORS = set(['set', 'unset', 'inc', 'dec', 'pop', 'push',
                        'push_all', 'pull', 'pull_all', 'add_to_set',
                        'set_on_insert', 'min', 'max', 'rename'])


_document_registry = {}


def get_document(name):
    """Get a document class by name."""
    doc = _document_registry.get(name, None)
    if not doc:
        # Possible old style name
        single_end = name.split('.')[-1]
        compound_end = '.%s' % single_end
        possible_match = [k for k in _document_registry.keys()
                          if k.endswith(compound_end) or k == single_end]
        if possible_match:
            try:
                # Get them both as a set of everything they inherit from
                inherited = name.split(".")
                possible_inherited = [i.split(".") for i in possible_match]

                set_inh = set(inherited)

                # first try to get an exact match
                same_inheritance = [i for i in possible_inherited if set(i) <= set_inh and set_inh <= set(i)]

                # If there isn't an exact match, just get one that is 'close'
                if not same_inheritance:
                    same_inheritance = sorted([i for i in possible_inherited if set(i) >= set_inh], key=len)

                doc = _document_registry.get(".".join(same_inheritance[0]), None)
            except IndexError:
                doc = None

    if not doc:
        raise NotRegistered("""
            `%s` has not been registered in the document registry.
            Importing the document class automatically registers it, has it
            been imported?
        """.strip() % name)
    return doc
