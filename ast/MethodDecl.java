import java.util.List;

/** Methoddecl -> Returntype id ( Argdecls ) { Fielddecls Stmts } Optionalsemi */
public class MethodDecl extends Node {
    private final String returnType;
    private final String id;
    private final List<ArgDecl> args;
    private final List<FieldDecl> fields;
    private final List<Stmt> stmts;
    private final boolean semi;

    public MethodDecl(String returnType, String id, List<ArgDecl> args,
                      List<FieldDecl> fields, List<Stmt> stmts, boolean semi) {
        this.returnType = returnType;
        this.id = id;
        this.args = args;
        this.fields = fields;
        this.stmts = stmts;
        this.semi = semi;
    }

    public String toString(int t) {
        return tabs(t) + returnType + " " + id + "(" + commas(args) + ")"
            + braced(fields, stmts, t) + (semi ? ";" : "");
    }
}
