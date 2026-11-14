/** ( Expr ). Only adds parentheses around an atom; every other node already prints its own. */
public class ParenExpr extends Expr {
    private final Expr inner;

    public ParenExpr(Expr inner) {
        this.inner = inner;
    }

    public String toString() {
        boolean atom = inner instanceof Name || inner instanceof CallExpr || inner instanceof Literal;
        return atom ? "(" + inner + ")" : inner.toString();
    }
}
