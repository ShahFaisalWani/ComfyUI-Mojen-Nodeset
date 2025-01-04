from .log_percent import LogPercentNode, StringLengthNode
from .tag_processor import TagProcessorNode
from .extract_style import StyleExtractorNode
from .analyze_processor import AnalyzeProcessorNode
from .nsfw_classifier import NSFWClassifierNode, NSFWClassifierSaveNode
from .image_loader import ImageLoader
from .aspect_ratio import AspectRatioNode

NODE_CLASS_MAPPINGS = {
  "MojenLogPercent": LogPercentNode,
  "MojenStringLength": StringLengthNode,
  "MojenTagProcessor": TagProcessorNode,
  "MojenStyleExtractor": StyleExtractorNode,
  "MojenAnalyzeProcessor": AnalyzeProcessorNode,
  "MojenNSFWClassifier": NSFWClassifierNode,
  "MojenNSFWClassifierSave": NSFWClassifierSaveNode,
  "MojenImageLoader": ImageLoader,
  "MojenAspectRatio": AspectRatioNode,
}

__all__ = ['NODE_CLASS_MAPPINGS']
