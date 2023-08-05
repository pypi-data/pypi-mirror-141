# Wagtail-Audio-Embed

Wagtail-Audio-Embed allows you to use links to sound files using the embed
feature of the draftail editor.

It uses the default audio tag to play the audio file:

![Rendering in Firefox](https://github.com/peterjochum/wagtail-audio-embed/raw/main/img/screenshot.png)

See [Wagtail-Audio-Embed on PyPi](https://pypi.org/project/wagtail-audio-embed/0.1.1/)
for binaries and additional information.

## Quick start

Install using pip:

```bash
pip install wagtail-audio-embed
```

Add "wagtailaudioembed" to your INSTALLED_APPS setting:

```python
INSTALLED_APPS = [
    ...
    'wagtailaudioembed',
]
```

Register the embed finder class in your settings

```python
WAGTAILEMBEDS_FINDERS = [
    {
        "class": "wagtailaudioembed.embed.AudioEmbedFinder",
    }
]
```

Restart your application and start embedding links to Vorbis files.

## References

- [Advanced tutorial: How to write reusable apps](https://docs.djangoproject.com/en/4.0/intro/reusable-apps/)
- [Wagtail docs - Embedded content](https://docs.wagtail.org/en/stable/advanced_topics/embeds.html)
- [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [Mozilla Developer Network : The Embed Audio element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/audio)
