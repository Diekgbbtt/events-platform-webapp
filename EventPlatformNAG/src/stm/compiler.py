from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener
from stm.parser import SecurityModelVisitor, SecurityModelParser, SecurityModelLexer
from ocl.compiler import LambdaVisitor
import ast
from range import Range


class SecurityModelError(Exception):
    def __init__(self, range: Range | None, msg = 'Security model error'):
        self.range = range
        self.msg = msg
        self.severity = "error"

common_vars = {
    'create': {"caller"},
    'delete': {"caller","self"},
    'read': {"caller","self"},
    'update': {"caller","self","value"},
    'add': {"caller","self","value"},
    'remove': {"caller","self","value"},
    'execute': {"caller","self"},
}

DEFAULT = 'default'
ANONYMOUS = 'anonymous'

actions = common_vars.keys()

class STMErrorListener(ErrorListener):

    def __init__(self):
        super(STMErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise SecurityModelError(Range(line, column, line, column), f"Syntax error: {msg}")


def parseLambda(lambda_string):
    tree = ast.parse(lambda_string, mode='eval')
    lambda_node = tree.body
    if isinstance(lambda_node, ast.Lambda):
        args = [arg.arg for arg in lambda_node.args.args] 
        body = ast.unparse(lambda_node.body) 
        return args, body
    else:
        raise ValueError("Provided string is not a lambda expression.") 

def expandLambda(constraint,vars):
    if len(vars) != 0:
        signatures, body = parseLambda(constraint[1:-1])
        new_signatures = ", ".join([f"{arg}=None" for arg in list(vars.union(set(signatures)))])
        return f"(lambda {new_signatures}: {body})"
    else:
        return constraint

class JSONVisitor(LambdaVisitor,SecurityModelVisitor):
    def __init__(self,dm,dm_file_extensions=None):
        super().__init__(dm,dm_file_extensions)
        self.securitymodel = {}
        self.datamodel = dm
        self.userClass = None
        self.roles = []
        self.defaultRole = None
        self.anonymousRole = None
        self.policy = {}
        self.default = False
        self.anonymous = False

        self.current_role = None
        self.current_resource = None
        self.current_actions = set()
        self.current_constraint = None
        self.current = {}


    def visitSecurityModel(self, ctx):
        self.visitChildren(ctx)
        if self.defaultRole == None:
            raise SecurityModelError(None, "No default role declared")
        if self.anonymousRole == None:
            raise SecurityModelError(None, "No anonymous role declared")
        self.securitymodel["userClass"]=self.userClass
        self.securitymodel["roles"]=self.roles
        self.securitymodel["defaultRole"]=self.defaultRole
        self.securitymodel["anonymousRole"]=self.anonymousRole
        self.securitymodel["policy"]=self.policy 

    def visitUserClass(self, ctx):
        uc = ctx.ResourceName().getText()
        cs = list(map(lambda c: c["class"],filter((lambda c: "isAssociation" not in c and "isEnum" not in c),self.datamodel)))
        if uc not in cs:
            raise SecurityModelError(
                Range.from_context(ctx.ResourceName()), 
                f"User class '{uc}' is not defined in the data model")
        self.userClass = uc

    def visitRoles(self, ctx):
        self.visitChildren(ctx)
        # validate roles
        
        def traverse(r,rs):
            if r in rs:
                raise SecurityModelError(Range.from_context(ctx), f"Role {r} cannot inherit from itself")
            else:
                drs = list(filter(lambda e: e["name"]==r,self.roles))
                if len(drs) > 0:
                    if len(drs) == 1:
                        dr = drs[0]
                        if "extends" in dr and dr["extends"]:
                            return traverse(dr["extends"],rs+[r])
                        else:
                            return False
                    else:
                        raise SecurityModelError(Range.from_context(ctx), f"Role {r} declared multiple times")
                else:
                    raise SecurityModelError(Range.from_context(ctx), f"Role {r} not declared")
        res = list(map(lambda e: traverse(e["name"],[]), self.roles))
        if sum(res) != 0:
            raise SecurityModelError(Range.from_context(ctx), f"Malformed roles")

    def visitSrole(self, ctx):
        if DEFAULT in ctx.getText():
            self.default = True 
        if ANONYMOUS in ctx.getText():
            self.anonymous = True 
        self.visitChildren(ctx)

    def visitRole(self, ctx):
        self.current_role = ctx.RoleName()[0].getText()
        if self.default:
            if self.defaultRole == None:
                self.defaultRole=self.current_role
                self.default=False
            else:
                raise SecurityModelError(Range.from_context(ctx.RoleName()[0]), "Multiple default roles specified.")
        if self.anonymous:
            if self.anonymousRole == None:
                self.anonymousRole=self.current_role
                self.anonymous=False
            else:
                raise SecurityModelError(Range.from_context(ctx.RoleName()[0]), "Multiple anonymous roles specified.")
        role = {"name":self.current_role}
        parent = ""
        if len(ctx.RoleName())>1:
            parent = ctx.RoleName()[1].getText()
            role["extends"] = parent
        self.visitChildren(ctx)
        self.roles.append(role)
        self.policy["Role." + self.current_role]=self.current
        self.current_role = None
        self.current={}

    def visitResource(self, ctx):
        uc=ctx.ResourceName().getText()
        cs = list(map(lambda c: c["class"],filter((lambda c: "isAssociation" not in c and "isEnum" not in c),self.datamodel)))
        if uc not in cs:
            raise SecurityModelError(
                Range.from_context(ctx.ResourceName()), 
                f"Class '{uc}' is not defined in the data model")
        self.current_resource = uc
        self.current[self.current_resource]={}
        self.visitChildren(ctx)
        self.current_resource=None

    def visitActionResource(self, ctx):
        action = ctx.ActionType().getText()
        pairs = self.allSubresources(action)
        for p in pairs:
            self.current_actions.add(p)

    # returns all pairs of actions and subresources for self.current_resource
    # if a is fullAccess, return all possible (simple action, subresource) pairs
    def allSubresources(self, action):
        action_resource_pairs = []
         # We decompose to all possible (simple) actions and subresources
        if action == "fullAccess":
            target_actions = ["create", "delete"]
            for a in target_actions:
                action_resource_pairs.append((a, self.current_resource))

        if action in ["read", "fullAccess"]:
            target_actions = ["read"]
            for a in target_actions:
                current_resource = list(filter((lambda c: c["class"] == self.current_resource), self.datamodel))[0]
                for attr in current_resource['attributes']:
                    action_resource_pairs.append((a, attr['name']))

                ends = list(map(lambda c: c["ends"],
                    filter((lambda c: "isAssociation" in c),self.datamodel)))
                end1 = list(map(lambda e: e[1]["name"],
                    filter(lambda e: (e[0]["target"]==self.current_resource) ,ends)))            
                end2 = list(map(lambda e: e[0]["name"],
                    filter(lambda e: (e[1]["target"]==self.current_resource) ,ends)))
                for end in end1 + end2:
                    action_resource_pairs.append((a, end))

                if self.userClass == self.current_resource:
                    action_resource_pairs.append((a, 'role'))
        
        if action in ["update", "fullAccess"]:
            target_actions = ["update"]
            for a in target_actions:
                current_resource = list(filter((lambda c: c["class"] == self.current_resource), self.datamodel))[0]
                for attr in current_resource['attributes']:
                    action_resource_pairs.append((a, attr['name']))

                ends = list(map(lambda c: c["ends"],
                    filter((lambda c: "isAssociation" in c),self.datamodel)))
                end1 = list(map(lambda e: e[1]["name"],
                    filter(lambda e: (e[0]["target"]==self.current_resource and e[1]["mult"]=="1") ,ends)))            
                end2 = list(map(lambda e: e[0]["name"],
                    filter(lambda e: (e[1]["target"]==self.current_resource and e[0]["mult"]=="1") ,ends)))
                for end in end1 + end2:
                    action_resource_pairs.append((a, end))

                if self.userClass == self.current_resource:
                    action_resource_pairs.append((a, 'role'))

        if action in ["add", "remove", "fullAccess"]:
            target_actions = ["add", "remove"] if action == "fullAccess" else [action]
            for a in target_actions:
                current_resource = list(filter((lambda c: c["class"] == self.current_resource), self.datamodel))[0]

                ends = list(map(lambda c: c["ends"],
                    filter((lambda c: "isAssociation" in c),self.datamodel)))
                end1 = list(map(lambda e: e[1]["name"],
                    filter(lambda e: (e[0]["target"]==self.current_resource and e[1]["mult"]=="*") ,ends)))            
                end2 = list(map(lambda e: e[0]["name"],
                    filter(lambda e: (e[1]["target"]==self.current_resource and e[0]["mult"]=="*") ,ends)))
                for end in end1 + end2:
                    action_resource_pairs.append((a, end))      

        if action in ["create", "delete"]:
            action_resource_pairs.append((action, self.current_resource))

        return action_resource_pairs    


    def visitActionAttribute(self, ctx):
        action = ctx.ActionType().getText()
        resource = self.current_resource
        subresource = ctx.attributeName().getText()
        if action in ["create", "delete"]:
            raise SecurityModelError(
                Range.from_context(ctx.attributeName()),
                "Create and delete actions apply only to resources and do not take subresources as parameters")
        self.validateSubresource(action, resource, subresource)
        self.current_actions.add((action,subresource))

    def validateSubresource(self, a, r, s):
        act = {
            "attr": ["read", "update"],
            "end-one": ["read", "update"],
            "end-many":["read", "add", "remove"],
            "meth":["execute"]
        }
        subresource_type = ""

        #Check ends
        ends = list(map(lambda c: c["ends"],
                        filter((lambda c: "isAssociation" in c),self.datamodel)))
        end0 = list(map(lambda e: e[0]["mult"],
                        filter(lambda e: (e[0]["name"]==s and e[1]["target"]==r) ,ends)))
        end1 = list(map(lambda e: e[1]["mult"],
                        filter(lambda e: (e[1]["name"]==s and e[0]["target"]==r) ,ends)))
        end = end0 + end1

        cls = list(filter((lambda c: c["class"] == r),self.datamodel))[0]

        #Check attributes
        attr = list(filter(lambda a: a["name"] == s,cls["attributes"]))

        #Check methods
        meth = list(filter(lambda m: m["name"] == s,cls["methods"]))

        if len(end) != 0:
            if "*" in end:
                subresource_type = "end-many"
            else:
                subresource_type = "end-one"

        elif len(attr) != 0:
            subresource_type = "attr"
        elif len(meth) != 0:
            subresource_type = "meth"
        elif self.userClass == cls["class"] and s == "role":
            subresource_type = "attr"
        else:
            raise SecurityModelError(None, f"Resourse {r} does not contain subresource {s}")

        if a not in act[subresource_type]:
            raise SecurityModelError(
                None, 
                f"Action {a} cannot be applied to {r}'s subresource {s}. Wrong subresource type")

    def visitActionUnconstrained(self, ctx):
        self.visit(ctx.actions())
        self.updatePermission('Constraint.fullAccess')
        if ctx.permissions():
            self.visit(ctx.permissions())

    def visitActionConstrained(self, ctx):
        self.visit(ctx.actions())
        self.visit(ctx.constraint())
        self.updatePermission(self.current_constraint)
        if ctx.permissions():
            self.visit(ctx.permissions())

    def merge(self, f1, f2):
        signature1, body1 = parseLambda(f1)
        signature2, body2 = parseLambda(f2)
        signatures = ", ".join([f"{arg}=None" for arg in list(set(signature1 + signature2))])
        body = f"({body1}) or ({body2})"
        return f"(lambda {signatures}: {body})"

    def updatePermission(self,c):
        current = self.current[self.current_resource] if self.current_resource != None else self.current
        for a,n in self.current_actions:
            a = "Action." + a
            if n in current:
                if a in current[n]:
                    if current[n][a] == 'Constraint.fullAccess' or c == 'Constraint.fullAccess':
                        current[n][a] = 'Constraint.fullAccess'
                    else:
                        current[n][a] = self.merge(current[n][a][1:-1], c[1:-1])
                else:
                    current[n][a] = c
            else:
                current[n] = {a : c}
        self.current_actions = set()
        self.current_constraint = None
        if self.current_resource != None:
            self.current[self.current_resource] = current
        else:
            self.current = current

    def visitConstraint(self, ctx):
        self.visit(ctx.oclExp())
        self.current_constraint = self.lambda_exp()
        fv = set(self.free_vars)
        self.reset()

        #TODO: Check if the constraint returns a boolean value (infer the return type of the labda
        #and c check if it is a Boolean) 

        # always allow the minimal subset among the action types
        acts = set(map(lambda a: a[0],self.current_actions))
        for a in common_vars.keys():
            if a in acts:
                if not fv.issubset(common_vars[a]):
                    raise SecurityModelError(
                        Range.from_context(ctx.oclExp()), 
                        f"Constraint '{self.current_constraint}' for action {a} must have at most {common_vars[a]} free variables")
                else:
                    self.current_constraint = expandLambda(self.current_constraint,common_vars[a]-fv)

                
        # for multiple update, adds and removes disallow value
        if len(set(filter(lambda a: a == "update", acts))) > 1 or len(set(filter(lambda a: a == "add", acts))) > 1 or len(set(filter(lambda a: a == "remove", acts))) > 1:
            if not fv.issubset({"caller","self"}):
                raise SecurityModelError(
                    Range.from_context(ctx.oclExp()), 
                    f"Constraint '{self.current_constraint}' for multiple update, add, or remove actions must have at most 'caller' and 'self' free variables")
            else:
                self.current_constraint = expandLambda(self.current_constraint, {"caller","self"}-fv)

        # for composite update, add and remove actions disallow value
        if ("update","*") in self.current_actions or ("add","*") in self.current_actions or ("remove","*") in self.current_actions:
            if not fv.issubset({"caller","self"}):
                raise SecurityModelError(
                    Range.from_context(ctx.oclExp()), 
                    f"Constraint '{self.current_constraint}' for composite update, add, or remove actions must have at most 'caller' and 'self' free variables")
            else:
                self.current_constraint = expandLambda(self.current_constraint, {"caller","self"}-fv)
            
        update = list(filter(lambda a: a[0]=="update",self.current_actions))
        add = list(filter(lambda a: a[0]=="add",self.current_actions))
        remove = list(filter(lambda a: a[0]=="remove",self.current_actions))

        # for a combination of update with add or remove actions disallow value
        if len(update) > 0 and (len(add) > 0 or len(remove) > 0):
            if not fv.issubset({"caller","self"}):
                raise SecurityModelError(
                    Range.from_context(ctx.oclExp()), 
                    f"Constraint '{self.current_constraint}' for combination of update with add or remove actions must have at most 'caller' and 'self' free variables")
            else:
                self.current_constraint = expandLambda(self.current_constraint, {"caller","self"}-fv)

        # for add and remove actions 
        if len(add) > 0 and len(remove) > 0:
            # on different subresources disallow value    
            if add[0][1] != remove[0][1]:
                if not fv.issubset({"caller","self"}):
                    raise SecurityModelError(
                        Range.from_context(ctx.oclExp()), 
                        f"Constraint '{self.current_constraint}' for add and remove actions on different subresources must have at most 'caller' and 'self' free variables")
                else:
                    self.current_constraint = expandLambda(self.current_constraint, {"caller","self"}-fv)

             


        

def compile(dm,s,dm_file_extensions=None):
    listener = STMErrorListener()

    input_stream = InputStream(s)
    lexer = SecurityModelLexer(input_stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(listener)

    stream = CommonTokenStream(lexer)
    parser = SecurityModelParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(listener)
    
    tree = parser.securityModel()
    visitor = JSONVisitor(dm,dm_file_extensions)
    tree.accept(visitor)
    return visitor.securitymodel, []

