import java.util.List;

/** Phase 1 root: Program -> Stmts */
public class StmtsProgram extends Program {
    private final List<Stmt> stmts;

    public StmtsProgram(List<Stmt> stmts) {
        this.stmts = stmts;
    }

    public String toString(int t) {
        return lines(stmts, t);
    }
}
