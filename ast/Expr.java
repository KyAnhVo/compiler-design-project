/**
 * Name, call and literal nodes are atoms and print bare, as in the expected
 * output (vals[0], sqrt(x), 0.0). Every other node prints its own parentheses,
 * which is what makes the shape of the tree visible.
 */
public abstract class Expr {
    public abstract String toString();
}
