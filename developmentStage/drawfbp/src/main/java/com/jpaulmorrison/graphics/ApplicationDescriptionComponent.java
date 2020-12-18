package com.jpaulmorrison.graphics;

import java.util.Map;
import java.util.List;

public class ApplicationDescriptionComponent {

    private String id;
    private String RAM;
    private String CPU;
    private String HDD;
    private List<Map<String, String>> WCET;
    private List<Map<String, List<Map<String, Map<String, String>>>>> ports;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getRAM() {
        return RAM;
    }

    public void setRAM(String RAM) {
        this.RAM = RAM;
    }

    public String getCPU() {
        return CPU;
    }

    public void setCPU(String CPU) {
        this.CPU = CPU;
    }

    public String getHDD() {
        return HDD;
    }

    public void setHDD(String HDD) {
        this.HDD = HDD;
    }

    public List<Map<String, String>> getWCET() {
        return WCET;
    }

    public void setWCET(List<Map<String, String>> WCET) {
        this.WCET = WCET;
    }

    public List<Map<String, List<Map<String, Map<String, String>>>>> getPorts() {
        return ports;
    }

    public void setPorts(List<Map<String, List<Map<String, Map<String, String>>>>> ports) {
        this.ports = ports;
    }
}
