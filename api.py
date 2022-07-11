# -*- coding: utf-8 -*-
"""
Created on Wed May  4 16:30:16 2022

@author: Lu, Max
"""

import os

from flask import Flask, request, jsonify, send_file, redirect
from flask_swagger_ui import get_swaggerui_blueprint

trans= '<http://linguistic.linkeddata.es/id/apertium/tranSetPT-GL/Ocidente_Occidente-np-pt-sense-Occidente_Ocidente-np-gl-sense-trans>'


# ---- init things ----
app = Flask(__name__)
swagger_ui = get_swaggerui_blueprint('/swagger', '/static/openapi.yaml')
app.register_blueprint(swagger_ui)

def main (trans, lex_entry_a='', lex_entry_b='', written_rep_a='', written_rep_b='', l1='', l2='', 
          AP_query_limit = 3, 
          BN_endpoint = "https://babelnet.org/sparql/", 
          AP_endpoint = "http://dbserver.acoli.cs.uni-frankfurt.de:5005/apertium/sparql", 
          BN_API = ''):
    
    #0. Imports
    import json
    import copy
    import sys
    
    from SPARQLWrapper import SPARQLWrapper, SPARQLWrapper2, JSON
    from SPARQLWrapper.Wrapper import QueryResult
    
    from rdflib import Namespace, Literal, Graph, URIRef
    from rdflib.namespace import RDF
    
    #1. Access APERTIUM RDF and extract data from it. 
    if lex_entry_a != '':
        sparql = SPARQLWrapper(AP_endpoint)
        sparql_query = """
        # Get all the direct translations belonging to a translation set:
        # source and target written representations along with all the 
        # intermediate elements and POS 
        
        PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        PREFIX tr: <http://www.w3.org/ns/lemon/vartrans#>
        PREFIX lime: <http://www.w3.org/ns/lemon/lime#>
        PREFIX lexinfo: <http://www.lexinfo.net/ontology/2.0/lexinfo#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT DISTINCT ?written_rep_a  ?sense_a ?sense_b  ?written_rep_b ?POS ?trans
        FROM <http://linguistic.linkeddata.es/id/apertium/>
        WHERE {
           
          #retrieve translation set
          ?trans_set tr:trans ?trans .
           
          #determine translation set
          ?trans_set lime:language '"""+l1+"""' ;
        			 lime:language '"""+l2+"""' .
        			 
          
          #retrieve source and target senses
          ?trans tr:source ?sense_a ;
        		 tr:target ?sense_b .
            
          #retrieve source lexical entry, form and written representation
          ?sense_a ontolex:isSenseOf  <"""+lex_entry_a+"""> .
          <"""+lex_entry_a+"""> ontolex:lexicalForm ?form_a .
          ?form_a ontolex:writtenRep ?written_rep_a .
          
          #retrieve target lexical entry, form and written representation
          ?sense_b ontolex:isSenseOf  <"""+lex_entry_b+"""> .
          <"""+lex_entry_b+"""> ontolex:lexicalForm ?form_b .
          ?form_b ontolex:writtenRep ?written_rep_b .
        
          #retrieve POS
          <"""+lex_entry_b+""">  lexinfo:partOfSpeech ?POS .
        } 
        LIMIT """+str(AP_query_limit)+"""
        """

        sparql.setQuery(sparql_query)
        sparql.setReturnFormat(JSON)
        AP_res = sparql.queryAndConvert()
        
        try:
            AP_res = AP_res['results']['bindings'][0]
        except:
            print('no results found in Apertium for this search')
            sys.exit(0)
        written_rep_a = AP_res['written_rep_a']['value']
        written_rep_b = AP_res['written_rep_b']['value']
        trans = AP_res['trans']['value']
    
    elif written_rep_a != '':
        sparql = SPARQLWrapper(AP_endpoint)
        sparql_query = """
        # Get all the direct translations belonging to a translation set:
        # source and target written representations along with all the 
        # intermediate elements and POS 

        PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        PREFIX tr: <http://www.w3.org/ns/lemon/vartrans#>
        PREFIX lime: <http://www.w3.org/ns/lemon/lime#>
        PREFIX lexinfo: <http://www.lexinfo.net/ontology/2.0/lexinfo#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT DISTINCT  ?sense_a ?sense_b ?lex_entry_a ?lex_entry_b ?POS ?trans
        FROM <http://linguistic.linkeddata.es/id/apertium/>
        WHERE {
           
          #retrieve translation set
          ?trans_set tr:trans ?trans .
           
          #determine translation set
          ?trans_set lime:language '"""+l1+"""' ;
        			 lime:language '"""+l2+"""' .
        			 
          
          #retrieve source and target senses
          ?trans tr:source ?sense_a ;
        		 tr:target ?sense_b .
            
          #retrieve source lexical entry, form and written representation
          ?sense_a ontolex:isSenseOf  ?lex_entry_a .
          ?lex_entry_a ontolex:lexicalForm ?form_a .
          ?form_a ontolex:writtenRep '"""+written_rep_a+"""'@"""+l1+""" .
          
          #retrieve target lexical entry, form and written representation
          ?sense_b ontolex:isSenseOf  ?lex_entry_b .
          ?lex_entry_b ontolex:lexicalForm ?form_b .
          ?form_b ontolex:writtenRep '"""+written_rep_b+"""'@"""+l2+""" .

          #retrieve POS
          ?lex_entry_b  lexinfo:partOfSpeech ?POS .
        } 
        LIMIT """+str(AP_query_limit)+"""
        """

        sparql.setQuery(sparql_query)
        sparql.setReturnFormat(JSON)
        AP_res = sparql.queryAndConvert()
        try:
            AP_res = AP_res['results']['bindings'][0]
        except:
            print('no results found in Apertium for this search')
            sys.exit(0)
        lex_entry_a = AP_res['lex_entry_a']['value']
        lex_entry_b = AP_res['lex_entry_b']['value']
        trans = AP_res['trans']['value']
        
    else:
        sparql = SPARQLWrapper(AP_endpoint)
        sparql.setQuery("""
        # Get all the direct translations belonging to a translation set:
        # source and target written representations along with all the 
        # intermediate elements and POS 

        PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        PREFIX tr: <http://www.w3.org/ns/lemon/vartrans#>
        PREFIX lime: <http://www.w3.org/ns/lemon/lime#>
        PREFIX lexinfo: <http://www.lexinfo.net/ontology/2.0/lexinfo#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT DISTINCT ?written_rep_a ?lex_entry_a ?sense_a ?sense_b ?lex_entry_b ?written_rep_b ?POS ?l1 ?l2
        FROM <http://linguistic.linkeddata.es/id/apertium/>
        WHERE {
           
          #retrieve translation set
          ?trans_set tr:trans <"""+ trans +"""> .
           
          #determine translation set
          ?trans_set lime:language ?l1 ;
        			 lime:language ?l2 .
        			 
          
          #retrieve source and target senses
          <"""+ trans +"""> tr:source ?sense_a ;
        		 tr:target ?sense_b .
            
          #retrieve source lexical entry, form and written representation
          ?sense_a ontolex:isSenseOf  ?lex_entry_a .
          ?lex_entry_a ontolex:lexicalForm ?form_a .
          ?form_a ontolex:writtenRep ?written_rep_a .
          
          #retrieve target lexical entry, form and written representation
          ?sense_b ontolex:isSenseOf  ?lex_entry_b .
          ?lex_entry_b ontolex:lexicalForm ?form_b .
          ?form_b ontolex:writtenRep ?written_rep_b .

          #retrieve POS
          ?lex_entry_b  lexinfo:partOfSpeech ?POS .
        } 
        LIMIT """+str(AP_query_limit)+"""
        """)
        sparql.setReturnFormat(JSON)
        AP_res = sparql.queryAndConvert()
        
        try:
            AP_res = AP_res['results']['bindings'][2]
        except:
            print('no results found in Apertium for this search')
            sys.exit(0)   
        lex_entry_a = AP_res['lex_entry_a']['value']
        lex_entry_b = AP_res['lex_entry_b']['value']
        written_rep_a = AP_res['written_rep_a']['value']
        written_rep_b = AP_res['written_rep_b']['value']
        l1 = AP_res['l1']['value']
        l2 = AP_res['l2']['value']
    
    #2. Access BabelNet RDF and extract the info related to the APERTIUM (#1) query results. 
    """ 
    BN info can be accessed in two different ways. 
    The first one uses BN SPARQL Endpoint. It is executed if BN_API is not provided. 
    The second one uses py_babelnet library and requires and API Key. The API
    Key can be obtained by former registration to BabelNet where one can ask
    for an increase on BabelNet queries per day 
    """
    
    pos = AP_res['POS']['value'] 
    
    if BN_API == '':

        def BN_query_1(written_rep_a, written_rep_b, l1, l2):
            #query trans in BN
            sparql = SPARQLWrapper(BN_endpoint)
            sparql.setReturnFormat('json')
            #extract all synsets shared by word_rep_a & word_rep_b (in this case: agua, water) plus their pos and semantic relationships
            sparql.setQuery("""
              SELECT ?synset
              WHERE {

                ?entries rdfs:label """"'"+ written_rep_a +"'@"+l1+""" .
                ?entries lemon:sense ?sense .
                ?sense lemon:reference ?synset .
                ?synset lemon:isReferenceOf ?sense2 .
                ?entry2 lemon:sense ?sense2 .
                ?entry2 rdfs:label """"'"+ written_rep_b +"'@"+l2+""" .
                ?entry2  lexinfo:partOfSpeech <"""+ pos +"""> 
                }
            """)
            return(QueryResult(sparql._query())._convertJSON())
        
        def get_synset_list (BN_res):
            #convert dic of BN synsets to list
            synset_list = []
            for i in BN_res['results']['bindings']:
              synset_list.append(i)
            return(synset_list)
        
        def link_dicts ():
            BN_res = BN_query_1(written_rep_a, written_rep_b, l1, l2) 
            #sparql query in BN to check for synsets that match both written_reps
            synset_list = get_synset_list(BN_res) 
            # return synsets as list
            BN_res['results']['bindings'] = synset_list  
            #add synset list to dict entry of the translation
            AP_BN_res = copy.deepcopy(AP_res)
            if len(BN_res['results']['bindings']) == 0:
                print('No babelnet links were found')
                return None
            
            synsets = []
            for i in BN_res['results']['bindings']:
                if i['synset']['value'] not in synsets:
                    synsets.append(i['synset']['value'])
            
            AP_BN_res['BN_reference'] = synsets
            return(AP_BN_res)
        
        AP_BN_res = link_dicts()
        
        
    else:
        
        from py_babelnet.calls import BabelnetAPI
        api = BabelnetAPI(BN_API)

        def BN_query_2(lang, written_rep):
            prov={}
            prov = copy.deepcopy(AP_res)
            #one search per language in translation set
            #modify written rep accordingly
            prov['BN_reference'] = api.get_senses(lemma = written_rep, searchLang = lang)
            return(prov)

        AP_l1 = BN_query_2(l1, written_rep_a)
        AP_l2 = BN_query_2(l2, written_rep_b)

        # +select only synsets with matching pos to apertium entry

        def clean_data(data):
            synsets=[]
            for sense in data['BN_reference']:      
                if sense['properties']['pos'] in pos.upper():
                    sense = sense['properties']['synsetID']['id']
                    #change BNid name to trace it in ontolgy(instead of bn:.., snnn)
                    sense = 's' + sense[3:]
                    sense = 'http://babelnet.org/rdf/' + sense
                    synsets.append(sense)
            data['BN_reference'] = synsets 
            return(data)

            
        def bind_dicts(dic1, dic2):
            common_BN_info = []
            for sense in dic1['BN_reference']:
                for sense1 in dic2['BN_reference']:
                    if sense == sense1:
                        if sense not in common_BN_info:
                            common_BN_info.append(sense1)
            dic1['BN_reference'] = common_BN_info
            return(dic1)

        dic1 = clean_data(AP_l1)
        dic2 = clean_data(AP_l2)
        AP_BN_res = bind_dicts(dic1, dic2)
        
    # 3. convert json dic to rdf

    #create graph
    g = Graph()

    base = 'http://linguistic.linkeddata.es/id/apertium/tranSet'+ l1.upper() + '-' + l2.upper() + '/'
    #PREFIXES
    BASE = Namespace(base)
    TR = Namespace('http://www.w3.org/ns/lemon/vartrans#')
    ONTOLEX = Namespace('http://www.w3.org/ns/lemon/ontolex#')
    BN = Namespace('http://babelnet.org/rdf/')
    LEXINFO = Namespace('http://www.lexinfo.net/ontology/3.0/lexinfo#')
    LIME = Namespace('http://www.w3.org/ns/lemon/lime#')


    #bind prefix to namespace
    g.bind('', BASE)
    g.bind('vartrans', TR)
    g.bind('ontolex', ONTOLEX)
    g.bind('babelnet', BN)
    g.bind('lexinfo', LEXINFO)
    g.bind('lime', LIME)

    #construct graph
    if AP_BN_res['BN_reference']!=[]: 
        for sense in AP_BN_res['BN_reference'][0]:
            #sense already existent in initial trans set for l1
            g.add((URIRef(AP_BN_res['sense_a']['value']), ONTOLEX.reference, URIRef(AP_BN_res['BN_reference'][0])))
            g.add((URIRef(AP_BN_res['sense_b']['value']), ONTOLEX.reference, URIRef(AP_BN_res['BN_reference'][0])))
        n=1
        for sense in AP_BN_res['BN_reference'][1:]:
            #create artifitial sense to express synset
            g.add((URIRef(base), TR.trans, (URIRef(trans +str(n)))))
            #new sense L1 associated to synset
            g.add(((URIRef(AP_BN_res['sense_a']['value']+str(n)), ONTOLEX.isSenseOf, URIRef(lex_entry_a))))
            g.add(((URIRef(AP_BN_res['sense_a']['value']+str(n)), ONTOLEX.reference, URIRef(sense))))
            #new sense L2 associated to synset
            g.add(((URIRef(AP_BN_res['sense_b']['value']+str(n)), ONTOLEX.isSenseOf, URIRef(lex_entry_b))))
            g.add(((URIRef(AP_BN_res['sense_b']['value']+str(n)), ONTOLEX.reference, URIRef(sense))))
            #relate new translation with new senses
            g.add((URIRef(trans+str(n)), TR.source, (URIRef(AP_BN_res['sense_a']['value']+str(n)))))
            g.add((URIRef(trans+str(n)), TR.target, (URIRef(AP_BN_res['sense_b']['value']+str(n)))))
            n+=1
    else:
        pass #if BN_info empty, i.e. no synset, no triples are created
        
    """6. download data"""

    AP_BN_RDF_results = g.serialize(format="turtle")
        
    return(AP_BN_RDF_results)

# ---- Endpoints ----

@app.route('/trans-to-bnet')
def enrich_rdf():
    val = main(request.values.get('trans', trans), request.values.get('lex_entry_a', ''),
         request.values.get('lex_entry_b', ''), 
         request.values.get('written_rep_a', ''), request.values.get('written_rep_b', ''),
         request.values.get('l1', ''), request.values.get('l2', ''), AP_query_limit = 3, 
         BN_endpoint = request.values.get('bnet-endpoint', "https://babelnet.org/sparql/"), 
         AP_endpoint = request.values.get('apertium-endpoint', "http://dbserver.acoli.cs.uni-frankfurt.de:5005/apertium/sparql"), 
         BN_API = request.values.get('bnet-api-key', ''))

    if not val:
        return '', 204
    return val

@app.route('/static/openapi.yaml')
def openapi_spec():
    return send_file('/bnet/openapi.yaml' if os.path.exists('/bnet/openapi.yaml') else 'openapi.yaml', cache_timeout=-1)
        

@app.route('/', methods=['GET'])
def index():
    return redirect('/swagger')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
