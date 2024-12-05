from .log_percent import LogPercentNode
from .tag_processor import TagProcessorNode
from .extract_style import StyleExtractorNode
from .analyze_processor import AnalyzeProcessorNode

NODE_CLASS_MAPPINGS = {
  "MojenLogPercent": LogPercentNode,
  "MojenTagProcessor": TagProcessorNode,
  "MojenStyleExtractor": StyleExtractorNode,
  "MojenAnalyzeProcessor": AnalyzeProcessorNode,
}

__all__ = ['NODE_CLASS_MAPPINGS']
