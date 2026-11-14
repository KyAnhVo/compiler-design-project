/** Name ++ ; | Name -- ; */
public class IncDecStmt extends Stmt {
    private final Name target;
    private final String op;

    public IncDecStmt(Name target, String op) {
        this.target = target;
        this.op = op;
    }

    String inline(int t) {
        return target + op + ";";
    }
}
