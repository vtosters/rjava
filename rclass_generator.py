# R.java class generator by public.xml
import argparse, sys, re
from typing import List

class AndroidResource:
    name: str
    id: str

    def __init__(self, name: str, id: str):
        self.name = name
        self.id = id

    def build_line(self) -> str:
        return "        public static final int {0} = {1};".format(self.name, self.id)

class Node:
    name: str
    resources: List[AndroidResource]

    def __init__(
            self,
            name: str,
    ):
        self.name = name
        self.resources = list()

    def build_lines(self) -> list[str]:
        lst = list()
        lst.append("    public static final class {0} {{".format(self.name))
        for resource in self.resources:
            lst.append(resource.build_line())
        lst.append("    }")
        return lst

nodes: list[Node] = list()

def find_node(name):
    for node in nodes:
        if name == node.name:
            return node

def generate_rclass(package_name):
    with open("R.java", "w") as f:
        if package_name:
            f.write("package {package};".format(package=package_name))
            f.write("\n\n")
        f.write("public class R {")
        for node in nodes:
            f.write("\n")
            for line in node.build_lines():
                f.write(line)
                f.write("\n")
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
                nodes.append(node)
            node.resources.append(AndroidResource(name, id))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", type=str, help="Pathname of public.xml")
    parser.add_argument("-p", type=str, help="Package of generated class")
    args = parser.parse_args()
    if not args.f:
        print("null pathname", file=sys.stderr)
        exit(-1)
    parse_resources(args.f)
    generate_rclass(args.p)