import java.util.List;

/** read ( Readlist ) ; | print ( Printlist ) ; | printline ( Printlinelist ) ; */
public class IoStmt extends Stmt {
    private final String keyword;
    private final List<? extends Expr> items;

    public IoStmt(String keyword, List<? extends Expr> items) {
        this.keyword = keyword;
        this.items = items;
    }

    String inline(int t) {
        return keyword + "(" + commas(items) + ");";
    }
}
