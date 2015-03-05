# ------------------------------------------------------------------------------
# Website Image Format
# ------------------------------------------------------------------------------
from wagtail.wagtailimages.formats import (Format,
                                           register_image_format,
                                           unregister_image_format)
from wagtail.wagtailimages.models import SourceImageIOError
from django.utils.html import escape

# Use our own format class which delegates to Rendition.img_tag
class WebFormat(Format):
    def image_to_html(self, image, alt_text, extra_attributes=''):
        try:
            rendition = image.get_rendition(self.filter_spec)
        except SourceImageIOError:
            # Image file is (probably) missing from /media/original_images
            return super().image_to_html(image, alt_text, extra_attributes)
        if self.classnames:
            if not hasattr(extra_attributes, '__setitem__'):
                extra_attributes = {}
            extra_attributes['class'] = escape(self.classnames)
        return rendition.img_tag(extra_attributes)

# Redefine the default image formats
unregister_image_format('fullwidth')
register_image_format(WebFormat('fullwidth', 'Full width',
                                'richtext-image full-width', 'width-800'))
unregister_image_format('left')
register_image_format(WebFormat('left', 'Left-aligned',
                                'richtext-image left', 'width-500'))
unregister_image_format('right')
register_image_format(WebFormat('right', 'Right-aligned',
                                'richtext-image right', 'width-500'))
