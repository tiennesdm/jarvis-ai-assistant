"""File management operations for Jarvis AI."""
import os
import shutil
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)


class FileManager:
    """Manages file system operations."""

    def list_directory(self, path: str = ".") -> List[str]:
        """List files in directory."""
        try:
            items = os.listdir(os.path.expanduser(path))
            return sorted(items)
        except Exception as e:
            logger.error(f"Cannot list {path}: {e}")
            return []

    def create_folder(self, path: str) -> bool:
        """Create new folder."""
        try:
            os.makedirs(os.path.expanduser(path), exist_ok=True)
            logger.info(f"Created folder: {path}")
            return True
        except Exception as e:
            logger.error(f"Cannot create {path}: {e}")
            return False

    def delete_file(self, path: str) -> bool:
        """Delete file (moves to trash if possible)."""
        try:
            full_path = os.path.expanduser(path)
            if os.path.isdir(full_path):
                shutil.rmtree(full_path)
            else:
                # Try to move to trash first
                try:
                    from send2trash import send2trash
                    send2trash(full_path)
                except ImportError:
                    os.remove(full_path)
            logger.info(f"Deleted: {path}")
            return True
        except Exception as e:
            logger.error(f"Cannot delete {path}: {e}")
            return False

    def move_file(self, src: str, dst: str) -> bool:
        """Move file from src to dst."""
        try:
            shutil.move(os.path.expanduser(src), os.path.expanduser(dst))
            logger.info(f"Moved {src} to {dst}")
            return True
        except Exception as e:
            logger.error(f"Cannot move: {e}")
            return False

    def copy_file(self, src: str, dst: str) -> bool:
        """Copy file from src to dst."""
        try:
            shutil.copy2(os.path.expanduser(src), os.path.expanduser(dst))
            logger.info(f"Copied {src} to {dst}")
            return True
        except Exception as e:
            logger.error(f"Cannot copy: {e}")
            return False

    def get_file_info(self, path: str) -> dict:
        """Get file information."""
        try:
            full_path = os.path.expanduser(path)
            stat = os.stat(full_path)
            return {
                "name": os.path.basename(path),
                "size": stat.st_size,
                "modified": stat.st_mtime,
                "is_file": os.path.isfile(full_path),
                "is_dir": os.path.isdir(full_path),
                "path": full_path
            }
        except Exception as e:
            logger.error(f"Cannot get info for {path}: {e}")
            return {}

    def search_files(self, query: str, directory: str = "~") -> List[str]:
        """Search for files matching query."""
        matches = []
        search_dir = os.path.expanduser(directory)

        try:
            for root, dirs, files in os.walk(search_dir):
                for name in files + dirs:
                    if query.lower() in name.lower():
                        matches.append(os.path.join(root, name))
                # Limit depth for performance
                if root.count(os.sep) > search_dir.count(os.sep) + 3:
                    break
        except Exception as e:
            logger.error(f"Search error: {e}")

        return matches[:20]  # Limit results
