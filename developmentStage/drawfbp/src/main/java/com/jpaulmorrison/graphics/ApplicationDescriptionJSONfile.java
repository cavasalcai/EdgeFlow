package com.jpaulmorrison.graphics;

import java.util.List;
import java.util.Map;

public class ApplicationDescriptionJSONfile {

    private Map<String, List<ApplicationDescriptionComponent>> application;

    public Map<String, List<ApplicationDescriptionComponent>> getApplication() {
        return application;
    }

    public void setApplication(Map<String, List<ApplicationDescriptionComponent>> application) {
        this.application = application;
    }
}
