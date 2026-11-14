/** while ( Expr ) Stmt */
public class WhileStmt extends Stmt {
    private final Expr cond;
    private final Stmt body;

    public WhileStmt(Expr cond, Stmt body) {
        this.cond = cond;
        this.body = body;
    }

    String inline(int t) {
        return "while (" + cond + ")" + body(body, t);
    }
}
