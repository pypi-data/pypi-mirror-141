# flavortext.py
I shamelessly yoinked this from [ZachFreedman's Singularitron](https://github.com/ZackFreedman/Singularitron) project, and rewrote it in Python.

sue me.

## How to use:
import the module:
`from flavortext import flavoricious`



flavoricious can take 6 arguments:

`yourConstrVerbs`: A list, verbs that are constructive such as 'Building' or 'Assembling'.  
`yourDestrVerbs`: A list, verbs that are destructive such as 'Destroying' or 'Breaking'.  
*Note for both of these args: Make sure to remove any sort of ending like 'ing' from the words you provide.*  
`yourNouns`: A list of... nouns. Seems pretty obvious, actually.  
`length`: An int, how many phrases should be generated. Defaults to 25.  
`delay`: A float, the delay between phrases being printed in seconds. Defaults to 0.05.  