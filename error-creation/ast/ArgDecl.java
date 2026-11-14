/** Argdecl -> Type id | Type id [ ] */
public class ArgDecl {
    private final String type;
    private final String id;
    private final boolean isArray;

    public ArgDecl(String type, String id, boolean isArray) {
        this.type = type;
        this.id = id;
        this.isArray = isArray;
    }

    public String toString() {
        return type + " " + id + (isArray ? "[]" : "");
    }
}
