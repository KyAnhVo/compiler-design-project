import java.util.List;
import java.util.stream.Collectors;

/**
 * Base of every AST node that spans whole lines. t is the indentation depth,
 * in tabs, of the line the node starts on.
 */
public abstract class Node {
    public abstract String toString(int t);

    static String tabs(int t) {
        return "\t".repeat(t);
    }

    static String lines(List<? extends Node> nodes, int t) {
        return nodes.stream().map(n -> n.toString(t)).collect(Collectors.joining("\n"));
    }

    static String commas(List<?> items) {
        return items.stream().map(Object::toString).collect(Collectors.joining(", "));
    }

    /** A brace-delimited scope whose closing brace sits at depth t. A blank line separates decls from stmts. */
    static String braced(List<? extends Node> decls, List<? extends Node> stmts, int t) {
        String body = lines(decls, t + 1);
        if (!decls.isEmpty() && !stmts.isEmpty()) {
            body += "\n\n";
        }
        body += lines(stmts, t + 1);
        return "{\n" + (body.isEmpty() ? "" : body + "\n") + tabs(t) + "}";
    }
}
