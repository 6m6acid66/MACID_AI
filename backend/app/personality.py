from pathlib import Path

from .config import SYSTEM_PROMPT_PATH


def load_personality():
    prompt_path = Path(SYSTEM_PROMPT_PATH)

    if not prompt_path.exists():
        raise FileNotFoundError(
            f"Personality file not found: {prompt_path}"
        )

    return prompt_path.read_text(encoding="utf-8").strip()
