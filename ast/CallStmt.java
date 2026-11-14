/** id ( ) ; | id ( Args ) ; */
public class CallStmt extends Stmt {
    private final CallExpr call;

    public CallStmt(CallExpr call) {
        this.call = call;
    }

    String inline(int t) {
        return call + ";";
    }
}
