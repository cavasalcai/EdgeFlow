# EdgeFlow
EdgeFlow is a methodology for latency-sensitive IoT applications development and deployment, composed of two different stages:
* The development stage.
* The deployment and validation stage.

At design time, the application developer can use the development stage to model the application and provide specific resource and timing requirements. In the end, the developer generates the application model and all its requirements into two JSON files, i.e., (i) the application model file and (ii) the flow constraints file. Furthermore, the developer must prepare the edge computing platform file. With the three files ready, the developer employs the deployment stage to validate and find an optimal or feasible deployment strategy.

## Development Stage

To prove the benefits of creating a new latency-sensitive application using EdgeFlow, we develop an application development prototype as an extension to <a href="https://github.com/jpaulm/drawfbp">drawFBP</a>. DrawFBP uses Flow-Based Programming (FBP) at its core and allows developers to create application models using blocks, i.e., components.

### Instructions

The developer can use our application development prototype to create new latency-sensitive applications by defining timing and resource requirements and connect multiple components. FBP is not a coding language; therefore, the ideal development process would be to use predefined components from a library. If needed, the application developer can develop new components in another programming language.

Specifically, with our DrawFBP extension, the developer can add different applications' requirements like:
* Component resource requirements, i.e., RAM, CPU, HDD, Period, and output data size.
* Timing requirements, i.e., components' worst-case execution time (WCET), the worst-case communication delay (WCCD), and the e2e delay for different communication flows.

For further instruction on how to install and use drafFBP as well as adding the example in javaFBP, please visit the GitHub where the initial drawFBP is placed, i.e., <a href="https://github.com/jpaulm/drawfbp">drawFBP</a>.

## Deployment and Validation Stage

The deployment and validation stage aids the developer in defining the application's timing and resource requirements and provide a deployment strategy that satisfies the application requirements. The deployment technique is developed and tested in Python 3.7 and requires Google OR-Tools to be installed.

### Instructions

* Be sure to have the three input files required by the development stage.
* Executing *deployment.py* will start the deployment stage.
* Check the options supported by our deployment technique by execution: <code>python3 deployment.py -h</code>
* For example, to find a deployment strategy you could execute the following: <code>python3 deployment.py -a "application_model_inputfile" -e "edge_platform_inputfile" -f "flow_constraints_inputfile" -o -r "results_outputfile"</code>
