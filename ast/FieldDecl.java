/** Fielddecl -> Optionalfinal Type id Optionalexpr ; | Type id [ intlit ] ; */
public class FieldDecl extends Node {
    private final boolean isFinal;
    private final String type;
    private final String id;
    private final Expr init;
    private final String arraySize;

    private FieldDecl(boolean isFinal, String type, String id, Expr init, String arraySize) {
        this.isFinal = isFinal;
        this.type = type;
        this.id = id;
        this.init = init;
        this.arraySize = arraySize;
    }

    /** init is null when there is no initializer. */
    public static FieldDecl scalar(boolean isFinal, String type, String id, Expr init) {
        return new FieldDecl(isFinal, type, id, init, null);
    }

    public static FieldDecl array(String type, String id, String size) {
        return new FieldDecl(false, type, id, null, size);
    }

    public String toString(int t) {
        return tabs(t) + (isFinal ? "final " : "") + type + " " + id
            + (arraySize != null ? "[" + arraySize + "]" : "")
            + (init != null ? " = " + init : "")
            + ";";
    }
}
