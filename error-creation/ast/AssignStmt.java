/** Name = Expr ; */
public class AssignStmt extends Stmt {
    private final Name target;
    private final Expr value;

    public AssignStmt(Name target, Expr value) {
        this.target = target;
        this.value = value;
    }

    String inline(int t) {
        return target + " = " + value + ";";
    }
}
