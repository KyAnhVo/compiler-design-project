public abstract class Stmt extends Node {
    /** The statement without the indentation of its first line. t still applies to any later lines. */
    abstract String inline(int t);

    public String toString(int t) {
        return tabs(t) + inline(t);
    }

    /** The body of an if/else/while headed at depth t: a block stays on the header line, anything else is indented below it. */
    static String body(Stmt s, int t) {
        return s instanceof Block ? " " + s.inline(t) : "\n" + s.toString(t + 1);
    }
}
