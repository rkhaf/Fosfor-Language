
class simbolTableClass:
    def __init__(self) -> None:
        self.scopeParent : simbolTableClass | None = None
        self.mappingVariabel : 