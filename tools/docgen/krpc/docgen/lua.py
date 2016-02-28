from krpc.docgen.domain import Domain
from krpc.docgen.nodes import *
from krpc.docgen.utils import snakecase
from krpc.types import ValueType, ClassType, EnumType, ListType, DictionaryType, SetType, TupleType

class LuaDomain(Domain):

    name = 'lua'
    prettyname = 'Lua'
    sphinxname = 'lua'
    codeext = 'lua'

    type_map = {
        'double': 'number',
        'float': 'number',
        'int32': 'number',
        'int64': 'number',
        'uint32': 'number',
        'uint64': 'number',
        'bool': 'boolean',
        'string': 'string',
        'bytes': 'string'
    }

    value_map = {
        'null': 'nil',
        'true': 'True',
        'false': 'False'
    }

    def __init__(self, macros):
        super(LuaDomain, self).__init__(macros)

    def currentmodule(self, name):
        super(LuaDomain, self).currentmodule(name)
        return '.. currentmodule:: %s' % name

    def type(self, typ):
        if isinstance(typ, ValueType):
            return self.type_map[typ.protobuf_type]
        elif isinstance(typ, ClassType):
            return self.shorten_ref(typ.protobuf_type[6:-1])
        elif isinstance(typ, EnumType):
            return self.shorten_ref(typ.protobuf_type[5:-1])
        elif isinstance(typ, ListType):
            return 'List'
        elif isinstance(typ, DictionaryType):
            return 'Map'
        elif isinstance(typ, SetType):
            return 'Set'
        elif isinstance(typ, TupleType):
            return 'Tuple'
        else:
            raise RuntimeError('Unknown type \'%s\'' % str(typ))

    def type_description(self, typ):
        if isinstance(typ, ValueType):
            return self.type_map[typ.protobuf_type]
        elif isinstance(typ, ClassType):
            return ':class:`%s`' % self.type(typ)
        elif isinstance(typ, EnumType):
            return ':class:`%s`' % self.type(typ)
        elif isinstance(typ, ListType):
            return 'List of %s' % self.type_description(typ.value_type)
        elif isinstance(typ, DictionaryType):
            return 'Map from %s to %s' % (self.type_description(typ.key_type), self.type_description(typ.value_type))
        elif isinstance(typ, SetType):
            return 'Set of %s' % self.type_description(typ.value_type)
        elif isinstance(typ, TupleType):
            return 'Tuple of (%s)' % ', '.join(self.type_description(typ) for typ in typ.value_types)
        else:
            raise RuntimeError('Unknown type \'%s\'' % str(typ))

    def ref(self, obj):
        name = obj.fullname
        if isinstance(obj, Procedure) or isinstance(obj, Property) or \
           isinstance(obj, ClassMethod) or isinstance(obj, ClassStaticMethod) or isinstance(obj, ClassProperty) or \
           isinstance(obj, EnumerationValue):
            name = name.split('.')
            name[-1] = snakecase(name[-1])
            name = '.'.join(name)
        return self.shorten_ref(name)

    def see(self, obj):
        if isinstance(obj, Property) or isinstance(obj, ClassProperty) or isinstance(obj, EnumerationValue):
            prefix = 'attr'
        elif isinstance(obj, Procedure) or isinstance(obj, ClassMethod) or isinstance(obj, ClassStaticMethod):
            prefix = 'meth'
        elif isinstance(obj, Class) or isinstance(obj, Enumeration):
            prefix = 'class'
        else:
            raise RuntimeError(str(obj))
        return ':%s:`%s`' % (prefix, self.ref(obj))

    def paramref(self, name):
        return super(LuaDomain, self).paramref(snakecase(name))