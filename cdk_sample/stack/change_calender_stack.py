from aws_cdk import Stack
from constructs import Construct

from cdk_sample.construct.change_calender import ChangeCalender


class ChangeCalenderStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        content = "BEGIN:VCALENDAR\r\nPRODID:-//AWS//Change Calendar 1.0//EN\r\nVERSION:2.0\r\nX-CALENDAR-TYPE:DEFAULT_CLOSED\r\nX-WR-CALDESC:詳細\r\nBEGIN:VTODO\r\nDTSTAMP:20200320T004207Z\r\nUID:3b5af39a-d0b3-4049-a839-d7bb8af01f92\r\nSUMMARY:Add events to this calendar.\r\nEND:VTODO\r\nEND:VCALENDAR\r\n"
        ChangeCalender(self, "Sample", content=content)
