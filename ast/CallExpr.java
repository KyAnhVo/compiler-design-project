import java.util.List;

/** id ( ) | id ( Args ) */
public class CallExpr extends Expr {
    private final String id;
    private final List<Expr> args;

    public CallExpr(String id, List<Expr> args) {
        this.id = id;
        this.args = args;
    }

    public String toString() {
        return id + "(" + Node.commas(args) + ")";
    }
}
