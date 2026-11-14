/** Expr Binaryop Expr */
public class BinaryExpr extends Expr {
    private final Expr left;
    private final String op;
    private final Expr right;

    public BinaryExpr(Expr left, String op, Expr right) {
        this.left = left;
        this.op = op;
        this.right = right;
    }

    public String toString() {
        return "(" + left + " " + op + " " + right + ")";
    }
}
