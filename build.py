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


def main():
    path = "./view"
    render = TemplateRender(path=path)

    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)) and file.endswith("html"):
            print("Build: `%s`." % file)
            data = render.render(file)

            with open(file, "w", encoding="UTF-8") as fd:
                fd.write(data)


if __name__ == "__main__":
    main()
