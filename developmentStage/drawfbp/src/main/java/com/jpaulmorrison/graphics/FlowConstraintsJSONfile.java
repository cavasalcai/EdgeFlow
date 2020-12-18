package com.jpaulmorrison.graphics;

import java.util.Map;
import java.util.List;

public class FlowConstraintsJSONfile {

    private Map<String, List<FlowConstraintsInputFile>> constraints;

    public Map<String, List<FlowConstraintsInputFile>> getFlows() {
        return constraints;
    }

    public void setFlows(Map<String, List<FlowConstraintsInputFile>> flows) {
        this.constraints = flows;
    }
}
