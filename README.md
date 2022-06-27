# Linking Apertium to BabelNet
This RestAPI is a tool to link lexical information from Apertium to lexical information from BabelNet.

Apertium RDF Graph contains 52 translations sets at the lexical entry level. Yet translations are better done at the sense level rather at the lexical entry level. To archieve this we provide this tool to link Apertium data to BabelNet, a resource which provides semantic information at the sense level of the words. 

A visual example of how this links between Apertium lexical entries to a BabelNet synset reference are created can be seen in the following image. When a translation between two lexical entries in two different languages exists (eg., ribera@es - bank@en), a translation identifier is created (bank-ribera). A sense is created to mediate between each lexical entry and the translation . Then this translation is linked to one or more synset references in BabelNet when both lexical entries in Apertium translation are found in BabelNet sharing a synset (eg., s00008363n):

<img width="677" alt="ExampleApertiumBNet_linking_bank" src="https://user-images.githubusercontent.com/79651222/175898594-e943ccb9-2f79-4aed-8361-acaec8ad5320.png">

Links can be done by starting from inputing either a translation set URI, two written representations from two different languages or two lexical entries from two different languages. 


Besides, BN info can be accessed in two different ways. The first one uses BN SPARQL Endpoint. It is executed if BN_API is not provided. The second one uses py_babelnet library and requires and API Key. The API Key can be obtained by former registration to BabelNet where one can ask for an increase on BabelNet queries per day 

