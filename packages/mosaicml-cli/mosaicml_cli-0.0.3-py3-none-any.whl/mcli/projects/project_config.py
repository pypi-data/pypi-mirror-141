""" The ProjectConfig for storing ProjectModels Locally """
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from io import StringIO
from pathlib import Path

from ruamel.yaml import YAML

from mcli import config
from mcli.api.projects.update_project import update_project
from mcli.models.project import ProjectModel
from mcli.utils.utils_date import time_since
from mcli.utils.utils_file import create_symlink, delete_file_if_exists


@dataclass
class ProjectConfig(ProjectModel):
    """
    The ProjectConfig is a wrapper object around a ProjectMdoel object (GraphQL)
    that helps coordinate local files
    """

    @classmethod
    def load(cls, path: Path) -> ProjectConfig:
        y = YAML()

        with open(path.absolute(), 'r', encoding='utf8') as f:
            data = y.load(f)
            data['last_update_time'] = datetime.fromisoformat(data['last_update_time'])
            data['creation_time'] = datetime.fromisoformat(data['creation_time'])
        return cls(**data)

    def dump(self, path: Path) -> None:

        data = asdict(self)
        data['last_update_time'] = data['last_update_time'].isoformat()
        data['creation_time'] = data['creation_time'].isoformat()

        y = YAML()
        y.explicit_start = True  # type: ignore

        with open(path.absolute(), 'w', encoding='utf8') as f:
            y.dump(data, f)

    @property
    def file_path(self) -> Path:
        return config.DEFAULT_PROJECTS_DIR / f'{ self.project }.yaml'

    def save(self) -> bool:
        """Saves the ProjectConfig to local disk and updates it in FeatureDB

        Return:
            Returns true if successful
        """
        self.last_update_time = datetime.now()
        if config.feature_enabled(config.FeatureFlag.USE_FEATUREDB):
            success = update_project(self)
            if not success:
                print('Failed to update project in FeatureDB')
                return False
        self.dump(self.file_path)
        return True

    def __str__(self) -> str:
        y = YAML()
        stream = StringIO()
        data = asdict(self)
        if 'new_project_name' in data:
            del data['new_project_name']
        y.dump(data, stream=stream)
        output = stream.getvalue()
        stream.close()
        return output

    def set_current_project(self) -> None:
        self.last_update_time = datetime.now()
        self.save()
        delete_file_if_exists(path=config.DEFAULT_CURRENT_PROJECT_SYMLINK_PATH)
        create_symlink(
            from_path=config.DEFAULT_CURRENT_PROJECT_SYMLINK_PATH,
            to_path=self.file_path,
        )

    def __lt__(self, other: ProjectConfig) -> bool:
        return self.last_update_time < other.last_update_time

    def __eq__(self, other: ProjectConfig) -> bool:
        # Only uses project names because names are unique
        return self.project == other.project

    def get_last_accessed_string(self) -> str:
        return time_since(self.last_update_time)
