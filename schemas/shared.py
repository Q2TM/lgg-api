from fastapi import Path

ChannelQueryParam = Path(
    ..., ge=1, le=8, description="Channel must be between 1 and 8")
