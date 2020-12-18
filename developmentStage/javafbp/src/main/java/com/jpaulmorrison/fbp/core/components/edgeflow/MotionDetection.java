package com.jpaulmorrison.fbp.core.components.edgeflow;

import com.jpaulmorrison.fbp.core.engine.*;


/** A mock up component for Motion Detection functionality. This component is part of the Public Safety application used
 *  to demonstrate the EdgeFlow methodology.
 */
@ComponentDescription("A mock up for the component c1: Motion Detection")
@OutPort(value = "OUT",
        description = "Generated results for c2 and c3")
@InPort(value = "IN", description = "Raw data from c0.")

public class MotionDetection extends Component {

    //ToDo: add the real functionality here for your component!

    @Override
    protected void execute(){

    }

    @Override
    protected void openPorts() {

    }

}
