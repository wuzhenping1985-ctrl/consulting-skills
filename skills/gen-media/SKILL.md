---
name: gen-media
description: Generate AI images, videos, music, and audio with the Generative Media Skills repository and MuAPI. Use when the user asks for Gen Media, generative media, AI image generation, AI video generation, image-to-video, text-to-video, music generation, media upload, or MuAPI-powered media workflows.
---

# Gen Media

Use this local wrapper as the entry point for the Generative Media Skills repository.

Before running a media generation task, read `core/media/SKILL.md` in this skill folder. Resolve all paths relative to this repository root. The shared model schema is `schema_data.json`, and the core scripts live in `core/media/`.

Common script paths:

- `core/media/generate-image.sh`
- `core/media/generate-video.sh`
- `core/media/image-to-video.sh`
- `core/media/create-music.sh`
- `core/media/upload.sh`

For expert workflows, inspect the matching folder under `library/` after reading the core media instructions.
