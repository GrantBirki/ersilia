from ersilia.utils.exceptions.throw_ersilia_exception import throw_exception
from .. import ErsiliaBase
from ..lake.manager import IsauraManager


class LakeStorer(ErsiliaBase):
    def __init__(self, model_id, config_json, credentials_json):
        ErsiliaBase.__init__(
            self, config_json=config_json, credentials_json=credentials_json
        )
        self.model_id = model_id
        self.isaura_manager = IsauraManager(
            model_id=model_id,
            config_json=config_json,
            credentials_json=credentials_json,
        )

    def store(self):
        try:
            self.logger.debug("Appeding local to public")
            self.isaura_manager.append_local_to_public()
            self.logger.debug("Pushing")
            self.isaura_manager.push()
            
        except Exception as E:
            throw_exception(E)
