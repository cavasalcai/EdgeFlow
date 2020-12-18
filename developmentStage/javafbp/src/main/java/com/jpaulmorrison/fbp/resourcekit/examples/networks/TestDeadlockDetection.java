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

package com.jpaulmorrison.fbp.resourcekit.examples.networks; 


import com.jpaulmorrison.fbp.core.engine.DispIPCounts;
import com.jpaulmorrison.fbp.core.components.misc.WriteToConsole;
import com.jpaulmorrison.fbp.core.engine.Network;
import com.jpaulmorrison.fbp.resourcekit.examples.components.GenerateSlowly;


/**
 *  This test should not report a deadlock - before Sven Steinseifer's changes to the
 * scheduler, it would have reported a spurious deadlock 
 */

public class TestDeadlockDetection {

  public static void main(final String[] args) {
    try {
      new Network() {

        @Override
        protected void define() {
          component("generate", GenerateSlowly.class);
          component("subD", SubnetD.class);
          component("DispCounts", DispIPCounts.class);

          connect("generate.OUT", "subD.IN", true);
          connect("subD.*", "DispCounts.CLSDN");
          initialize("500", component("DispCounts"), port("INTVL")); // DispIPCounts is SelfStarting
          connect("DispCounts.OUT", component("Display", WriteToConsole.class), port("IN"));

        }
      }.go();
    } catch (Exception e) {
      System.err.println("Exception trapped here");
      e.printStackTrace();
    }

  }

}
