# Wagtail audio embed

Wagtail-audio-embed allows you to use links to sound files using the embed
feature of the draftail editor.

It uses the default audio tag to play the audio file:
![Rendering in Firefox](img/screenshot.png)

## Quick start

Add "wagtailaudioembed" to your INSTALLED_APPS setting like this::

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

Restart your application and start embedding links to Vorbis files

## References

- [Advanced tutorial: How to write reusable apps](https://docs.djangoproject.com/en/4.0/intro/reusable-apps/)
- [Wagtail docs - Embedded content](https://docs.wagtail.org/en/stable/advanced_topics/embeds.html)
