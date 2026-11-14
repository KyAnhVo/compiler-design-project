/** if ( Expr ) Stmt IfEnd */
public class IfStmt extends Stmt {
    private final Expr cond;
    private final Stmt thenStmt;
    private final Stmt elseStmt;

    /** elseStmt is null when there is no else branch. */
    public IfStmt(Expr cond, Stmt thenStmt, Stmt elseStmt) {
        this.cond = cond;
        this.thenStmt = thenStmt;
        this.elseStmt = elseStmt;
    }

    String inline(int t) {
        String s = "if (" + cond + ")" + body(thenStmt, t);
        if (elseStmt == null) {
            return s;
        }
        s += thenStmt instanceof Block ? " else" : "\n" + tabs(t) + "else";
        return s + (elseStmt instanceof IfStmt ? " " + elseStmt.inline(t) : body(elseStmt, t));
    }
}
