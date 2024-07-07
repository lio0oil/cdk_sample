from aws_cdk import aws_ssm as ssm
from constructs import Construct


class ChangeCalender(Construct):
    @property
    def changecalender(self) -> ssm.CfnDocument:
        return self._changecalender

    def __init__(self, scope: Construct, id: str, *, content: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        self.__content = content

        self._CreateChangeCalendar()

    def _CreateChangeCalendar(self):
        content = self.__content

        # Content only accepts json. Therefore pass it empty and overwrite it later.
        doc: ssm.CfnDocument = ssm.CfnDocument(
            self,
            "ChangeCalendar",
            content={},
            document_type="ChangeCalendar",
            document_format="TEXT",
            name="ChangeCalendar",
            update_method="NewVersion",
        )
        doc.add_property_override("Content", content)

        self._changecalender = doc
