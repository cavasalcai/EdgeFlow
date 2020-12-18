package com.jpaulmorrison.fbp.core.components.edgeflow;

import com.jpaulmorrison.fbp.core.engine.*;

/** A mock up component for Send Alarm functionality. This component is part of the Public Safety application used
 *  to demonstrate the EdgeFlow methodology.
 */
@ComponentDescription("A mock up for the component c4: Send Alarm")
//@OutPort(value = "OUT",
//        description = "Generated results for c4")
@InPort(value = "IN", description = "Input from c2 and c3")

public class SendAlarm extends Component {


    //ToDo: add the real functionality here for your component!

    @Override
    protected void execute(){

    }

    @Override
    protected void openPorts() {

    }
}