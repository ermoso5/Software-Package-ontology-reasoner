from xml.dom.minidom import Document
from xml.dom import minidom

class Package:
    def __init__(self): 
        self.package = ""
        self.version = ""
        self.description = ""
        self.distribution = ""
        self.section = ""
        self.architecture = ""
        self.maintainer = ""
        self.filename = ""
        self.type = "" #community manager; window manager; not community manager
        self.depends = []
        self.conflicts = []
        self.recommends = []
        self.suggests = []
        self.debianKeys = ['package', 'version', 'description', 'distribution', 'section', 'architecture', 'maintainer', 'filename']
        self.fedoraKeys = ['name', 'version', 'summary', 'distribution', 'group', 'architecture', 'maintainer', 'source0' ] #architecture & maintainer missing
        self.debianRelations = ['depends', 'conflicts', 'recommends', 'suggests']
        self.fedoraRelations = ['requires', 'conflicts', 'recommends', 'suggests'] # conflicts & recommends & suggests missing


class PackageParser:
    def __init__(self, filePath, outputFilePath, ontologyPath, version):
        self.filePath = filePath
        self.outputFile = outputFilePath
        self.ontologyPath = ontologyPath

        self.doc = Document()
        self.ID = "&Ontology1395738954259;"
        self.packages = open(self.filePath).read().split("\n\n")
        self.entities = []
        
        for p in range(0, len(self.packages)):
            props = self.packages[p].split("\n")
            package = Package()
            
            if props[0].startswith("Package"): #Debian
                keys = package.debianKeys
                relations = package.debianRelations
            else:
                keys = package.fedoraKeys
                relations = package.fedoraRelations
                
            for i in range(0, len(props)):
                pair = []
                if not ":" in props[i]:
                    continue

                pair.append(props[i].split(":", 1)[0])
                pair.append(props[i].split(":", 1)[1])

                propName = pair[0].lower()
                for key in range(0, len(keys)):
                    if propName.startswith(keys[key]):
                        setattr(package, package.debianKeys[key], pair[1].strip()) 
                        break
                    
                for key in range(0, len(relations)):
                    if propName.startswith(relations[key]):
                        setattr(package, package.debianRelations[key], getattr(package, package.debianRelations[key])+ list(map(self.resolveDependencies, pair[1].split(","))))
                        break
                    
                package.distribution = version    

            self.entities.append(package)
            

    def Parse(self):
        ontology = open(self.ontologyPath,'r')
        xmldoc = minidom.parse(ontology)
        rdf = xmldoc.getElementsByTagName("rdf:RDF")[0]
        
        for i in range(0, len(self.entities)):
            individual = self.createIndividual(self.entities[i])
            rdf.appendChild(individual)
        ontology.close()
        
        f = open(self.outputFile,'w')
        f.write(xmldoc.toxml().replace("&amp;", "&").replace("&gt;", ">").replace("&lt;", "<"))
        f.close() 

####### PRIVATE SECTION #########
    def resolveDependencies(self, element):
        return element.split("(")[0].strip().replace(" ", "").replace("|", "_")

    def createNode(self, nodename):  
        return self.doc.createElement(nodename)
    
    def createIndividual(self, package):
        output = ""
        ind = self.createNode("owl:NamedIndividual")
        ind.setAttribute("rdf:about", self.ID + package.package.replace("|", "_"))
        type = self.createNode("rdf:type")

        ##type##
        if "debian.org" in package.maintainer or ".deb" in package.filename:
            type.setAttribute("rdf:resource", self.ID+"Debian_package")
        else: #todo
            type.setAttribute("rdf:resource", self.ID+"Fedora_package")
        ind.appendChild(type)

        Type = self.createNode("PackageType")
        if package.distribution.count("@") == package.distribution.count("debian.org"):
            text = self.doc.createTextNode("Community manager")
        else:
            if "window" in package.package and "manager" in package.package:
                text = self.doc.createTextNode("Window manager")
            else:
                text = self.doc.createTextNode("Not community manager")

        Type.appendChild(text)
        ind.appendChild(Type)

        distr = self.createNode("Distribution")
        text = self.doc.createTextNode(package.distribution)
        distr.appendChild(text)
        ind.appendChild(distr)

        section = self.createNode("Section")
        text = self.doc.createTextNode(package.section)
        section.appendChild(text)
        ind.appendChild(section)

        architecture = self.createNode("Architecture")
        text = self.doc.createTextNode(package.architecture)
        architecture.appendChild(text)
        ind.appendChild(architecture)

        descr = self.createNode("Description")
        text = self.doc.createTextNode(package.description)
        descr.appendChild(text)
        ind.appendChild(descr)

        version = self.createNode("Version")
        text = self.doc.createTextNode(package.version)
        version.appendChild(text)
        ind.appendChild(version)
        
        for i in range(0, len(package.depends)):
            dep = self.createNode("depends")
            dep.setAttribute("rdf:resource", self.ID + package.depends[i])
            ind.appendChild(dep)

        for i in range(0, len(package.conflicts)):
            dep = self.createNode("conflicts")
            dep.setAttribute("rdf:resource", self.ID + package.conflicts[i])
            ind.appendChild(dep)

        for i in range(0, len(package.recommends)):
            dep = self.createNode("recommends")
            dep.setAttribute("rdf:resource", self.ID + package.recommends[i])
            ind.appendChild(dep)

        for i in range(0, len(package.suggests)):
            dep = self.createNode("suggests")
            dep.setAttribute("rdf:resource", self.ID + package.suggests[i])
            ind.appendChild(dep)

        return ind
    
## <owl:NamedIndividual rdf:about="&Ontology1395738954259;E">
##        <rdf:type rdf:resource="&Ontology1395738954259;Debian_Package"/>
##        <recommends rdf:resource="&Ontology1395738954259;C"/>
##        <depends rdf:resource="&Ontology1395738954259;F"/>
##        <conflicts rdf:resource="&Ontology1395738954259;J"/>
##    </owl:NamedIndividual>


