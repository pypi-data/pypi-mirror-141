from itertools import count


class AddTLV1:
    def __init__(self):
        pass

    def add(self, data=None):
        url_addition = "add" + self.url
        if self.url == "Call":
            url_addition = "addCallback"
        return self.post(url_addition=url_addition, additional_data=data)


class UpdateTLV1:
    def __init__(self):
        pass


class DeleteTLV1:
    def __init__(self):
        pass


class ListTLV1:
    def __init__(self):
        pass

    def list(self, data=None):

        if data is None:
            data = {}
        there_are_more_pages = True
        c = count(0)
        size = 100
        while there_are_more_pages:
            page_data = {"amount": size, "pageno": next(c)}
            data.update(page_data)
            url_addition = (
                "get" + self.url + "s"
                if self.url not in ["Timetracking"]
                else "get" + self.url
            )
            respons = self.post(url_addition=url_addition, additional_data=data)
            object_lists = respons.json()
            there_are_more_pages = len(object_lists) == size
            for object_element in object_lists:
                yield object_element


class InfoTLV1:
    def __init__(self):
        pass

    def info(self, object_id, data={}):
        data.update({"contact_id": str(object_id)})
        reponse = self.post(url_addition="get" + self.url, additional_data=data)
        return reponse.json()
