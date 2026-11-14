import java.util.Collections;
import java.util.List;

/** Phase 2 root: Program -> class id { Memberdecls } */
public class ClassProgram extends Program {
    private final String id;
    private final List<Node> members;

    public ClassProgram(String id, List<Node> members) {
        this.id = id;
        this.members = members;
    }

    public String toString(int t) {
        return tabs(t) + "class " + id + " " + braced(Collections.<Node>emptyList(), members, t);
    }
}
