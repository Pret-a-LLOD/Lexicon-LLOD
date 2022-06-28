# Linking Apertium RDF to BabelNet

This RestAPI is a tool to link lexical information from Apertium RDF to conceptual information from BabelNet (https://babelnet.org/).

Apertium RDF Graph contains 52 translations sets at the lexical entry level. Yet translations are established between Lexical Senses in Apertium RDF, such senses lack ontology references. To associate such senses with conceptual information, we link them to BabelNet, a resource which provides semantic information at the sense level of the words ("babelsynsets"). We use lemon [ontolex](https://www.w3.org/2016/05/ontolex/#core) and [vartrans](https://www.w3.org/2016/05/ontolex/#variation-translation-vartrans) modules as representation means. 

A visual example of how these links between Apertium lexical entries and a BabelNet synset reference are created can be seen in the following image, where a translation between two lexical entries in two different languages exists in Apertium (eg., ribera@es - bank@en) through a translation (bank-ribera) and their intermediate lexical senses (senses 1 and sense 2). The senses are linked to one reference in BabelNet when both lexical entries (their written representations) are found in BabelNet sharing a synset (eg., s00008363n). (If more babelsynsets are found, new "artifcial" senses associated to the lexical entries are created and linked to them, along with their translations):

<img width="677" alt="ExampleApertiumBNet_linking_bank" src="https://user-images.githubusercontent.com/79651222/175898594-e943ccb9-2f79-4aed-8361-acaec8ad5320.png">

The input to this method is either a translation set URI, two written representations from two different languages or the URIs of two lexical entries from two different languages. 

Besides, BabelNet info can be accessed in two different ways. The first one uses BN SPARQL Endpoint (https://babelnet.org/sparql/). It is executed if BN_API is not provided. The second one uses py_babelnet library and requires and API Key. The API Key can be obtained by registering to BabelNet. Notices, though, that there is a limit in the number of queries to BabelNet that one can run per day. 

## License

Lexicon-LLOD was developed by the SID group (University of Zaragoza).

>    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

>    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

>    You should have received a copy of the GNU General Public License
    along with this program.  If not, see [http://www.gnu.org/licenses/].

