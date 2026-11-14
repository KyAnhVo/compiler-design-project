/** return ; | return Expr ; */
public class ReturnStmt extends Stmt {
    private final Expr value;

    /** value is null for a bare return. */
    public ReturnStmt(Expr value) {
        this.value = value;
    }

    String inline(int t) {
        return value == null ? "return;" : "return " + value + ";";
    }
}
