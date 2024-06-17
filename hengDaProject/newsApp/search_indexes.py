from haystack import indexes
from .models import MyNew
import jieba
import re

class MyNewIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return MyNew

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

    def prepare(self, obj):
        data = super().prepare(obj)
        try:
            # 打印原始文本和分词后的文本
            segmented_text = self.segment_text(data['text'])
            print(f"Original text: {data['text']}")
            print(f"Segmented text: {segmented_text}")
            data['text'] = segmented_text
        except Exception as e:
            print(f"Error during segmentation: {e}")
        return data

    def segment_text(self, text):
        # 判断文本是否包含中文字符并进行分词
        if any('\u4e00' <= char <= '\u9fff' for char in text):
            # 对中文文本使用 jieba 分词
            return ' '.join(jieba.cut_for_search(text))
        else:
            # 对英文文本使用空格分词
            return text
