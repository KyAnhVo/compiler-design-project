/** ( Expr ? Expr : Expr ) */
public class TernaryExpr extends Expr {
    private final Expr cond;
    private final Expr ifTrue;
    private final Expr ifFalse;

    public TernaryExpr(Expr cond, Expr ifTrue, Expr ifFalse) {
        this.cond = cond;
        this.ifTrue = ifTrue;
        this.ifFalse = ifFalse;
    }

    public String toString() {
        return "(" + cond + " ? " + ifTrue + " : " + ifFalse + ")";
    }
}
