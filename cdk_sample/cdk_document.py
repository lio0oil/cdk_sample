from aws_cdk import aws_ssm as ssm
from constructs import Construct


class CdkDocument:
    def CreateChangeCalendar(self, scope: Construct):
        content = "BEGIN:VCALENDAR\r\nPRODID:-//AWS//Change Calendar 1.0//EN\r\nVERSION:2.0\r\nX-CALENDAR-TYPE:DEFAULT_CLOSED\r\nX-WR-CALDESC:詳細\r\nBEGIN:VTODO\r\nDTSTAMP:20200320T004207Z\r\nUID:3b5af39a-d0b3-4049-a839-d7bb8af01f92\r\nSUMMARY:Add events to this calendar.\r\nEND:VTODO\r\nEND:VCALENDAR\r\n"

        # Content only accepts json. Therefore pass it empty and overwrite it later.
        doc: ssm.CfnDocument = ssm.CfnDocument(
            scope,
            "ChangeCalendar",
            content={},
            document_type="ChangeCalendar",
            document_format="TEXT",
            name="ChangeCalendar",
            update_method="NewVersion",
        )
        doc.add_property_override("Content", content)
