from enum import Enum
from itertools import count
from typing import Optional

from requests import Response

from .methods import AddTLV1, DeleteTLV1, InfoTLV1, ListTLV1, UpdateTLV1
from .privateLists import TaskType, User


class Entity(Enum):
    CONTACT = "contact"
    COMPANY = "company"
    PROJECT_MILESTONE = "project_milestone"


class Priority(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class Done(Enum):
    YES = 1
    NO = 0


class Subscriptions(AddTLV1, UpdateTLV1, DeleteTLV1, ListTLV1, InfoTLV1):
    def __init__(self, get_teamleader, post_teamleader) -> None:
        self.get = get_teamleader
        self.post = post_teamleader
        self.url = "Subscription"
        super().__init__()


class Tasks:
    def __init__(self, get_teamleader, post_teamleader) -> None:
        self.get = get_teamleader
        self.post = post_teamleader

    def info(self, task_id: int):
        return self.post(
            url_addition="getTask", additional_data={"task_id": task_id}
        ).json()

    def delete(self, task_id: int) -> Response:
        return self.post(
            url_addition="deleteTask", additional_data={"task_id": task_id}
        )

    def update(
        self,
        task_id: int,
        description: str = None,
        duration: int = None,
        task_type: TaskType = None,
        user: User = None,
        priority: Priority = None,
        done: Done = None,
        custom_field_ID: int = None,
    ) -> Response:

        data = {
            "task_id": task_id,
            "description": description,
            "duration": duration,
            "task_type_id": task_type,
            "user_id": user,
            "priority": priority,
            "done": done,
            "custom_field_ID": custom_field_ID,
        }
        return self.post(url_addition="updateTask", additional_data=data)

    def list(self, data=None):

        if data is None:
            data = {}
        there_are_more_pages = True
        c = count(1)
        size = 100
        while there_are_more_pages:
            page_data = {"amount": size, "pageno": next(c)}
            data.update(page_data)
            respons = self.post(url_addition="getTasks", additional_data=data)
            object_lists = respons.json()
            there_are_more_pages = len(object_lists) == size
            for object_element in object_lists:
                yield object_element

    def add(
        self,
        description: str,
        due_date: int,
        user_id: int = User.JAAP_VAN_DEN_BROEK,
        task_type_id: int = TaskType.DOORONTWIKKELING_RECHT_DIRECT,
        duration: int = 0,
        priority: Priority = Priority.D,
        for_what_entity: Optional[Entity] = None,
        for_id: Optional[int] = None,
        creator_user_id: Optional[int] = None,
        related_deal_id: Optional[int] = None,
        related_ticket_id: Optional[int] = None,
        custom_field_id: Optional[int] = None,
    ) -> Response:

        data = {
            "description": description,
            "due_date": due_date,
            "user_id": user_id,
            "task_type_id": task_type_id,
            "duration": duration,
            "priority": priority,
            "for": for_what_entity,
            "for_id": for_id,
            "creator_user_id": creator_user_id,
            "related_deal_id": related_deal_id,
            "related_ticket_id": related_ticket_id,
            "custom_field_ID": custom_field_id,
        }

        return self.post(url_addition="addTask", additional_data=data)


class Tickets(ListTLV1):
    def __init__(self, get_teamleader, post_teamleader) -> None:
        self.get = get_teamleader
        self.post = post_teamleader
        self.url = "Ticket"
        super().__init__()


class Companies(ListTLV1):
    def __init__(self, get_teamleader, post_teamleader) -> None:
        self.get = get_teamleader
        self.post = post_teamleader
        self.url = "Companie"
        super().__init__()

    def info(self, object_id, data={}):
        data.update({"company_id": str(object_id)})
        reponse = self.post(url_addition="getCompany", additional_data=data)
        return reponse.json()


class Contacts(ListTLV1, InfoTLV1):
    def __init__(self, get_teamleader, post_teamleader) -> None:
        self.get = get_teamleader
        self.post = post_teamleader
        self.url = "Contact"
        super().__init__()


class Calls(ListTLV1, AddTLV1):
    def __init__(self, get_teamleader, post_teamleader) -> None:
        self.get = get_teamleader
        self.post = post_teamleader
        self.url = "Call"
        super().__init__()


class TimeTracking(ListTLV1):
    def __init__(self, get_teamleader, post_teamleader) -> None:
        self.get = get_teamleader
        self.post = post_teamleader
        self.url = "Timetracking"
        super().__init__()


class Deals(ListTLV1, AddTLV1):
    def __init__(self, get_teamleader, post_teamleader) -> None:
        self.get = get_teamleader
        self.post = post_teamleader
        self.url = "Deal"
        super().__init__()
