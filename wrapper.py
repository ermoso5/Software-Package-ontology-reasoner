__author__ = 'Manuel'
from packageParser import PackageParser
from subprocess import call

swipl_loc = ""
prolog_file = ""
base_ontology = ""
packageFile = ""
version = ""
output = ""
ontology_loc = ""

def setSwipl():
    global swipl_loc
    global prolog_file
    global base_ontology
    global packageFile
    global version
    global output
    global ontology_loc
    print("Current paths are:")
    print("swipl_loc (Prolog executable): "+swipl_loc)
    print("prolog_file (Prolog reasoner script): "+prolog_file)
    print("base_ontology (Ontology skeleton): "+base_ontology)
    print("packageFile (Package descriptions): "+packageFile)
    print("version (Package file is stable/testing/unstable): "+version)
    print("output (Output ontology): "+output)
    print("ontology_loc (Output ontology absolute path in prolog syntax): "+ontology_loc)

    while True:
        i = input("Type the name of the variable you want to change or type 'q' to go back to the menu: ").strip()
        if i == "swipl_loc":
            swipl_loc = str(input("Type the path: ").strip())
            print("Variable changed.")
            break
        elif i == "prolog_file":
            prolog_file = str(input("Type the path: ").strip())
            print("Variable changed.")
            break
        elif i == "base_ontology":
            base_ontology = str(input("Type the path: ").strip())
            print("Variable changed.")
            break
        elif i == "packageFile":
            packageFile = str(input("Type the path: ").strip())
            print("Variable changed.")
            break
        elif i == "version":
            version = str(input("Type the version for the package input file: ").strip())
            print("Variable changed.")
            break
        elif i == "output":
            output = str(input("Type the path: ").strip())
            print("Variable changed.")
            break
        elif i == "ontology_loc":
            ontology_loc = str(input("Type the path: ").strip())
            print("Variable changed.")
            break
        elif i == "q":
            print("Returning to menu.")
            break
        else:
            print("No valid variable has been given.")


def loadSwipl():
    global swipl_loc
    global prolog_file
    global base_ontology
    global packageFile
    global version
    global output
    global ontology_loc

    try:
        with open("config.conf") as f:
            content = f.readline()
            swipl_loc = content.strip().split("=")[1]

            content = f.readline()
            prolog_file = content.strip().split("=")[1]

            content = f.readline()
            base_ontology = content.strip().split("=")[1]

            content = f.readline()
            packageFile = content.strip().split("=")[1]

            content = f.readline()
            version = content.strip().split("=")[1]

            content = f.readline()
            output = content.strip().split("=")[1]

            content = f.readline()
            ontology_loc = content.strip().split("=")[1]
    except Exception as e:
        pass


def parse():
    global packageFile
    global output
    global base_ontology
    global version
    try:
        PackageParser(packageFile, output, base_ontology, version).Parse()
    except Exception as e:
        print("An error has occured while parsing. Please verify the paths. "+str(e))


def reason():
    x = str(input("Obtain information about package: ")).strip()
    package = '\'' + x + '\''

    try:
        call([swipl_loc, "--quiet", "-t", "load("+ontology_loc+"), info("+package+")", prolog_file])
    except Exception as e:
        print("Cannot execute reasoner, arguments are incorrect. Please verify the paths. "+str(e))
    print("\n")


def print_all():
    try:
        call([swipl_loc, "--quiet", "-t", "load("+ontology_loc+"), printall", prolog_file])
    except Exception as e:
        print("Cannot execute reasoner, arguments are incorrect. Please verify the paths. "+str(e))
    print("\n")


def main():
    loadSwipl()
    print("\n================================================")
    print("Welcome to the Software Package ontology reasoner.\n")
    loop = True

    while(loop):
        print("Select an action to perform:")
        print("1. Change paths for SWIPL and other files.")
        print("2. Parse package file into ontology.")
        print("3. Perform reasoning on the ontology.")
        print("4. Print all the packages in the ontology and their dependencies.")
        print("5. Quit\n")

        typeCheck = True
        while typeCheck:
            try:
                typed_str = int(input("Enter a command number: ").strip())
            except ValueError:
                print("Invalid option. Try again.")
                continue

            if typed_str is 1:
                typeCheck = False
                setSwipl()
                pass
            elif typed_str is 2:
                typeCheck = False
                parse()
                pass
            elif typed_str is 3:
                typeCheck = False
                reason()
                pass
            elif typed_str is 4:
                typeCheck = False
                print_all()
            elif typed_str is 5:
                typeCheck = False
                print("Quitting program.")
                loop = False
            else:
                print("Invalid option. Try again.")
        print("\n================================================")

if __name__ == "__main__":
    main()