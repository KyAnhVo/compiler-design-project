/** ~ Expr | - Expr | + Expr */
public class UnaryExpr extends Expr {
    private final String op;
    private final Expr operand;

    public UnaryExpr(String op, Expr operand) {
        this.op = op;
        this.operand = operand;
    }

    public String toString() {
        return "(" + op + operand + ")";
    }
}
