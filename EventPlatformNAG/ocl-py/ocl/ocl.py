from forbiddenfruit import curse, reverse
from contextlib import contextmanager
from ocl.compiler import compile
import types
import inspect

class OCLError(Exception):
    def __init__(self, msg = 'OCL error'):
        self.msg = msg

### Extension methods

##############################
## Collection
##############################

def flat(xss):
    if not isinstance(xss, (list, dict, set)):
        raise OCLError("flat: input must be a collection (list, dict, or set)")
    if len(xss) == 0:
        return xss
    if type(list(xss)[0]) in [list, dict, set]:
        ret = [x for xs in xss for x in xs]
        if isinstance(xss, dict) or isinstance(xss, set):
            return dict.fromkeys(ret)
        else:
            return list(ret) 
    else:
        return xss


def dot(self, attr):
    if hasattr(self, attr):
        return getattr(self, attr)
    else:
        if isinstance(self, dict) or isinstance(self, set) or isinstance(self, list):
            return type(self)(flat([x.dot(attr) for x in self]))
        else:
            raise OCLError(f"Attribute '{attr}' not found in {self.__class__.__name__}")

def isCollection(c):
    return True if type(c) in [list,dict,set] else False

def iterate(self,acc,f):
    return [acc := f(acc,x) for x in self][-1] if self else acc

def any(self,f):
    return self.iterate(None, lambda a,e: e if f(e) else a)

def asBag(self):
    return list(self)

def asOrderedSet(self):
    return dict.fromkeys(self)

def asSequence(self):
    return list(self)

def asSet(self):
    return set(self)

def collect(self,f):
    return list(map(f, self))

def count(self,e):
    return len(list(filter(lambda x: x==e, self)))

def excludes(self,e):
    return e not in self

def excludesAll(self,es):
    return (set(self) - set(es)) == set(self)

def excluding(self,e):
    result = list(filter(lambda x: x!=e, self))  # Convert to list first
    if isinstance(self, dict):
        return dict.fromkeys(result)
    elif isinstance(self, set):
        return set(result)
    elif isinstance(self, list):
        return result
    else:
        raise OCLError("Internal: supported type only includes Set, Bag, and Sequence.")
    return result

def exists(self,f):
    return not all(not f(x) for x in self)

def flatten(self):
    def helper(l):
        ret = []
        for e in l:
            if isCollection(e):
                ret = ret + helper(e)
            else:
                ret.append(e)
        return ret
    result = helper(self)
    if isinstance(self, dict):
        return dict.fromkeys(result)
    elif isinstance(self, set):
        return set(result)
    elif isinstance(self, list):
        return list(result)
    else:
        raise OCLError("Internal: supported type only includes Set, Bag, and Sequence.")
    return result

def forAll(self,f):
    return all(f(x) for x in self)

def includes(self,e):
    return e in self

def includesAll(self,es):
    return set(self).union(set(es)) == set(self)

def including(self,e):
    result = list(self) + [e]
    if isinstance(self, dict):
        return dict.fromkeys(result)
    elif isinstance(self, set):
        return set(result)
    elif isinstance(self, list):
        return list(result)
    else:
        raise OCLError("Internal: supported type only includes Set, Bag, and Sequence.")
    return result

def isEmpty(self):
    return len(self) == 0

def isUnique(self,f):
    return len(self) == len(set(self.collect(f)))

def notEmpty(self):
    return len(self) > 0

def one(self,f):
    return len(list(filter(f, self))) == 1

def product(self,es):
    result = []
    for e1 in self:
        for e2 in es:
            result.append((e1,e2))
    if isinstance(self, dict):
        return dict.fromkeys(result)
    elif isinstance(self, set):
        return set(result)
    elif isinstance(self, list):
        return list(result)
    else:
        raise OCLError("Internal: supported type only includes Set, Bag, and Sequence.")
    return result

def reject(self,e):
    result = list(filter(lambda x: not e(x), self))  # Convert to list first
    if isinstance(self, dict):
        return dict.fromkeys(result)
    elif isinstance(self, set):
        return set(result)
    elif isinstance(self, list):
        return result
    else:
        raise OCLError("Internal: supported type only includes Set, Bag, and Sequence.")
    return result

def select(self,e):
    result = list(filter(e, self))  # Convert to list first
    if isinstance(self, dict):
        return dict.fromkeys(result)
    elif isinstance(self, set):
        return set(result)
    elif isinstance(self, list):
        return result  # Already a list
    else:
        raise OCLError("Internal: supported type only includes Set, Bag, and Sequence.")
    return result

