/** ( Type ) Expr */
public class CastExpr extends Expr {
    private final String type;
    private final Expr operand;

    public CastExpr(String type, Expr operand) {
        this.type = type;
        this.operand = operand;
    }

    public String toString() {
        return "((" + type + ") " + operand + ")";
    }
}
