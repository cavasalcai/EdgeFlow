/*
 * JavaFBP - A Java Implementation of Flow-Based Programming (FBP)
 * Copyright (C) 2009, 2016 J. Paul Morrison
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Library General Public
 * License as published by the Free Software Foundation; either
 * version 3.0 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
 *
 * You should have received a copy of the GNU Library General Public
 * License along with this library; if not, see the GNU Library General Public License v3
 * at https://www.gnu.org/licenses/lgpl-3.0.en.html for more details.
 */

package com.jpaulmorrison.fbp.core.components.routing;


import com.jpaulmorrison.fbp.core.engine.Component;
import com.jpaulmorrison.fbp.core.engine.ComponentDescription;
import com.jpaulmorrison.fbp.core.engine.InPort;
import com.jpaulmorrison.fbp.core.engine.InputPort;
import com.jpaulmorrison.fbp.core.engine.OutPort;
import com.jpaulmorrison.fbp.core.engine.OutputPort;
import com.jpaulmorrison.fbp.core.engine.Packet;


/** Sort a stream of up to 999999 Packets to an output stream
**/
@ComponentDescription("Sorts up to 999999 packets, based on contents")
@OutPort(value = "OUT", description = "Output port", type = String.class)
@InPort(value = "IN", description = "Packets to be sorted", type = String.class)
public class Sort extends Component {

  
  private InputPort inport;

  private OutputPort outport;

  @Override
  protected void execute() {

    Packet p;
    int i = 0, j, k, n;
    Packet[] array = new Packet[999999];
    while ((p = inport.receive()) != null) {
      array[i] = p;
      //System.out.println("in: " + p.getContent());
      ++i;
    }

    //network.traceFuncs(this.getName() + ": No. of elements:" + i);
    j = 0;
    k = i;
    n = k; // no. of packets to be sent out

    while (n > 0) {
      String t = "\uffff";

      for (i = 0; i < k; i++) {
        if (array[i] != null) {

          String s = (String) array[i].getContent();

          if (s.compareTo(t) < 0) {
            j = i;
            t = (String) array[j].getContent();
          }
        }
      }
      //  if (array[j] == null) break;
      outport.send(array[j]);
      array[j] = null;

      --n;
    }

  }

  @Override
  protected void openPorts() {

    inport = openInput("IN");

    outport = openOutput("OUT");

  }
}
