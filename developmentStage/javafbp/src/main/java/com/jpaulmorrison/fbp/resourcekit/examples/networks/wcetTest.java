package com.jpaulmorrison.fbp.resourcekit.examples.networks; //change package name if desired
import com.jpaulmorrison.fbp.core.engine.*; 
public class wcetTest extends Network {
String description = "Click anywhere on selection area";
protected void define() { 
  component("Read___Sample_File",com.jpaulmorrison.fbp.core.components.io.ReadFile.class,10); 
  component("filter_by_first_letter",com.jpaulmorrison.fbp.core.components.text.StartsWith.class,6); 
  component("display____accepted__lines",com.jpaulmorrison.fbp.core.components.swing.ShowText.class,1); 
  component("ignore",com.jpaulmorrison.fbp.core.components.routing.Discard.class,0); 
  connect(component("Read___Sample_File"), port("OUT"), component("filter_by_first_letter"), port("IN")); 
  connect(component("filter_by_first_letter"), port("ACC"), component("display____accepted__lines"), port("IN")); 
  connect(component("filter_by_first_letter"), port("REJ"), component("ignore"), port("IN")); 
  initialize("J", component("filter_by_first_letter"), port("TEST")); 
  initialize("input/text.txt", component("Read___Sample_File"), port("SOURCE")); 
  initialize("AcceptedEntries", component("display____accepted__lines"), port("TITLE")); 
} 
public static void main(String[] argv) throws Exception  { 
  new wcetTest().go(); 
} 
}
