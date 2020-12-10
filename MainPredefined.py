from Core.Initializer import *


if __name__ == "__main__":
    init = Initializer()
    init.build("input/template.xml", "output/mypdf.pdf", "input/template.properties", Signature.AUTO_DATE)
    print("\n" + "--------------------------------------DONE--------------------------------------")
