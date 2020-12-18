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

package com.jpaulmorrison.fbp.core.components.text;


import com.jpaulmorrison.fbp.core.engine.Component;
import com.jpaulmorrison.fbp.core.engine.ComponentDescription;
import com.jpaulmorrison.fbp.core.engine.InPort;
import com.jpaulmorrison.fbp.core.engine.InPorts;
import com.jpaulmorrison.fbp.core.engine.InputPort;
import com.jpaulmorrison.fbp.core.engine.OutPort;
import com.jpaulmorrison.fbp.core.engine.OutPorts;
import com.jpaulmorrison.fbp.core.engine.OutputPort;
import com.jpaulmorrison.fbp.core.engine.Packet;


/**
 * Provide measured lines from a stream of words - essentially same as routing.ReCompose
 * Bob Corrick December 2011
 */
@ComponentDescription("Take words IN and deliver OUT a line no longer than MEASURE characters")
@OutPorts({ @OutPort(value = "OUT") })
@InPorts({ @InPort("IN"), @InPort("MEASURE") })
public class WordsToLine extends Component {
  

  private InputPort inport;

  InputPort mport;

  private OutputPort outport;

  @Override
  protected void execute() {
    // Get measure
    Packet pMeas = mport.receive();
    if (pMeas == null) {
      return;
    }
    mport.close();
    String sMeasure = ((String) pMeas.getContent()).trim();
    drop(pMeas);

    // Interpret measure
    int measure = 0;
    try {
      measure = Integer.parseInt(sMeasure);
    } catch (NumberFormatException e) {
      System.err.println("Value " + sMeasure + " cannot be interpreted as a number");
      e.printStackTrace();
    }

    String line = "";
    Packet pIn;
    while ((pIn = inport.receive()) != null) {
      String w = ((String) pIn.getContent()).trim();
      drop(pIn);

      if (line.length() + 1 + w.length() > measure) {
        Packet pOut = create(line);
        outport.send(pOut);
        line = w;
      } else {
        if (line.length() > 0) {
          line += " ";
        }
        line += w;
      }
    }
    if (line.length() > 0) {
      Packet pEnd = create(line);
      outport.send(pEnd);
    }
  }

  @Override
  protected void openPorts() {
    inport = openInput("IN");
    mport = openInput("MEASURE");
    outport = openOutput("OUT");
  }
}
