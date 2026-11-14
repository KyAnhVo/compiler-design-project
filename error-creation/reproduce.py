#!/usr/bin/env python3
"""Rebuilds the project with one fix undone at a time and records the raw tool output in errors.txt."""
import difflib, os, re, shutil, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
VARIANTS = os.path.join(ROOT, "variants")
CUPJAR = os.path.join(ROOT, "java-cup-11b.jar")
JFLEXJAR = os.path.join(ROOT, "jflex-full-1.8.2.jar")
ASTDIR = os.path.join(ROOT, "ast")
MAX_LINES = 45

def read(path):
    with open(os.path.join(ROOT, path)) as f:
        return f.read()

def rep(old, new):
    def patch(src):
        assert src.count(old) == 1, old
        return src.replace(old, new)
    return patch

def regex(pattern, new):
    def patch(src):
        out, n = re.subn(pattern, new, src, flags=re.M)
        assert n >= 1, pattern
        return out
    return patch

INLINED_BINOPS = regex(r"^       \| Expr:l \w+ Expr:r \{: RESULT = new BinaryExpr\(l, \"[^\"]+\", r\); :\}\n", "")
BINARYOP = [
    INLINED_BINOPS,
    rep("non terminal Expr Expr;", "non terminal Expr Expr;\nnon terminal String Binaryop;"),
    rep("       | LPAREN Expr:c QUESTION_MARK",
        "       | Expr:l Binaryop:o Expr:r {: RESULT = new BinaryExpr(l, o, r); :}\n       | LPAREN Expr:c QUESTION_MARK"),
    rep("Type ::= INT",
        "Binaryop ::= MUL {: RESULT = \"*\"; :} | DIV {: RESULT = \"/\"; :} | ADD {: RESULT = \"+\"; :} | SUB {: RESULT = \"-\"; :}\n"
        "           | LT {: RESULT = \"<\"; :} | GT {: RESULT = \">\"; :} | LTE {: RESULT = \"<=\"; :} | GTE {: RESULT = \">=\"; :}\n"
        "           | EQ {: RESULT = \"==\"; :} | LTGT {: RESULT = \"<>\"; :} | LOR {: RESULT = \"||\"; :} | LAND {: RESULT = \"&&\"; :}\n"
        "           ;\n\nType ::= INT"),
]

NUMERIC_TERMINALS = rep("terminal String ID, STRLIT, CHARLIT, INTLIT, FLOATLIT;",
                        "terminal String ID, STRLIT, CHARLIT;\nterminal Integer INTLIT;\nterminal Float FLOATLIT;")
NUMERIC_LEXER = [rep("{return newSym(sym.INTLIT, yytext());}", "{return newSym(sym.INTLIT, Integer.valueOf(yytext()));}"),
                 rep("{return newSym(sym.FLOATLIT, yytext());}", "{return newSym(sym.FLOATLIT, Float.valueOf(yytext()));}")]

PHASE1, PHASE2, LEXER = "phase1/grammar.cup", "phase2/grammar.cup", "tokens.jflex"
THROW_RULE = "[^]             { throw new ScannerException(yytext(), yyline + 1, yycolumn + 1); }"

