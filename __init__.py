from .log_percent import StringLengthNode
from .tag_processor import TagProcessorNode
from .extract_style import StyleExtractorNode
from .analyze_processor import AnalyzeProcessorNode
from .nsfw_classifier import NSFWClassifierNode, NSFWClassifierSaveNode
from .image_loader import ImageLoader
from .aspect_ratio import AspectRatioNode
from .transparent_bg import TransparentBgNode

NODE_CLASS_MAPPINGS = {
  "MojenStringLength": StringLengthNode,
  "MojenTagProcessor": TagProcessorNode,
  "MojenStyleExtractor": StyleExtractorNode,
  "MojenAnalyzeProcessor": AnalyzeProcessorNode,
  "MojenNSFWClassifier": NSFWClassifierNode,
  "MojenNSFWClassifierSave": NSFWClassifierSaveNode,
  "MojenImageLoader": ImageLoader,
  "MojenAspectRatio": AspectRatioNode,
  "MojenTransparentBg": TransparentBgNode,
}

__all__ = ['NODE_CLASS_MAPPINGS']