def size(self):
    return len(self)

def sum(self):
    return float(self.iterate(0.0, lambda a, e: a + e))

##############################
## Set
##############################

# = compiled to ==

# - exists

# intersection exists

def symmetricDifference(self,es):
    return self.symmetric_difference(es)

# union exists

##############################
## OrderedSet
##############################

# = compiled to ==

def append(self,e):
    if isinstance(self, dict):
        self[e]=None
    elif isinstance(self, list):
        self += [e]
    else:
        raise OCLError("Internal: append not defined for this type")
    return self

def at(self,i):
    return list(self)[i]

def first(self):
    return list(self)[0]

def indexOf(self,e):
    return list(self).index(e)

def insertAt(self,i,e):
    result = list(self)[:i] + [e] + list(self)[i:]
    if isinstance(self, dict):
        return dict.fromkeys(result)
    elif isinstance(self, set):
        return set(result)
    elif isinstance(self, list):
        return list(result)
    else:
        raise OCLError("Internal: supported type only includes Set, Bag, and Sequence.")
    return result

def last(self):
    return list(self)[-1]

def prepend(self,e):
    result = [e] + list(self)
    if isinstance(self, dict):
        return dict.fromkeys(result)
    elif isinstance(self, set):
        return set(result)
    elif isinstance(self, list):
        return list(result)
    else:
        raise OCLError("Internal: supported type only includes Set, Bag, and Sequence.")
    return result

def subOrderedSet(self,b,e):
    return dict.fromkeys(list(self)[b:e])


##############################
## Bag
##############################

# = compiled to ==

def intersection(self, es):
    c = list()
    b = list(es)
    for x in self:
        if x in b:
            b.remove(x)
            c.append(x)
    return type(self)(c)

def union(self, es):
    return type(self)(list(self) + list(es))

##############################
## Sequence
##############################

# = compiled to ==

# append handled in OrderedSet

# at handled in OrderedSet

# first handled in OrderedSet

# indexOf handled in OrderedSet

# insertAt handled in OrderedSet

# last handled in OrderedSet

# prepend handled in OrderedSet

def subSequence(self,b,e):
    return list(self)[b:e]

# union handled in Bag



@contextmanager
def ocl_extensions():

    # save original methods that will be overridden
    append_backup = list.append
    count_backup = list.count

    # common collection methods
    collection = [dot,iterate,any,asBag,asOrderedSet,asSequence,asSet,
                collect,count,excludes,excludesAll,excluding,
                exists,flatten,forAll,includes,includesAll,including,
                isEmpty,isUnique,notEmpty,one,product,reject,select,size,sum]
    

    for ds in [list, set, dict]:
        for m in collection:
            curse(ds, str(m.__name__), m)

    # common list and dict methods (non-unique element collections)
    nonunique = [append,at,first,indexOf,insertAt,last,prepend]

    for ds in [list,dict]:
        for m in nonunique:
            curse(ds, str(m.__name__), m)

    # collection-specific methods
    curse(set,"symmetricDifference",symmetricDifference)
    curse(dict,"subOrderedSet",subOrderedSet)
    curse(list,"subSequence",subSequence)
    curse(list,"intersection",intersection)
    curse(list,"union",union)

    try:
        yield
    finally:

        # Restore original methods

        # restore common collection methods
        for ds in [list, set, dict]:
            for m in collection:
                reverse(ds, str(m.__name__))

        # restore common list and dict methods (non-unique element collections)
        for ds in [list,dict]:
            for m in nonunique:
                reverse(ds, str(m.__name__))

        # restore collection-specific methods
        reverse(set,"symmetricDifference")
        reverse(dict,"subOrderedSet")
        reverse(list,"subSequence")
        reverse(list,"intersection")
        reverse(list,"union")

        # restore overridden methods
        curse(list,"append",append_backup)
        curse(list,"count",count_backup)

def eval_python(func, **args):
    #Check if the code takes exactly args as parameters 
    sig = inspect.signature(func)
    _, _, kv, _, _, _, _ = inspect.getfullargspec(func)
    if set(sig.parameters.keys()) == set(args.keys()) or kv:
        #Evaluate the python code with (temporarily) extended primitive types
        with ocl_extensions():
            result = func(**args) if len(args) > 0 else func()
        #Eager evaluation
        result = result if not isinstance(result,types.GeneratorType) else list(result)
        return result
    else:
        raise OCLError(f"Provided values for Python code evaluation do not match the expected parameters. Missing parameters: {set(sig.parameters.keys()) - set(args.keys())}, Additional parameters: {set(args.keys())-set(sig.parameters.keys())}")

