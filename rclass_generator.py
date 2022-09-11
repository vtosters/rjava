# R.java class generator by public.xml
import argparse, sys, re
from typing import List

TABULATION = " " * 4

class AndroidResource:
    name: str
    id: str

    def __init__(self, name: str, id: str):
        self.name = name
        self.id = id

    def build_line(self) -> str:
        return TABULATION * 2 + "public static final int {0} = {1};".format(self.name, self.id)

class Node:
    name: str
    resources: List[AndroidResource]

    def __init__(
            self,
            name: str,
    ):
        self.name = name
        self.resources = list()

    def build_lines(self, add_comments) -> list[str]:
        lst = list()
        lst.append(TABULATION + "public static final class {0} {{".format(self.name))
        for resource in self.resources:
            line = resource.build_line()
            if add_comments:
                line += " // " + str(int(resource.id, 16))
            lst.append(line)
        lst.append(TABULATION + "}")
        return lst

NODES: list[Node] = list()

def find_node(name):
    for node in NODES:
        if name == node.name:
            return node

def generate_rclass(package_name, add_comments):
    with open("R.java", "w") as f:
        if package_name:
            f.write("package {0};\n\n".format(package_name))
        f.write("public class R {")
        for node in NODES:
            f.write("\n")
            for line in node.build_lines(add_comments):
                f.write(line + "\n")
        f.write("}")

def parse_resources(pathname):
    with open(pathname, "r") as f:
        for line in f.readlines()[2:-1]:
            name = re.search("name=\"(.+?)\"", line).group(1).replace(".", "_")
            id = re.search("id=\"(.+?)\"", line).group(1)
            type = re.search("type=\"(.+?)\"", line).group(1)
            node = find_node(type)
            if not node:
                node = Node(type)
                NODES.append(node)
            node.resources.append(AndroidResource(name, id))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Pathname of public.xml")
    parser.add_argument("-p", "--package", help="Package of generated class")
    parser.add_argument("-c", "--comments", action="store_true", help="Add comments with decimal resource ids")
    args = parser.parse_args()
    print(args)
    if not args.file:
        print("null pathname", file=sys.stderr)
        exit(-1)
    parse_resources(args.file)
    generate_rclass(args.package, args.comments)