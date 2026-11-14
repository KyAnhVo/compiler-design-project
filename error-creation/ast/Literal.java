/** intlit | charlit | strlit | floatlit | true | false, kept as the source lexeme. */
public class Literal extends Expr {
    private final String lexeme;

    public Literal(String lexeme) {
        this.lexeme = lexeme;
    }

    public String toString() {
        return lexeme;
    }
}
