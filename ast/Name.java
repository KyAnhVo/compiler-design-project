/** Name -> id | id [ Expr ] */
public class Name extends Expr {
    private final String id;
    private final Expr index;

    /** index is null for a plain id. */
    public Name(String id, Expr index) {
        this.id = id;
        this.index = index;
    }

    public String toString() {
        return index == null ? id : id + "[" + index + "]";
    }
}
