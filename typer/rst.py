import docutils.frontend
import docutils.nodes
import docutils.parsers.rst
import docutils.utils


def parse(text: str) -> docutils.nodes.document:
    parser = docutils.parsers.rst.Parser()
    settings = docutils.frontend.OptionParser(
        components=(docutils.parsers.rst.Parser,)
    ).get_default_values()
    document = docutils.utils.new_document("<rst-doc>", settings=settings)
    parser.parse(text, document)
    return document
