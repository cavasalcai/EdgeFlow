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
 * 
 * ====================================================================================
 * 
 * Copied from http://www.java-tips.org/java-se-tips/java.lang/creating-application-specific-exceptions.html 
 * 
 * Thanks!
 */
 
package com.jpaulmorrison.fbp.core.engine;


public class ComponentException extends Exception {

  private int intError;

  public ComponentException(final int intErrNo) {
    intError = intErrNo;
  }

  public ComponentException(final String strMessage) {
    super(strMessage);
  }

  @Override
  public String toString() {
    return "Component exception - value: " + intError;
  }

  int getValue() {
    return intError;
  }
}
