import java.util.Collections;
import java.util.List;

/** { Fielddecls Stmts } Optionalsemi */
public class Block extends Stmt {
    private final List<FieldDecl> fields;
    private final List<Stmt> stmts;
    private final boolean semi;

    public Block(List<FieldDecl> fields, List<Stmt> stmts, boolean semi) {
        this.fields = fields;
        this.stmts = stmts;
        this.semi = semi;
    }

    /** Phase 1 blocks cannot declare fields. */
    public Block(List<Stmt> stmts, boolean semi) {
        this(Collections.<FieldDecl>emptyList(), stmts, semi);
    }

    String inline(int t) {
        return braced(fields, stmts, t) + (semi ? ";" : "");
    }
}
