from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener
from ptm.parser import PrivacyModelVisitor, PrivacyModelParser, PrivacyModelLexer
from ocl.compiler import LambdaVisitor
from stm.compiler import expandLambda
from range import Range


class PrivacyModelWarning(Exception):
    def __init__(self, range: Range | None, msg='Privacy model warning'):
        self.range = range
        self.msg = msg
        self.severity = "warning"

class PrivacyModelError(Exception):
    def __init__(self, range: Range | None, msg='Privacy model error'):
        self.range = range
        self.msg = msg
        self.severity = "error"

class PTMErrorListener(ErrorListener):

    def __init__(self):
        super(PTMErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise PrivacyModelError(Range(line, column, line, column), f"Syntax error: {msg}")

class JSONVisitor(LambdaVisitor,PrivacyModelVisitor):
    def __init__(self,dm,sm,dm_file_extensions):
        super().__init__(dm,dm_file_extensions)
        self.privacymodel = {}
        self.datamodel = dm
        self.personaldata = []
        self.purposes = []
        self.policy = []
        self.current_constraint = "true"
        self.current_desc = "true"
        self.securitymodel = sm
        self.userClass = sm["userClass"]
        self.warnings = []
        
    def getPurpose(self, p):
        return list(filter(lambda e: e["name"]==p,self.purposes))

    def filter(self,ls):
        ls_ = []
        seen = set()

        for l in ls:  # assuming 'data' is your list of dictionaries
            data = (l['resource'], l['subresource'])
            if data not in seen:
                seen.add(data)
                ls_.append(l)
        return ls_

    def validatePersonalDataUsage(self):
        all_resources_usage = []
        for policy in self.policy:
            all_resources_usage += policy['resources']
        all_resources_usage = self.filter(all_resources_usage)

        for pd in self.personaldata:
            if not any(dpd['resource'] == pd['resource'] and dpd['subresource'] == pd['subresource'] for dpd in all_resources_usage):
                self.warnings.append(PrivacyModelWarning(
                    None,
                    f"Resource {pd['resource']} with subresource {pd['subresource']} is declared as personal data but never mentioned in the declared purposes."
                ))
                
    def visitPrivacyModel(self, ctx):
        self.visitChildren(ctx)
        self.privacymodel["personalData"]=self.filter(self.personaldata)
        self.privacymodel["purposes"]=self.purposes
        self.privacymodel["policy"]=self.policy

        self.validatePersonalDataUsage()

    def visitResources(self, ctx):
        r = ctx.ResourceName().getText()
        cs = list(map(lambda c: c["class"],filter((lambda c: "isEnum" not in c),self.datamodel)))
        if r not in cs:
            raise PrivacyModelError(
                Range.from_context(ctx.ResourceName()),
                f"Resource '{r}' is not defined in the data model")

        cls = list(filter((lambda c: c["class"] == r),self.datamodel))[0]
        ends = list(map(lambda c: c["ends"],
                        filter((lambda c: "isAssociation" in c),self.datamodel)))
        end0 = list(map(lambda e: e[0]["name"],
                        filter(lambda e: (e[1]["target"]==r) ,ends)))
        end1 = list(map(lambda e: e[1]["name"],
                        filter(lambda e: (e[0]["target"]==r) ,ends)))
        end = end0 + end1
        attr = list(map(lambda a: a["name"],cls["attributes"]))

        if self.userClass == r:
            attr.append('role')
    
        s = None
        if ctx.methodName():
            s = ctx.methodName().getText()
            
            if s not in end and s not in attr:
                raise PrivacyModelError(
                    Range.from_context(ctx.methodName()), 
                    f"Subresource '{s}' of resource '{r}' is not defined in the data model")
            self.personaldata.append({'resource': r, 'subresource': s})
        else:
            for s in end + attr:
                self.personaldata.append({'resource': r, 'subresource': s})
        
        self.visitChildren(ctx)

    def visitPurposes(self, ctx):
        self.visitChildren(ctx)
        # valudate purposes
        def traverse(p,pl):
            if p in pl:
                raise PrivacyModelError(
                    Range.from_context(ctx), 
                    f"Complex purpose '{p}' cannot contain itself")
            else:
                dps = self.getPurpose(p)
                if len(dps) > 0:
                    if len(dps) == 1:
                        dp = dps[0]
                        if "includes" in dp and dp["includes"]:
                            res = list(map(lambda e: traverse(e,pl+[p]), dp["includes"]))
                            assert sum(res) == 0
                            return False
                        else:
                            return False
                    else:
                        raise PrivacyModelError(
                            Range.from_context(ctx),
                            f"Purpose '{p}' declared multiple times")
                else:
                    raise PrivacyModelError(
                        Range.from_context(ctx),
                        f"Purpose {p} not declared")
        res = list(map(lambda e: traverse(e["name"],[]), self.purposes))
        if sum(res) != 0:
            raise PrivacyModelError(
                Range.from_context(ctx),
                f"Malformed purposes")


                    

    def visitPurpose(self, p, sp, name_ctx):
        pp = self.getPurpose(p)
        if len(pp) == 0:
            self.purposes.append({
                "name" : p,
                "endpoints" : [],
                "includes" : sp
            })
        else:
            raise PrivacyModelError(
                name_ctx,
                f"Purpose {p} already declared")

    def visitSimplePurpose(self, ctx):
        p = ctx.PurposeName().getText()
        self.visitPurpose(p,[],ctx.PurposeName())
        self.visitChildren(ctx)
        
    def visitComplexPurpose(self, ctx):
        p = ctx.PurposeName()[0].getText()
        ps = list(map(lambda e: e.text,ctx.pss))
        self.visitPurpose(p,ps,ctx.PurposeName()[0])
        self.visitChildren(ctx)

    def visitApurpose(self, ctx):
        if ctx.getChild(0).getText() == 'main':
            r = None
            m = ctx.getChild(0).getText()        
        else:
            r = ctx.ResourceName().getText()
            m = ctx.methodName().getText()
            
            # validate r
            cs = list(map(lambda c: c["class"],filter((lambda c: "isEnum" not in c),self.datamodel)))
            if r not in cs:
                raise PrivacyModelError(
                    Range.from_context(ctx.ResourceName()),
                    f"Resource '{r}' is not defined in the data model")
        
            #validate m
            cls = list(filter((lambda c: c["class"] == r),self.datamodel))[0]
            meth = list(filter(lambda e: e["name"] == m,cls["methods"]))
            if len(meth) == 0:            
                raise PrivacyModelError(
                    Range.from_context(ctx.ResourceName()),
                    f"Resourse '{r}' does not contain subresource '{m}'")

        p = ctx.PurposeName().getText()
        
        #validate p
        dps = self.getPurpose(p)
        if len(dps) == 0:
            raise PrivacyModelError(
                Range.from_context(ctx.ResourceName()),
                f"Purpose '{p}' not declared")

        dp = dps[0]
        dp["endpoints"].append({
            "class" : r,
            "met" : m
        })

        self.visitChildren(ctx)

    def visitDpurpose(self, ctx):
        p = ctx.PurposeName().getText()

        #validate p
        dp = self.getPurpose(p)
        if len(dp) == 0:
            raise PrivacyModelError(
                Range.from_context(ctx.PurposeName()),
                f"Purpose '{p}' not declared")

        if ctx.constraint():
            self.visit(ctx.constraint())
            self.visit(ctx.desc())

        # Validate subresources
        def validateSubresource(r,s):
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

            if len(end) != 0 or \
            len(attr) != 0 or \
            len(meth) != 0 or \
            (self.userClass == cls["class"] and s == "role"):
                pass
            else:
                raise PrivacyModelError(
                    Range.from_context(ctx.PurposeName()),
                    f"Resourse '{r}' does not contain subresource '{s}'")

        rs = []
        
        for i in range(len(ctx.rs)):
            r = ctx.rs[i].text
            m = None
            if not any(item['resource'] == r for item in self.personaldata):
                raise PrivacyModelError(
                    Range.from_context(ctx.PurposeName()),
                    f"Resource '{r}' is not personal data")
          
            if i < len(ctx.ms):
                m = ctx.ms[i].getText()
                if not any(item['resource'] == r and (item['subresource'] == m or item['subresource'] is None) for item in self.personaldata):
                    raise PrivacyModelError(
                        Range.from_context(ctx.PurposeName()),
                        f"Subresource '{m}' of '{r}' is not personal data")
                validateSubresource(r,m)
                rs.append({
                    "resource" : r,
                    "subresource" : m
                })
            else:
                cls = list(filter((lambda c: c["class"] == r),self.datamodel))[0]
                ends = list(map(lambda c: c["ends"],
                                filter((lambda c: "isAssociation" in c),self.datamodel)))
                end0 = list(map(lambda e: e[0]["name"],
                                filter(lambda e: (e[1]["target"]==r) ,ends)))
                end1 = list(map(lambda e: e[1]["name"],
                                filter(lambda e: (e[0]["target"]==r) ,ends)))
                end = end0 + end1
                attr = list(map(lambda a: a["name"],cls["attributes"]))
                for m in end + attr:
                    rs.append({
                        "resource" : r,
                        "subresource" : m
                    })

            
        self.policy.append({
            "purpose" : p,
            "action" : "read",
            "resources" : rs,
            "constraint" : {
                "ocl" : self.current_constraint,
                "desc" : self.current_desc
            }
        })
        
        self.current_constraint = "true"
        self.current_desc = "true"
        if ctx.dpurpose():
            self.visit(ctx.dpurpose())

    def visitDesc(self, ctx):
        words = list(map(lambda w: w.text,ctx.words))
        self.current_desc = " ".join(words)
    
    def visitConstraint(self, ctx):
        self.visit(ctx.oclExp())
        self.current_constraint = self.lambda_exp()
        fv = set(self.free_vars)
        self.reset()
        
        if not fv.issubset({"self"}):
            raise PrivacyModelError(
                Range.from_context(ctx.oclExp()),
                f"Constraint '{self.current_constraint}' defining applicability of a declared purpose can have at most 'self' free variable")
        else:
            self.current_constraint = expandLambda(self.current_constraint, {"self"}-fv)


def compile(dm,sm,s,dm_file_extensions=None):
    listener = PTMErrorListener()

    input_stream = InputStream(s)
    lexer = PrivacyModelLexer(input_stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(listener)

    stream = CommonTokenStream(lexer)
    parser = PrivacyModelParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(listener)
    
    tree = parser.privacyModel()
    visitor = JSONVisitor(dm,sm,dm_file_extensions)
    tree.accept(visitor)
    return visitor.privacymodel, visitor.warnings

