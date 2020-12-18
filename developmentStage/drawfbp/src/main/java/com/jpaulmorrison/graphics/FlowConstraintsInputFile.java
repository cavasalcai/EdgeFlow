package com.jpaulmorrison.graphics;

import java.util.List;

public class FlowConstraintsInputFile {

    private String id;
    private String e2e;
    private List<FlowConstraintPathComponent> path;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getE2e() {
        return e2e;
    }

    public void setE2e(String e2e) {
        this.e2e = e2e;
    }

    public List getPath() {
        return path;
    }

    public void setPath(List<FlowConstraintPathComponent> elem) {
        this.path = elem;
    }
}
