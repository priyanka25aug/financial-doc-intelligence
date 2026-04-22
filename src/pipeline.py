"""End-to-end pipeline: classify → extract → interpret → output with confidence."""
from .classifier import DocumentClassifier
from .extractor import EntityExtractor
from .interpreter import DocumentInterpreter
from .schemas import PipelineOutput


class FinancialDocPipeline:
    def __init__(self):
        self.classifier = DocumentClassifier()
        self.extractor = EntityExtractor()
        self.interpreter = DocumentInterpreter()

    def process(self, text: str) -> PipelineOutput:
        classification = self.classifier.classify(text)
        extraction = self.extractor.extract(text, classification.doc_type)
        interpretation = self.interpreter.interpret(text, classification, extraction)

        return PipelineOutput(
            classification=classification,
            extraction=extraction,
            interpretation=interpretation,
            text_preview=text[:200].strip(),
        )