# (id, undone change, phase, {file: patches}, [(input, expected stdout)])
CASES = [
 ("00-control", "nothing undone", 2, {}, [("class c { void m() { x = 1 + 2 * 3; } }",
    "class c {\n\tvoid m(){\n\t\tx = (1 + (2 * 3));\n\t}\n}")]),
 ("01-binaryop-nonterminal", "Binaryop as its own nonterminal", 1, {PHASE1: BINARYOP},
    [("x = 1 + 2 * 3;", "x = (1 + (2 * 3));"), ("x = 1 * 2 + 3;", "x = ((1 * 2) + 3);"), ("x = 1 - 2 - 3;", "x = ((1 - 2) - 3);")]),
 ("02-no-precedence", "all precedence declarations removed", 1,
    {PHASE1: [regex(r"^precedence .*\n", ""), regex(r" %prec \w+", "")]}, []),
 ("03-precedence-reversed", "precedence levels declared highest first", 1,
    {PHASE1: [rep("precedence left LOR;\nprecedence left LAND;\nprecedence left EQ, LTGT;\nprecedence left LT, GT, LTE, GTE;\nprecedence left ADD, SUB;\nprecedence left MUL, DIV;\n",
                  "precedence left MUL, DIV;\nprecedence left ADD, SUB;\nprecedence left LT, GT, LTE, GTE;\nprecedence left EQ, LTGT;\nprecedence left LAND;\nprecedence left LOR;\n")]},
    [("x = 1 + 2 * 3;", "x = (1 + (2 * 3));")]),
 ("04-unary-no-prec", "%prec UNARY removed from - and +", 1,
    {PHASE1: [rep('SUB Expr:e {: RESULT = new UnaryExpr("-", e); :} %prec UNARY', 'SUB Expr:e {: RESULT = new UnaryExpr("-", e); :}'),
              rep('ADD Expr:e {: RESULT = new UnaryExpr("+", e); :} %prec UNARY', 'ADD Expr:e {: RESULT = new UnaryExpr("+", e); :}')]},
    [("x = -a * b;", "x = ((-a) * b);")]),
 ("05-tilde-no-prec", "%prec UNARY removed from ~", 1,
    {PHASE1: [rep('TILDE Expr:e {: RESULT = new UnaryExpr("~", e); :} %prec UNARY', 'TILDE Expr:e {: RESULT = new UnaryExpr("~", e); :}')]},
    [("x = ~a * b;", "x = ((~a) * b);"), ("x = ~a + b;", "x = ((~a) + b);")]),
 ("06-cast-no-prec", "%prec CAST removed", 1,
    {PHASE1: [rep("new CastExpr(t, e); :} %prec CAST", "new CastExpr(t, e); :}")]},
    [("x = (int)a * b;", "x = (((int) a) * b);"), ("x = (int)a + b;", "x = (((int) a) + b);")]),
 ("07-phase1-missing-type", "Type undefined in Phase 1, as in the Phase 1 table of the spec", 1,
    {PHASE1: [regex(r"^non terminal String Type;\n", ""),
              regex(r"^Type ::= INT[\s\S]*?^       ;\n", "")]}, []),
 ("08-unused-terminals-removed", "CLASS, FINAL, VOID removed from Phase 1 terminals", 1,
    {PHASE1: [rep("terminal CLASS, FINAL, VOID, INT,", "terminal INT,")]}, []),
 ("09-memberdecls-as-spec", "Memberdecls -> Fielddecls Methoddecls", 2,
    {PHASE2: [rep("Memberdecls ::= Fielddecl:f Memberdecls:rest {: rest.addFirst(f); RESULT = rest; :}\n              | Methoddecls:m {: RESULT = m; :}\n              ;",
                  "Memberdecls ::= Fielddecls:f Methoddecls:m {: LinkedList<Node> all = new LinkedList<Node>(f); all.addAll(m); RESULT = all; :} ;")]}, []),
 ("10-optionalfinal-as-spec", "Optionalfinal as its own nonterminal", 2,
    {PHASE2: [rep("non terminal Expr Optionalexpr;", "non terminal Expr Optionalexpr;\nnon terminal Boolean Optionalfinal;"),
              rep("Fielddecl ::= FINAL Type:t ID:i Optionalexpr:e SEMICOLON {: RESULT = FieldDecl.scalar(true, t, i, e); :}\n            | Type:t ID:i Optionalexpr:e SEMICOLON {: RESULT = FieldDecl.scalar(false, t, i, e); :}",
                  "Optionalfinal ::= FINAL {: RESULT = true; :} | {: RESULT = false; :} ;\n\nFielddecl ::= Optionalfinal:o Type:t ID:i Optionalexpr:e SEMICOLON {: RESULT = FieldDecl.scalar(o, t, i, e); :}")]}, []),
 ("11-returntype-as-spec", "Returntype as its own nonterminal", 2,
    {PHASE2: [rep("non terminal Expr Optionalexpr;", "non terminal Expr Optionalexpr;\nnon terminal String Returntype;"),
              rep("Methoddecl ::= Type:t ID:i LPAREN Argdecls:a RPAREN LBRACE Fielddecls:f Stmts:s RBRACE Optionalsemi:semi\n                  {: RESULT = new MethodDecl(t, i, a, f, s, semi); :}\n             | VOID ID:i LPAREN Argdecls:a RPAREN LBRACE Fielddecls:f Stmts:s RBRACE Optionalsemi:semi\n                  {: RESULT = new MethodDecl(\"void\", i, a, f, s, semi); :}",
                  "Returntype ::= Type:t {: RESULT = t; :} | VOID {: RESULT = \"void\"; :} ;\n\nMethoddecl ::= Returntype:t ID:i LPAREN Argdecls:a RPAREN LBRACE Fielddecls:f Stmts:s RBRACE Optionalsemi:semi\n                  {: RESULT = new MethodDecl(t, i, a, f, s, semi); :}")]}, []),
 ("12-dangling-else", "NO_ELSE precedence removed from IfEnd", 2,
    {PHASE2: [rep("{: RESULT = null; :} %prec NO_ELSE", "{: RESULT = null; :}"),
              rep("precedence nonassoc NO_ELSE;\nprecedence nonassoc ELSE;\n", ""),
              rep("terminal CAST, UNARY, NO_ELSE;", "terminal CAST, UNARY;")]}, []),
 ("13-numeric-literal-action", "INTLIT/FLOATLIT typed Integer/Float, actions unchanged", 1,
    {PHASE1: [NUMERIC_TERMINALS], LEXER: NUMERIC_LEXER}, []),
 ("14-numeric-literal-values", "INTLIT/FLOATLIT typed Integer/Float, converted with String.valueOf", 1,
    {PHASE1: [NUMERIC_TERMINALS, rep("INTLIT:l {: RESULT = new Literal(l); :}", "INTLIT:l {: RESULT = new Literal(String.valueOf(l)); :}"),
              rep("FLOATLIT:l {: RESULT = new Literal(l); :}", "FLOATLIT:l {: RESULT = new Literal(String.valueOf(l)); :}")],
     LEXER: NUMERIC_LEXER},
    [("x = 123456789.0;", "x = 123456789.0;"), ("x = 1.10;", "x = 1.10;"), ("x = 99999999999;", "x = 99999999999;")]),
 ("15-illegal-char-printed", "illegal char printed and skipped instead of thrown", 1,
    {LEXER: [rep(THROW_RULE, '.               { System.out.println("Illegal char, \'" + yytext() + "\' line: " + yyline + ", column: " + yycolumn); }')]},
    [("x = 1 # ;", "(no stdout, ScannerException on stderr)")]),
 ("16-catchall-dot", "catch-all rule written as . instead of [^]", 1,
    {LEXER: [rep(THROW_RULE, ".               { throw new ScannerException(yytext(), yyline + 1, yycolumn + 1); }")]},
    [("x = 1;\f", "(no stdout, ScannerException on stderr)")]),
]

