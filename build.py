# coding: UTF-8
import jinja2
import os


class TemplateRender:
    __instance = None

    def __new__(cls, path):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls._engine = jinja2.Environment(loader=jinja2.FileSystemLoader(path))

        return cls.__instance

    def render(self, template, *args, **kwargs):
        template = self._engine.get_template(template)
        return template.render(*args, **kwargs)


def getFiles(dir):
    files = []
    for file in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, file)) and file.endswith("html"):
            files.append(file)
    return files

def getDirs(dir):
    dirs = []
    for file in os.listdir(dir):
        if not os.path.isfile(os.path.join(dir, file)):
            dirs.append(file)
    return dirs

def main():
    path = "./view"

    render = TemplateRender(path=path)

    for file in getFiles(path):
        print("Build: `%s`." % os.path.join(path, file).replace("\\", "/"))
        data = render.render(file)

        with open(file, "w", encoding="UTF-8") as fd:
            fd.write(data)


    for dir in getDirs(path):
        if dir != "layout":
            for file in getFiles(os.path.join(path, dir)):
                print("Build: `%s`." % os.path.join(path, dir, file).replace("\\", "/"))
                data = render.render(os.path.join(dir, file).replace("\\", "/"))

                with open(os.path.join(dir, file), "w", encoding="UTF-8") as fd:
                    fd.write(data)

if __name__ == "__main__":
    main()
