package com.jpaulmorrison.graphics;

import java.util.List;
import java.util.Map;

public class FlowConstraintPathComponent {

    private String src;
    private String dest;
    private List<Map> port;

    public String getSrc() {
        return src;
    }

    public void setSrc(String src) {
        this.src = src;
    }

    public String getDest() {
        return dest;
    }

    public void setDest(String dest) {
        this.dest = dest;
    }

    public List<Map> getPort() {
        return port;
    }

    public void setPort(List<Map> prt) {
        this.port = prt;
    }
}