def eval_ocl(ocl, **valuation):
    #Compile OCL
    python, fv = compile(ocl)
    #Check that all and only free variables are provided in the valuation
    if set(valuation.keys()) == fv:
        # Create a globals dict that includes imported modules but preserves built-ins
        import sys
        import builtins
        eval_globals = dict(globals())
        
        # Get all built-in names dynamically
        builtin_names = set(dir(builtins))
        
        for name, module in sys.modules.items():
            if (not name.startswith('_') and 
                name not in builtin_names and
                hasattr(module, '__file__')):
                eval_globals[name] = module
        
        return eval_python(eval(python, eval_globals), **valuation)
    else:
        raise OCLError(f"Provided valuation does not match OCL free variables. Missing variables: {fv - set(valuation.keys())}, Additional variables: {set(valuation.keys()) - fv}")


# Types
class OCLType:
    pass

class OCLTypeVariable(OCLType):
    var = 0

    def gen_var():
        OCLTypeVariable.var = OCLTypeVariable.var+1
        return OCLTypeVariable.var

    def __init__(self):
        self._name = OCLTypeVariable.gen_var()
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self,n):
        self._name = n

class OCLAnyType(OCLType):
    pass

class IntegerType(OCLAnyType):
    pass

class BooleanType(OCLAnyType):
    pass

class RealType(OCLAnyType):
    pass

class StringType(OCLAnyType):
    pass

class TupleType(OCLAnyType):
    def __init__(self, *args):
        self.type=list(args)

class SetType(OCLAnyType):
    def __init__(self, arg):
        self.type = arg

class BagType(OCLAnyType):
    def __init__(self, arg):
        self.type = arg

class OrderedSetType(OCLAnyType):
    def __init__(self, arg):
        self.type = arg

class SequenceType(OCLAnyType):
    def __init__(self, arg):
        self.type = arg

# def foo(a):
#     match a: 
#         case TupleType(a):
#                 print(len(a))
#                 return
#         case Integer():
#                 print("int")
#                 return
#         case SetType(type=a):
#                 print("set")
#                 return

# Terms
from collections import defaultdict
import weakref

class OCLTerm():
    __refs__ = defaultdict(list)
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Automatically wrap the subclass __init__ method
        original_init = cls.__init__
        
        def wrapped_init(self, *args, **kwargs):
            # Add to references
            self.__refs__[self.__class__].append(weakref.ref(self))
            # Call the original __init__
            original_init(self, *args, **kwargs)
        
        cls.__init__ = wrapped_init

    def __init__(self):
        self.__refs__[self.__class__].append(weakref.ref(self))

    def __eq__(self, value): 
        return self.__dict__ == value.__dict__ if type(value) == type(self) else False
    
    def __hash__(self): 
        # Create hash from hashable attributes only
        try:
            return hash(frozenset(self.__dict__.items()))
        except TypeError:
            # Handle unhashable attributes by converting to strings or using object id
            hashable_items = []
            for key, val in self.__dict__.items():
                try:
                    hash(val)
                    hashable_items.append((key, val))
                except TypeError:
                    # For unhashable types, use their string representation or id
                    if hasattr(val, '__dict__'):
                        hashable_items.append((key, id(val)))
                    else:
                        hashable_items.append((key, str(val)))
            return hash(frozenset(hashable_items))

    def oclAsSet(self):
        return set(self)

    def oclIsUndefined(self):
        return False
    
    def oclIsInvalid(self):
        return False
    
    def oclIsTypeOf(self,c):
        return isinstance(self, c)
    
    def oclIsKindOf(self,c):
        return issubclass(type(self), c)
    
    @classmethod
    def allInstances(cls):
        return set(cls.instances())

    @classmethod
    def instances(cls):
        for inst_ref in cls.__refs__[cls]:
            inst = inst_ref()
            if inst is not None:
                yield inst

    # TODO: Move to the dtm generator
    # @classmethod
    # def allInstances(cls):
    #     return cls.query.all() if hasattr(cls,'query') else []
    
    def dot(self, attr):
        if hasattr(self, attr):
            return getattr(self, attr)
        else:
            raise OCLError(f"Attribute '{attr}' not found in {self.__class__.__name__}")
    
class OCLTuple(OCLTerm):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def allInstances(cls):
        raise OCLError("Cannot enumerate all Tuple instances")