def sh(cmd, cwd=ROOT):
    p = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=180)
    return p.returncode, p.stdout.replace(ROOT + "/", "")

def clip(text):
    lines = text.rstrip("\n").split("\n")
    if len(lines) <= MAX_LINES:
        return text.rstrip("\n")
    return "\n".join(lines[:MAX_LINES]) + f"\n[... {len(lines) - MAX_LINES} more lines, full text in the variant's output.txt ...]"

def run_case(case):
    cid, title, phase, patches, inputs = case
    vdir = os.path.join(VARIANTS, cid)
    build = os.path.join(vdir, "build")
    os.makedirs(build)
    files = {PHASE1 if phase == 1 else PHASE2: None, LEXER: None}
    diffs = []
    for name in files:
        original = read(name)
        src = original
        for patch in patches.get(name, []):
            src = patch(src)
        path = os.path.join(ROOT, name)
        if src != original:
            path = os.path.join(vdir, os.path.basename(name))
            with open(path, "w") as f:
                f.write(src)
            diffs.append("".join(difflib.unified_diff(original.splitlines(True), src.splitlines(True),
                         "working/" + name, "broken/" + name, n=1)))
        files[name] = path
    grammar = files[PHASE1 if phase == 1 else PHASE2]
    out = []
    def step(label, cmd):
        code, text = sh(cmd)
        out.append(f"$ {label}\n{text.rstrip()}\n[exit code {code}]")
        return code, text
    rel = lambda p: os.path.relpath(p, ROOT)
    code, cup = step(f"java -jar java-cup-11b.jar -interface -destdir {rel(build)} {rel(grammar)}",
                     ["java", "-jar", CUPJAR, "-interface", "-destdir", build, grammar])
    m = re.search(r"(\d+) conflicts? detected", cup)
    summary = {"cup_exit": code, "conflicts": m.group(1) if m else "?", "javac": "not reached", "runs": "not reached"}
    results = []
    if code == 0 and os.path.exists(os.path.join(build, "parser.java")):
        step(f"java -jar jflex-full-1.8.2.jar --nobak -d {rel(build)} {rel(files[LEXER])}",
             ["java", "-jar", JFLEXJAR, "--nobak", "-d", build, files[LEXER]])
        srcs = [os.path.join(build, n) for n in ("parser.java", "sym.java", "Lexer.java")]
        srcs += [os.path.join(ROOT, "ScannerTest.java")] + sorted(os.path.join(ASTDIR, n) for n in os.listdir(ASTDIR))
        code, _ = step(f"javac --release 11 -cp java-cup-11b.jar -d {rel(build)} <generated sources> ScannerTest.java ast/*.java",
                       ["javac", "--release", "11", "-cp", CUPJAR, "-d", build] + srcs)
        summary["javac"] = "ok" if code == 0 else f"failed ({code})"
        if code == 0:
            matched = []
            for i, (text, want) in enumerate(inputs):
                inp = os.path.join(vdir, f"input{i}.txt")
                with open(inp, "w") as f:
                    f.write(text)
                p = subprocess.run(["java", "-cp", f"{build}:{CUPJAR}", "ScannerTest", inp],
                                   capture_output=True, text=True, timeout=60)
                err = p.stderr.strip().split("\n")
                results.append(f"input:    {text!r}\nwanted:   {want!r}\nstdout:   {p.stdout!r}\nstderr:   {err[0] if err[0] else '(empty)'}\nexit:     {p.returncode}")
                matched.append(p.stdout == want or ("no stdout" in want and p.stdout == "" and "ScannerException" in p.stderr))
            summary["runs"] = "none" if not inputs else f"{sum(matched)}/{len(matched)} as wanted"
    shutil.rmtree(build)
    full = "\n\n".join(out)
    with open(os.path.join(vdir, "output.txt"), "w") as f:
        f.write(full + "\n")
    section = [f"{'=' * 78}\n{cid}\nUndone: {title}\nPhase: {phase}\n{'=' * 78}"]
    if diffs:
        section.append("--- CHANGE (- is the working version, + is the broken version) ---\n" + "\n".join(d.rstrip() for d in diffs))
    section.append("--- TOOL OUTPUT ---\n" + clip(full))
    if results:
        section.append("--- PROGRAM RUNS ---\n" + "\n\n".join(results))
    return summary, "\n\n".join(section)

def main():
    shutil.rmtree(VARIANTS, ignore_errors=True)
    rows, sections = [], []
    for case in CASES:
        summary, section = run_case(case)
        rows.append(f"{case[0]:<30} cup_exit={summary['cup_exit']} conflicts={summary['conflicts']:<4} javac={summary['javac']:<12} runs={summary['runs']}")
        sections.append(section)
        print(rows[-1], flush=True)
    with open(os.path.join(ROOT, "errors.txt"), "w") as f:
        f.write("Summary\n" + "\n".join(rows) + "\n\n" + "\n\n\n".join(sections) + "\n")

main()
